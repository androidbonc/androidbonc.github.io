---
layout: post
title: "PHP-FPM的chroot"
date: 2016-04-15 12:50
---

之前的[Nginx 和 PHP-FPM 权限安全配置]({% post_url 2016-03-06-nginx-php-fpm-configuration-security %})提到过`chroot`的配置。

不过在一个实际(稍复杂的)环境下，还有很多的依赖文件和lib库需要处理。

比如昨天排查一个程序发送邮件的问题：

1. 首先smtp地址解析不了
2. 开启ssl失败

其中一个方法就是把如 `/dev`、 `/etc`、 '/lib' 等目录做 `mount --bind` 到chroot的环境下。不过增加了维护的成本，比如一个机器上有多个站点要维护，那么就是N个目录乘以站点数，mount列表会很混乱。

也可以定制一个基本的**最小chroot环境**，供后续使用。

这个问题[Problems with chroot php-fpm /nginx and resolving](https://forum.nginx.org/read.php?3,212362,212372)里有人已经给出了一个比较全面的文件列表。

首先是DNS解析问题：

除了要copy一些配置文件，另外就是lib库了。

可以通过一些二进制命令来排查，如常用的`ping`、 `host`等等。将相应的命令和依赖的库copy到chroot环境。如我要使用ping来排查:

	$ ldd `which ping`
	linux-vdso.so.1 (0x00007fff200fa000)
	libc.so.6 => /lib64/libc.so.6 (0x00007fafab504000)
	/lib64/ld-linux-x86-64.so.2 (0x00007fafab8a6000)

注意lib库的查找路径定义在 `/etc/ld.so.conf`，包含子配置目录`/etc/ld.so.conf.d/*`，这些也要copy过去，否则一些如`/usr/lib/gcc/x86_64-pc-linux-gnu/4.9.3/`下的库默认找不到。(参考[update to gcc-4.7.3 killed libgcc_s.so.1](https://forums.gentoo.org/viewtopic-p-7310128.html))

测试chroot下ping:

	$ chroot /path/to/ /bin/ping -c1 example.com

或者:

	$ chroot /path/to /bin/bb     # /bin/bb 即 /bin/busybox
	$ /bin/ping -c example.com

这里推荐使用`busybox` 而不是 `/bin/bash`, 是因为前者不需要额外lib库依赖。

调式的过程中记得要重启php-fpm进程，否则解析不生效。


另外一个是ssl的问题，smtp开启ssl走465端口，看日志是fsockopen()无法开启加密，而ssl, crypto相关的lib库都copy过去了，最后发现是 `/etc/openssl/*` 下的内容没有copy。还有一个要注意里面的一些证书是软链接，需要`cp -L`来将软链接拷贝为实际文件。


参考:

* [Problems with chroot php-fpm /nginx and resolving](https://forum.nginx.org/read.php?3,212362,212372)
* [建立PHP-FPM的Chroot执行环境](https://segmentfault.com/a/1190000003044622)
* [An absolutely minimal chroot](http://sagar.se/an-absolutely-minimal-chroot.html)
* [Chrooted PHP-FPM with Nginx on CentOS 6](http://ae.koroglu.org/chrooted-php-fpm-with-nginx-on-centos-6/)
* [PHP5 - Fails to resolve hostnames when not in interactive mode](http://stackoverflow.com/a/25336617/1276501)
* [php-fpm + FreeBSD 8.2 and SSL issue](https://forum.nginx.org/read.php?3,228808)


