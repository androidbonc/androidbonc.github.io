---
layout: post
title: "关于Ubuntu下sysvinit和upstart管理网络的问题"
date: 2014-06-04 11:38
categories: Linux
---

<!-- more -->

关于 Ubuntu 12.04 Server 下重启网络:

	root@ubuntu:~# sudo /etc/init.d/networking restart
	 * Running /etc/init.d/networking restart is deprecated because it may not enable again some interfaces
	 * Reconfiguring network interfaces...                                                                                                                                              ssh stop/waiting
	ssh start/running, process 1697                        [ OK ]

	root@ubuntu:~# service networking restart
	stop: Unknown instance:
	networking stop/waiting

如果用 `/etc/init.d/xxx` 重启，都会提示这个方式是过时的，但是使用 `service xxx restart` 方式又不行。

网上也有很多关于这个的提问

最简单的方式就是使用 `ifup` 和 `ifdown`:

	ifdown eth0 && ifup eth0

或针对SSH连接：

	nohup sh -c "ifdown eth0 && ifup eth0 "

当然，重启网络很快，还不至于导致SSH连接断掉。

还有推荐使用：

	service network-manager restart

不确定 `network-manager` 是不是在desktop版下自带的，至少默认的server版是没有，还需要安装。

在[Ubuntu Bugs](https://bugs.launchpad.net/ubuntu/+source/sysvinit/+bug/440179)里也有人提到。

另外想到了 `/etc/init.d/xxx` 和 `service xxx` 这两种方式的区别。

`man service` :

> service runs a System V init script or upstart job
>
> /etc/init.d
>	The directory containing System V init scripts.
> 
> /etc/init
>	The directory containing upstart jobs.

service方式可以管理老式的`System V`启动脚本，即`/etc/init.d/`下的，也可以管理新式的`upstart`方式，即`/etc/init/` 下。

AskUbuntu上有两篇回答不错:

[回答1](http://askubuntu.com/questions/2075/whats-the-difference-between-service-and-etc-init-d):

> `/etc/init.d` scripts are the old way of doing things. They come from the System V standard. However, those scripts are fired only in a particular sequence, no real dependencies can be established.
> 
> Therefore, upstart has been developed with the intent to substitute all the `/etc/init.d` scripts with upstart scripts (in `/etc/init`).
> 
> `service` allows the smooth transition from `/etc/init.d` scripts to upstart scripts. When in the future more on more scripts are transferred to upstart, service will still work, because it finds both possibilties.

[回答2](http://askubuntu.com/questions/5039/what-is-the-difference-between-etc-init-and-etc-init-d)

> `/etc/init.d` contains scripts used by the [System V](http://en.wikipedia.org/wiki/UNIX_System_V) init tools (SysVinit). This is the traditional service management package for Linux, containing the `init` program (the first process that is run when the kernel has finished initializing¹) as well as some infrastructure to start and stop services and configure them. Specifically, files in `/etc/init.d` are shell scripts that respond to `start`, `stop`, `restart`, and (when supported) `reload` commands to manage a particular service. These scripts can be invoked directly or (most commonly) via some other trigger (typically the presence of a symbolic link in `/etc/rc?.d/`).
> 
> `/etc/init` contains configuration files used by Upstart. Upstart is a young service management package championed by Ubuntu. Files in `/etc/init` are configuration files telling Upstart how and when to `start`, `stop`, `reload` the configuration, or query the `status` of a service. As of lucid, Ubuntu is transitioning from SysVinit to Upstart, which explains why many services come with SysVinit scripts even though Upstart configuration files are preferred. In fact, the SysVinit scripts are processed by a compatibility layer in Upstart.
> 
> `.d` in directory names typically indicates a directory containing many configuration files or scripts for a particular situation (e.g. `/etc/apt/sources.list.d` contains files that are concatenated to make a virtual `sources.list`; `/etc/network/if-up.d` contains scripts that are executed when a network <strong>i</strong>nter<strong>f</strong>ace is activated). This structure is usually used when each entry in the directory is provided by a different source, so that each package can deposit its own plug-in without having to parse a single configuration file to reference itself. In this case, it just happens that “init” is a logical name for the directory, SysVinit came first and used `init.d`, and Upstart used plain `init` for a directory with a similar purpose (it would have been more “mainstream”, and perhaps less arrogant, if they'd used `/etc/upstart.d` instead).

[这篇](http://my.oschina.net/lvyi/blog/183123)是上面的翻译说明。

已知的服务管理器有 `sysvinit`，`systemd`，`upstart`

Ubuntu之前使用的是`sysvinit`，后来改为异步的`upstart`方式，为了对以前的方式兼容，至少到现在为止，还是支持`sysvinit`的，只是会提示过时，建议用service命令管理。

继续前面关于Ubuntu网络服务管理的问题

	root@ubuntu:~# status networking
	networking stop/waiting

<!-- -->

	root@cdn-tpl:/etc/init# which status
	/sbin/status
	root@cdn-tpl:/etc/init# ll /sbin/status
	lrwxrwxrwx 1 root root 7 Jan 19  2013 /sbin/status -> initctl*

`status`命令是initctl的别名，相当于调用`initctl status xxx`

`initctl`是一个upstart守护进程的管理工具

关于 `initctl` 和 `service` 的区别，我暂时觉得可能就是 `service` 兼容(管理)了sysvinit的脚本。

另外关于 `initctl list` 和 `service --status-all` 也有区别，`man service`中有解释:

> service --status-all runs all init scripts, in alphabetical order, with the status command. This option only calls status for sysvinit jobs, upstart jobs can be queried in a similar manner with initctl list'.

如果要查看upstart服务，使用前者。

`service --status-all`输出的一部分:

	 [ ? ]  resolvconf
	 [ - ]  rsync
	 [ ? ]  rsyslog
	 [ ? ]  screen-cleanup
	 [ ? ]  sendsigs
	 [ ? ]  setvtrgb
	 [ + ]  ssh
	 [ - ]  stop-bootlogd
	 [ - ]  stop-bootlogd-single
	 [ ? ]  sudo
	 [ ? ]  udev

关于前面 `+`，`-`和`?`的意义，man/info里都没找到，不过在这个[帖子](http://ubuntuforums.org/archive/index.php/t-1574977.html)里有人解释了:

> "+" started
> 
> "-" stopped
> 
> "?" unknown

实际测试:

	root@ubuntu:~# /etc/init.d/rsync status
	 * rsync is not running

	root@ubuntu:~# /etc/init.d/ssh status
	Rather than invoking init scripts through /etc/init.d, use the service(8)
	utility, e.g. service ssh status

	Since the script you are attempting to invoke has been converted to an
	Upstart job, you may also use the status(8) utility, e.g. status ssh
	ssh start/running, process 1697

另外也可以看到/etc/init.d/下很多脚本指向`/lib/init/upstart-job`:

	lrwxrwxrwx  1 root root   21 Nov 27  2013 rsyslog -> /lib/init/upstart-job*
	lrwxrwxrwx  1 root root   21 Jun  7  2011 screen-cleanup -> /lib/init/upstart-job*
	-rwxr-xr-x  1 root root 4321 Jul 27  2012 sendsigs*
	lrwxrwxrwx  1 root root   21 Apr 20  2012 setvtrgb -> /lib/init/upstart-job*
	-rwxr-xr-x  1 root root  590 Jul 27  2012 single*
	-rw-r--r--  1 root root 4304 Jul 27  2012 skeleton
	-rwxr-xr-x  1 root root 4371 Apr 11  2013 ssh*

这些都是upstart管理的服务，只是在/etc/init.d/下作了一个软链接。

接着看下initctl下管理的network服务:

	root@ubuntu:/etc/init.d# initctl list | grep network
	network-interface (lo) start/running
	network-interface (eth0) start/running
	network-interface-security (network-interface/eth0) start/running
	network-interface-security (network-interface/lo) start/running
	network-interface-security (networking) start/running
	networking stop/waiting
	network-interface-container stop/waiting

网络肯定是启动的，所以networking是管理不了，但是`network-interface`可以。

	root@ubuntu:~# status network-interface INTERFACE=eth0
	network-interface (eth0) start/running

	root@ubuntu:/etc/init.d# service network-interface status INTERFACE=eth0
	network-interface (eth0) start/running

所以重启网络用`network-interface` 也可以:

	root@ubuntu:/etc/init.d# service network-interface restart INTERFACE=eth0
	network-interface stop/waiting
	network-interface (eth0) start/running

OK，一个Ubuntu中sysvinit和upstart管理网络的问题，各种延伸查找资料，知识面也扩展了一些。

接下来要了解upstat具体的管理方式和配置，进一步看看为何`service networking restart`不行。

---

补充：

刚在微博把这篇文章贴出来，基友 @[枯木](http://kumu-linux.github.io/) 就找上我了，他前阵子在14.04下也遇到相关的问题，详见[Ubuntu14.04重启网卡不生效](http://kumu-linux.github.io/blog/2014/05/28/ubuntu-network-br0/)
