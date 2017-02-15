---
layout: post
title: "iptables的hashlimit模块"
date: 2015-03-18 21:00
---

某机器有一条防DNS攻击的规则:

	iptables -t raw -I dns_limit -m string --algo bm --icase \
		--hex-string "|${hex_domain}|"                       \
		-m hashlimit                                         \
		--hashlimit-name DNS                                 \
		--hashlimit-mode srcip                               \
		--hashlimit-above 1/second                           \
		--hashlimit-burst 1                                  \
		--hashlimit-htable-max 1000000                       \
		--hashlimit-htable-expire 180000                     \
		--hashlimit-htable-gcinterval 30000                  \
		--hashlimit-srcmask 28                               \
		-m comment --comment "${domain}" -j DROP

当时机器上测试dig查询, 发现某个域名被完全封禁了, 而不是预想中的`限速`.

查看iptables的规则链dns_limit, 发现这个域名有两条这样的规则, 删除一条后则和预想一致, 实现了限速.

先说下最主要的, hashlimit 模块的核心是[令牌桶算法(Token Bucket)](http://en.wikipedia.org/wiki/Token_bucket), 这个模块的作用是匹配, 限速是根据匹配结果以及target操作而实现的功能.
当时了解到这个后, 问题就迎刃而解了.

几个参数:

* `--hashlimit-name`: 定义这条hashlimit规则的名称, 所有的条目(entry)都存放在`/proc/net/ipt_hashlimit/{hashlimit-name}`里
* `--hashlimit-mode`: 限制的类型,可以是源地址/源端口/目标地址/目标端口
* `--hashlimit-srcmask`: 当mode设置为srcip时, 配置相应的掩码表示一个网段
* `--hashlimit-above`: mount/quantum, 允许进来的包速率(令牌恢复速率)
* `--hashlimit-burst`: 允许突发的个数(其实就是令牌桶最大容量)
* `--hashlimit-htable-max`: hash的最大条目数
* `--hashlimit-htable-expire`: hash规则失效时间, 单位毫秒(milliseconds)
* `--hashlimit-htable-gcinterval`: 垃圾回收器回收的间隔时间, 单位毫秒

上面是man手册比较正式的解释.

关于 expire 和 gcinterval, 如果在这个时间内没有再次触发规则, 则时间逐渐减为0, 进而负数, 但是并不会从hash中删除, 直到垃圾回收器执行后, 才会删除.

gcinterval 一般设置会比 expire 小, 这个值应配合 expire 选取合适值, 太小会导致频繁占用资源, 太大会导致封禁条目达到失效时间后还需要等待很久才会被删除.

失效时间到达后未被删除, 还是会被封禁.

查看 /proc/net/ipt_hashlimit/DNS 文件:

	$ cat /proc/net/ipt_hashlimit/DNS
	180 X.X.X.X:0->0.0.0.0:0 32000 32000 32000

这里第一个字段是expire倒计时时间(单位是秒), 比如这里设置180000毫秒, 即180s, 如果180s内没有再次触发这个规则, 则会一直减到0 (见上面关于expire解释); 如果触发则再次变为180.

第二个字段是 srcip:port->dstip:port, 这里mode只设置了srcip

第三个字段是当前剩余的令牌数

第四个字段是令牌桶最大容量, 是一个定值

第五个字段是一次触发使用的令牌数, 也是令牌产生速率, 也是一个定值

一秒(second)有`32000`个令牌(TODO 这里没有找到相关说明, 源码也没翻到... 猜测应该是每jiffy(毫秒) 32个令牌), 如果限制是 1req/sec, 则令牌产生速率是 32000/1 = 32000, 如果是 2req/sec, 则第五个字段就是 32000/2 = 16000.

而最大的令牌数就是 `令牌产生速率 * {hashlimit-burst}`, 比如 2req/sec, burst是5, 则第四个字段就是 `32000/2*5 = 80000`

第三个字段每触发一次规则, 都会减去 `令牌产生速率 * 1`个令牌, 并以这个速率恢复. 如果长时间没有触发, 会一直处于和最大令牌数一样的值.

关于hashlimit的匹配结果: 当查询包进来时, 如果令牌足够, 则会减去一次令牌数, 接着恢复, 且接着去下一条规则; 如果在剩余的令牌不足以减去一次查询的令牌, 则匹配这条hashlimit规则, target是DROP时, 则丢弃这个包.

模拟DNS攻击, 查看第三个字段的值, 发现两条规则时, 就是减少两次令牌, 因为一次会减少32000个令牌, 两次减少64000个, 而令牌桶的最大数目是32000, 也就是说这是一个永远无法完成的操作, 当然也就会造成一种完全封禁的情况.

实验测试中, 比如把速率改为 2seq/sec, burst改为3, 一遍dig一遍抓包并查看/proc/net/ipt_hashlimit/DNS文件, 可以看到当令牌不够时, 匹配这个域名后的包确实丢掉了.

---

简单小结下: 开头的这个规则, 主要就是 hashlimit-above 和 hashlimit-burst 这两个参数的设置. 首先匹配上域名, 然后hashlimit会新建一个entry, 用令牌桶管理包速. hashlimit-above 决定了一秒允许多少个包经过, 相应也就是令牌产生的速率, hashlimit-burst决定令牌桶的最大容量, 如果查询包超过这个限制(令牌桶剩余令牌不够), 则匹配上这条规则, DROP掉包, 否则包继续进入下一条规则查看是否匹配.

