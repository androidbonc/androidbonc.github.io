---
layout: post
title: "Rsyslog RELP记录"
date: 2015-01-14 22:30
---

[`RELP`](http://en.wikipedia.org/wiki/Reliable_Event_Logging_Protocol) (Reliable Event Logging Protocol), 是基于TCP封装的可靠日志消息传输协议.

> Unlike the syslog protocol, RELP works with a backchannel which conveys information back to the sender about messages processed by the receiver. This enables RELP to always know which messages have been properly received, even in the case of a connection abort.

<!-- -->

> During initial connection, sender and receiver negotiate session options, like supported command set or application level window size. Network event messages are transferred as commands, where the receiver acknowledges each command as soon as it has processed it. Sessions may be closed by both sender and receiver, but usually should be terminated by the sender side. In order to facilitate message recovery on session aborts, RELP keeps transaction numbers for each command, and negotiates which messages need to be resent on session reestablishment.

---

Rsyslog提供了相应的[`imrelp`](http://www.rsyslog.com/doc/imrelp.html)和[`omrelp`](http://www.rsyslog.com/doc/omrelp.html)模块，用于通过relp通信的发送和接收.

也有一篇详细的[RELP描述](http://www.rsyslog.com/doc/relp.html)

现在对RELP的理解还比较浅显(也可能有错). 简单的说:

RELP是一个C/S模型, 提供了一种command-response模型, 客户端(client)发送命令(command), 服务端(server)收到命令并处理, 返回响应(response)

刚开始建立会话(session)连接时, client会发送一个`open`命令, server收到命令后, 会回复一个`rsp 200`作为响应连接OK. 然后会话就建立起来, 并开始传送数据.

如此图:

![connect ok](https://tankywoo-wb.b0.upaiyun.com/rsyslog-relp-connect.png)

但是如果server端没有响应, 则client会一直发送`open`命令.

连接后, client发送数据, 分块的包发送完毕, server处理完后, 也会响应一个`rsp 200`, 表示这个数据已经完整的发送到server并处理完成.

如此图:

![server send rsp](https://tankywoo-wb.b0.upaiyun.com/rsyslog-relp-send-ok.png)

---

最近遇到一个问题, 部分节点异常, server没有收到日志, 在节点上抓包排查, 因为程序是一分钟发送一次数据, 但是一直没看到有发送数据的包, 只看到一直不停的发送`open`命令包.

重启正常节点的rsyslog, 然后也异常了.

尝试把relp改为直接写入本地文件, 也是正常的.

最初怀疑是系统更新过, 导致omrelp模块(`/usr/lib/rsyslog/omrelp.so`)有问题, 但是对比了正常的机器, 发现所有相关组件都一样.

然后怀疑到server的问题, 尝试重启server, 恢复了.

当时正好抓包, 看到一个`rsp 200 OK`的回应, 看了下relp的文档, 了解到建立会话时的一个command-response模型.

但是这个问题不好回溯, 刚好第二天再次出现了这个问题. 于是`strace`跟踪进程, 发现刷屏式的提示`too many open files`. 如图:

![strace分析](https://tankywoo-wb.b0.upaiyun.com/rsyslog-relp-strace-cap.png)

想到omprog处理imrelp收到的日志, 连接的节点太多, 每个节点都需要写入文件, 导致的这个问题.

继续搜索发现rsyslog有配置ulimit的相关参数[`$MaxOpenFiles`](http://www.rsyslog.com/doc/rsconf1_maxopenfiles.html), 把最大打开文件数给调大了.

<strike>TODO: 这几天再观察下, 看看是否还有这个问题出现.</strike>

---

2015-01-22 补充:

首先设置了`$MaxOpenFiles`后，这几天没有出现这个问题.

另外，今天查看了下rsyslog的文件句柄数:

    lsof -a -p `pgrep rsyslog` | wc -l

或者:

    ls -l /proc/`pgrep rsyslog`/fd/ | wc -l

一个tcp connection一个文件句柄，按理应该不会超过系统默认的ulimit:

    $ cat /proc/`pgrep rsyslog`/limits | grep 'Max open files'
    Limit                     Soft Limit           Hard Limit           Units
    Max open files            1024                 4096                 files

默认应该可以达到Hard Limit.

后来和BOSS说到这事, 知道他修改了一个地方, 这个地方很关键.

BOSS之前发现一个节点会有好几个tcp连接, 有些还没有及时关闭掉.(这里我之前没有去查看...)

之前rsyslog的版本是7.x, 用的是老配置(legacy rsyslog), 在`8.1.4`版本以后，新的配置语法(RainerScript)对[`imrelp`](http://www.rsyslog.com/doc/imrelp.html)增加了`KeepAlive`的选项, 这个选项默认是关闭的.

升级到新版本的rsyslog, 给imrelp配置上这个参数, 查看进程的文件句柄, 发现都是一个节点一个文件句柄了.

    # 老的配置 legacy rsyslog
    $ModLoad imrelp

    # 新的配置 RainerScript
    module(load="imrelp")
    input(type="imrelp" port="514" KeepAlive="on")

圆满解决 :)
