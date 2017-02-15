---
layout: post
title: "Rsyslog Troubleshooting"
date: 2016-08-31 18:15
---

注：虽然标题写的是关于rsyslog的排查，但是最终定位的原因和rsyslog无关。

最近发现有几个机器，rsyslog没有写日志，syslog, kern.log, auth.log等最近一阵子都是空的，系统是Ubuntu 12.04。

最开始以为是rsyslog的队列被阻塞了，但是某些文件还是可以写日志，并且relp和udp传输都没问题。

又怀疑是写`/dev/log`有问题，然后`strace`跟踪`logger`写日志，以及rsyslog进程读取日志，可以看到rsyslog进程是可以从`/dev/log`中读到数据的。

接着批量排查这些机器出问题的情况，以及如syslog、kern.log、auth.log等出问题的时间，发现syslog都是13号出问题，kern.log、auth.log都是17号出的问题，且都是在`logrotate`后就没再写的。

进而`lsof`查看进程打开文件：

```bash
$ lsof -p 3298
...
rsyslogd 3298 syslog    0u  unix 0xffff88045cbb8700       0t0      15782 /dev/log
rsyslogd 3298 syslog    1w   REG                8,1  43547200    1165974 /var/log/auth.log-20160717 (deleted)
rsyslogd 3298 syslog    2w   REG                8,1 104865976    1165937 /var/log/syslog-20160713 (deleted)
rsyslogd 3298 syslog    4r   REG                8,1     31234    1187914 /var/log/nginx/error.log
rsyslogd 3298 syslog    5u  IPv4              32071       0t0        UDP *:53148
rsyslogd 3298 syslog    7u  IPv4              32079       0t0        UDP *:57178
rsyslogd 3298 syslog   10w   REG                8,1     90557    1165931 /var/log/kern.log-20160717 (deleted)
```

确实这些文件经过`logrotate`后就没再reload了。

查看logrotate对rsyslog的轮转，因为syslog文件是一天一次，auth.log、kern.log是一周一次，而12号还ok，13号凌晨rotate日志就出问题，所以可以断定是12号时有异常。

另外rsyslog是通过`upstart`方式被启动和管理的, 所以logroate中对rsyslog的reload是执行命令`reload rsyslog`，本质是发`HUP`信号。但是我尝试reload失败，直接发信号是可以重启：

```bash
$ reload rsyslog
reload: Unknown instance:
```

说明是upstart事件管理这块出了问题！

查看12号遗留下来的日志，在kern.log中找到这条：

```
2016-07-12T14:18:55.230383+08:00 test-vm-1 kernel: [3529142.933530] init: Re-executing /sbin/init
```

检查其它异常机器，同一时间都报这个，第一感觉就是这块出了问题。

`init u` 或者 `kill -TERM 1` 都会导致重执行。

测试机器上测试，确实可以重现这个问题。

执行这个后，原init进程管理的upstart jobs就相当于脱离控制了，而新的init进程对这些因为没有之前的控制，认为是stop的状态，尝试启动也会因为冲突而无法进来。

目前只能杀掉老的rsyslog进程，然后再通过`initctl`重新启动。
