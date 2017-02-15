---
layout: post
title: "Bind9 Notify 问题"
date: 2014-10-15 22:00
---

遇到一个问题, DNS master端之前只有ip 192.168.0.200, 现在又添加了一个ip 192.168.0.100, 其中192.168.0.100是主ip, 192.168.0.200是secondary ip.

slave上master的配置只包含之前配置的192.168.0.200

修改zone文件的serial number后, slave并没有及时同步, 监控发现slave的serial number和master的serial number不一致.

等了几分钟至几十分钟后, 会陆续同步恢复.

如果配置正确, master端会主动发NOTIFY信息, 应该是很快就会同步更新.

查看此[配置文档](http://www.zytrax.com/books/dns/ch7/xfer.html), 关于`bind9` 的master和slave, master修改配置后, 主动给 slave 发`NOTIFY`, 有以下几个配置控制:

* `allow-notify`: slave端配置, 控制允许发送NOTIFY消息的master, 默认是 `master` 里配置的ip列表

* `also-notify`: master端配置, 修改配置后主动给slave发送NOTIFY消息

* `notify`: master和slave都可以配置, 默认是yes, 当配置修改后, 就会发送NOTIFY消息给zone文件里配置的NS和`also-notify`里的ip列表

* `notify-source`: 默认是`*`, 表示当前的主机ip, 可以指定某个ip和port, ip必须在slave的master中包含

然后经过抓包(在master上抓取向slave发送NOTIFY信息的包)发现:

	00:37:25.152884 IP 192.168.0.100.50326 > 192.168.2.50.53: 47421 notify [b2&3=0x2400] [1a] SOA? intra.domain.com. (79)
	00:37:25.178583 IP 192.168.2.50.53 > 192.168.0.100.50326: 47421 notify Refused 0/0/0 (35)

发现NOTIFY信息被拒绝了. 并且这里走的是主ip, 也就是新配的ip, 而这个ip不在slave的master配置中, 即不在slave的allow-notify ip列表里. 所以被拒绝了.

方法之一是在slave的master语句列表中加上master端新增的主ip.

方法之二是在master端使用`notify-source`指定具体从哪个ip发NOTIFY消息, 修改后抓包:

	00:41:57.576905 IP 192.168.0.200.34407 > 192.168.2.50.53: 40373 notify [b2&3=0x2400] [1a] SOA? intra.domain.com. (80)
	00:41:57.603706 IP 192.168.2.50.53 > 192.168.0.200.34407: 40373 notify* 0/0/0 (36)

至于陆续恢复, 是因为zone文件配置的`Refresh`时间:

	1H         ; Refresh
