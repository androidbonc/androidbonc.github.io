---
layout: post
title: "host localhost?"
date: 2016-06-01 22:45
---

之前有时看下localhost，要么`ping`， 要么`host`(或者`dig`)。

昨天在回答一个[Issue](https://github.com/tankywoo/simiki/issues/60)后，我本地测试了下，发现`host localhost`没有结果，但是在线上机器是可以返回：

```
$ host localhost
localhost has address 127.0.0.1
localhost has IPv6 address ::1
```

印象中，一直以为像`host`这类dns解析命令也会根据nsswitch配置读取`/etc/hosts`。现在看来是错的。

下面这个回答解释的很清楚：

> The `host` program uses `libresolv` to perform a DNS query directly, i.e., does not use `gethostbyname`.
> 
> Most programs, when attempting to connect to another host, invoke the `gethostbyname` system call or a similar function. This function obeys the configuration of `/etc/nsswitch.conf`. This file has a line which in Ubuntu 12.04 defaults to the following:
> 
>     hosts:          files mdns4_minimal [NOTFOUND=return] dns mdns4
> 
> which means that it will first use `/etc/hosts`, then fall back to DNS queries.
> 
> 
> If you want to perform a host lookup this way, you can do this with `getent hosts`.  For example:
> 
>     $ getent hosts serverfault.com
>     198.252.206.16  serverfault.com
> 
> I hope this helps.

像`host`，`nsloopup`，`dig`这类工具只是单纯的DNS解析工具，根据`/etc/resolv.conf`配置的nameserver去做解析；并不会涉及到NSS。

根据`strace`的结果也可以看到，比如`ping`命令，通过读取`/etc/nsswitch.conf`，首先得到的是files，于是调用`/lib64/libnss_files.so`，查看`/etc/hosts`自定义的别名。

而在线上机器之所以可以host得到结果，是因为本地DNS(Bind9)配置了localhost的zone：

```
$ cat named.conf
zone "localhost" in{
  type master;
  file "master.localhost";
};

$ cat master.localhost
$TTL	86400 ; 24 hours could have been written as 24h or 1D
$ORIGIN localhost.
; line below expands to: localhost 1D IN SOA localhost root.localhost
@  1D  IN	 SOA @	root (
			      2002022401 ; serial
			      3H ; refresh
			      15 ; retry
			      1w ; expire
			      3h ; minimum
			     )
@  1D  IN  NS @ 
   1D  IN  A  127.0.0.1
```

> This zone allows resolution of the name localhost to the loopback address 127.0.0.1 when using the DNS server. Any query for 'localhost' from any host using the name server will return 127.0.0.1.

参考[named.conf - localhost](http://www.zytrax.com/books/dns/ch7/)

所以线上的这个结果，是根据配置的nameserver, 进而查询获取的结果。

