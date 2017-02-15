---
layout: post
title: "PXE and Kickstart Deploy Operation"
date: 2014-01-13 14:46
comments: true
categories: Linux
---

<!-- more -->

环境：

* 服务器系统: ubuntu 12.04
* 客户端要安装的是: ubuntu 12.04

一台服务器，装好 Ubuntu 12.04. 客户端要自动部署的也是 Ubuntu 12.04.

PXE 整体的流程图(这两个算是把流程体现的比较清晰的):

![dhcp流程图](https://tankywoo-wb.b0.upaiyun.com/pxe_process.png)

(图1)

![dhcp流程图](https://tankywoo-wb.b0.upaiyun.com/pxe_process2.jpg) 

(图2)

## 准备工作 ##


首先把 ubuntu 12.04 的镜像(`ubuntu-12.04.2-server-amd64.iso`)在服务端挂载上:

	mkdir -p /mnt/ubuntu1204
	mount -o loop ubuntu-12.04.2-server-amd64.iso /mnt/ubuntu1204
	# 因为这样挂载是只读的, 为了方便, 把 ks.cfg 也需要共用这个目录以提供http访问, 所以可以拷贝出来.
	cp -r /mnt/ubuntu1204 /mnt/ubuntu
	

安装软件:

* `nginx`
* `isc-dhcp-server`
* `tftpd-hpa`
* `system-config-kickstart`
* `syslinux`


## Nginx ##

Nginx 配置很简单, 因为kickstart的安装方式选择通过 `url`来安装, 所以这里需要提供一个web服务器。 

安装 `nginx` , Ubuntu 下可以在 `/etc/nginx/sites-enabled` 下放一个配置文件:

	server {
	        listen   80; ## listen for ipv4; this line is default and implied
	
	        root /mnt/ubuntu/;
	        index index.html index.htm;
	        autoindex on;
	
	        # Make site accessible from http://localhost/
	        server_name localhost;
	}
	
(注意nginx默认配置是用的80端口, 可以把这个配置的给禁用掉, 或者直接在上面修改。)

重启 nginx:

	service nginx restart

这样就可以通过 http://x.x.x.x/ 来访问。

## DHCP ##

动态主机配置协议 (Dynamic Host Configuration Protocol)

DHCP服务器端使用67/udp，客户端使用68/udp。

DHCP 的流程图:

![dhcp流程图](https://tankywoo-wb.b0.upaiyun.com/dhcp_session.png!small) 

图片来至 [维基百科](http://zh.wikipedia.org/wiki/DHCP)

DHCP运行分为四个基本过程，分别为请求IP、提供IP、选择IP和确认IP。

查看日志也可以看出:

	Jan 16 15:01:58 pxe-test dhcpd: DHCPDISCOVER from 00:0c:29:83:d1:d1 via eth1
	Jan 16 15:01:58 pxe-test dhcpd: DHCPOFFER on 192.168.0.214 to 00:0c:29:83:d1:d1 via eth1
	Jan 16 15:01:58 pxe-test dhcpd: DHCPREQUEST for 192.168.0.214 (192.168.0.150) from 00:0c:29:83:d1:d1 via eth1
	Jan 16 15:01:58 pxe-test dhcpd: DHCPACK on 192.168.0.214 to 00:0c:29:83:d1:d1 via eth1

另外在DHCP整个过程中, 还有一个 `租约` 的问题, 用来防止一个 ip 被某台机器长时间占用。

更多的细节推荐看《[鸟哥的Linux私房菜 服务器架设篇 12章 DHCP服务器](http://vbird.dic.ksu.edu.tw/linux_server/0340dhcp.php)》和 `man 5 dhcpd.conf`, 配合默认的配置文件, 里面的注释已经很详细了。

安装 `isc-dhcp-server`.

修改 `/etc/default/isc-dhcp-server`, 配置 dhcpd 服务器在哪个网口回应 dhcp 请求:

	# On what interfaces should the DHCP server (dhcpd) serve DHCP requests?
	#       Separate multiple interfaces with spaces, e.g. "eth0 eth1".
	INTERFACES="eth1"

因为一台机器可能有多块网卡, 不同的网络, 配的网段一般也不一样, 如果在所有网卡监听, 则会出问题。

比如:

	eth0 : 192.168.0.0/24
	eth1 : 192.168.1.0/24
	dhcp 配置的自动分配 ip 段是 range 192.168.0.100 192.168.0.150;
	如果在 eth0 和 eth1 上都监听, 那 192.168.1.0/24 下的一个客户端请求 dhcp 时, dhcp 服务器也会回应并分配一个 192.168.0.0/24 段的 ip。


配置 `/etc/dhcp/dhcpd.conf`:

	root@pxe-test:~# cat /etc/dhcp/dhcpd.conf
	default-lease-time 600;
	max-lease-time 7200;
	
	subnet 192.168.0.0 netmask 255.255.255.0 {
	    authoritative;
	    option routers 192.168.0.1;
	    option broadcast-address 192.168.0.255;
	    option domain-name-servers 192.168.0.1;
	    option domain-name "mydomain.example";
	    range 192.168.0.210 192.168.0.220;
	    filename "/pxelinux.0";
	}

这里的 `filename "/pxelinux.0";` 是针对 tftp 文件存放目录的位置。

重启 dhcpd 服务:

    service isc-dhcp-server restart
    
可以通过 `/var/lib/dhcp/dhcpd.leases` 查看已分配 ip 和相关信息。

	lease 192.168.0.211 {
		starts 6 2014/01/18 13:50:34;
		ends 6 2014/01/18 14:00:34;
		cltt 6 2014/01/18 13:50:34;
		binding state active;
		next binding state free;
		rewind binding state free;
		hardware ethernet 00:0c:29:62:ec:eb;
		client-hostname "gentoo-jl";
	}

注意 dhcpd 需要配置 dns, 不然通过 kickstart 部署时中途会停止等待dns配置.


参考：

* [Ubuntu 12.04 安裝 DHCP server](http://dragonspring.pixnet.net/blog/post/37398356-%5B%E7%AD%86%E8%A8%98%5D-ubuntu-12.04-%E5%AE%89%E8%A3%9D-dhcp-server)
* [Dynamic Host Configuration Protocol (DHCP)](https://help.ubuntu.com/13.10/serverguide/dhcp.html)

## tftp-hpa ##

`tftp` (Trivial File Transfer Protocol)是简单文件传输协议。没有 `ftp` 那么多的功能, 因为非常简单, 所以非常适合 PXE 引导使用。而且 ftp 使用的是 tcp 的 21 端口, tftp 使用的是 udp 的 69 端口。

更多可以看下 [维基百科 - TFTP](http://en.wikipedia.org/wiki/Trivial_File_Transfer_Protocol)

(tftp 功能太简单了, 所以当时我想连接上tftp服务器后, 执行list或目录传输, 都是不支持的, 囧)

安装 `tftp-hpa`, 配置文件 `/etc/default/tftpd-hpa`, 保持默认不变。

	# /etc/default/tftpd-hpa
	
	TFTP_USERNAME="tftp"
	TFTP_DIRECTORY="/var/lib/tftpboot"
	TFTP_ADDRESS="0.0.0.0:69"
	TFTP_OPTIONS="--secure"

启动服务

	service tftp-hpa start

tftp-hpa 文件的默认存放位置是 `TFTP_DIRECTORY` 配置的，在 `/var/lib/tftpboot`。


## Kickstart ##

> The Red Hat Kickstart installation method is used primarily (but not exclusively) by the Red Hat Enterprise Linux operating system to automatically perform unattended operating system installation and configuration. Red Hat publishes Cobbler as a tool to automate the Kickstart configuration process.
> 
> Kickstart is normally used at sites with many such Linux systems, to allow easy installation and consistent configuration of new computer systems.
> Kickstart configuration files can be built three ways:
> 
>	* By hand.
>	* By using the GUI system-config-kickstart tool.
>	* By using the standard Red Hat installation program Anaconda.

> Anaconda will produce an anaconda-ks.cfg configuration file at the end of any manual installation. This file can be used to automatically reproduce the same installation or edited (manually or with system-config-kickstart).

[来源 Kickstart (Linux)](http://en.wikipedia.org/wiki/Kickstart\_(Linux))

kickstart 是 `Red Hat` 自动部署安装的方式。(后面提到了, `Debian` 系还有 `preseed`)

安装 `system-config-kickstart`(graphical tool for creating Kickstart files), 是一个图形化生成 kickstart 文件的工具，也支持命令行。

	system-config-kickstart --generate ks.cfg
	
生成 ks.cfg 文件, 这个是根据本机生成的一份配置。

然后可以在这个基础上进行定制， 参考语法:

* [Kickstart Options - RedHat6](https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Installation_Guide/s1-kickstart2-options.html) *
* [Kickstart Options - Centos5](http://www.centos.org/docs/5/html/Installation_Guide-en-US/s1-kickstart2-options.html)
* [Anaconda/Kickstart](http://fedoraproject.org/wiki/Anaconda/Kickstart)
* [create Logical Volume Manager (LVM) partitions using kickstart](http://rhcelinuxguide.wordpress.com/2006/06/03/create-logical-volume-manager-lvm-partitions-using-kickstart/)

给一个参考:

	#Generated by Kickstart Configurator
	#platform=x86
	
	#System language
	lang en_US.UTF-8
	#Language modules to install
	langsupport en_US.UTF-8 --default=en_US.UTF-8
	#System keyboard
	keyboard us
	#System mouse
	mouse
	#System timezone
	# XXX: must set --utc, otherwise it will wait network clock setting  for a while.
	timezone --utc Asia/Harbin
	# Text mode to install
	text
	#Root password, XXX: init is 123456789
	rootpw --iscrypted $6$cf89bJ4V$G8Eb2JAtOQWrGxgU1gP4TTunrd..JXcJRULGnjFC08Z7/mzcXTeOVNiNUqg7.4DfhSbjBEBmTfC1lxMHH.f0u0
	#Initial user
	user --disabled
	#Install OS instead of upgrade
	install
	url --url http://x.x.x.x/
	# System bootloader configuration
	bootloader --location=mbr
	#Clear the Master Boot Record
	zerombr yes
	#Partition clearing information
	clearpart --all --initlabel
	
	# Partition Disk
	# XXX: --ondisk and --label not support under Ubuntu12.04
	part / --fstype=ext3 --size=2048 --asprimary
	part pv.01 --size=1 --asprimary --grow
	volgroup vg_data pv.01
	logvol  /home  --vgname=vg_data  --size=1024  --name=lv_home
	# XXX: if no swap partition, ubuntu will ask.
	logvol  swap  --vgname=vg_data  --size=1024  --name=lv_swap
	
	# Disable Firewall
	firewall --disabled
	# Do not configure the X Window System
	skipx
	# Disable SELinux
	selinux --disabled
	# Specify the minimum level of messages that appear on tty3
	logging --level=info
	# Reboot after finish installtion
	reboot
	
	#Package install information
	%packages
	openssh-client
	openssh-server
	rsync
	screen
	ubuntu-minimal
	vim
	
	%post
	e2label /dev/sda1 /
	e2label /dev/vg_data/lv_home /home
	swaplabel -L lvmswap /dev/vg_data/lv_swap

里面一些需要注意的地方都用 `XXX` 标记给标注了。 初始密码设置为 123456789, 分了三个区, 根分区 ext3, /home分区和swap分区使用 lvm。

可以把这个 ks.cfg 放到 /mnt/ubuntu/ 下, 这样就可以通过: http://x.x.x.x/ks.cfg 访问到。


*补充* :

注意这里有个坑，当时用 system-config-kickstart 生成的 ks.cfg 文件中, 关于 `%packages` 一段的格式是:

	%packages
	ubuntu-minimal
	vim
	rsync
	(...)
	
但是我看了redhat的语法后，加了一个结束标记 `%end`，然后每次到安装软件时都报错, 但是其实前面的软件都安装完了，可以直接进行下一步安装 grub 了。

`Ctrl+Alt+F3` 切换到 tty3 下 `tail -n 20 /var/log/syslog` 可以看到:

	unable to locate package %end

Ubuntu 的 ks 文件语法看来是不需要去指定结束标记。

因为 kickstart 主要是针对 `REHL` 系的。在 `Debian` 系有些语法不一样，比如针对分区的 `part` 命令, 至少在我本地测试了, `--ondisk` 和 `--label` 这些选项都用不了。所以估计这里也是语法针对 Debian 系有点问题。 具体可以看看这个 [BUG报告](https://bugs.launchpad.net/ubuntu/+source/kickseed/+bug/537421) 。

另外， `Debian` 系也有自己的自动部署工具 `preseed`, 这个还需要了解。**TODO**

## PXELINUX ##

> PXELINUX is a SYSLINUX derivative, for booting Linux from a network server using a network ROM conforming to the Intel PXE (Pre-Execution Environment) specification. 

[来源 PXELINUX](http://www.syslinux.org/wiki/index.php/PXELINUX)

安装 `syslinux`(或者在官网直接下载syslinux压缩包, 解压), 安装后的一些文件在 `/usr/lib/syslinux/` 里.

将 `pxelinux.0`(或 `gpexlinux.0`) 以及 `menu.c32` 拷贝到 tftp-hpa 的文件目录下(/var/lib/tftpboot).

在 /var/lib/tftpboot 下新建一个目录 `pxelinux.cfg`, 里面放一个文件名叫`default`:

	root@pxe-test:/var/lib/tftpboot# cat pxelinux.cfg/default
	########
	# Ref: http://www.syslinux.org/wiki/index.php/SYSLINUX#How_do_I_Configure_SYSLINUX.3F
	########
	
	# Default boot option to use
	DEFAULT menu.c32
	MENU TITLE PXE
	
	prompt 0
	
	# Timeout in units of 1/10 s
	TIMEOUT 100
	
	LABEL Ubuntu/12.04
	    MENU LABEL Ububtu/12.04
	    KERNEL linux
	    APPEND vga=normal initrd=initrd.gz ks=http://x.x.x.x/ks.cfg
	
	MENU SEPARATOR
	
	LABEL localboot
	    LOCALBOOT 0x80
	    MENU LABEL ^Boot from local disk

其中, `ks=http://x.x.x.x/ks.cfg` 是 ks 文件存放的位置, 通过http方式来获取。


接着拷贝 /mnt/ubuntu/ 下的 `install/netboot/ubuntu-installer/amd64/` 里的 `initrd.gz` 和 `linux` 到 pxelinux.cfg 目录下.
(如果想通过网络安装, 则可以只下载Ubuntu 的 [netboot](http://archive.ubuntu.com/ubuntu/dists/precise-updates/main/installer-amd64/current/images/netboot/))

并把 `ks.cfg` 也放到 ubuntu 目录下.

整体的结构是:

	root@pxe-test:/var/lib/tftpboot# tree
	.
	├── initrd.gz
	├── linux
	├── menu.c32
	├── pxelinux.0
	└── pxelinux.cfg
	    └── default
	
	1 directory, 5 files


## 总结 ##

PXE自动化部署, 是需要经过本地大量测试, 才能整理出一份配置。可能针对不同的服务端和客户端, 配置会有少许不同。

而且中间也有一些位置, 需要大量实验, 才能知道如何测底自动化。

比如:

* 在DHCP中如果没有配置dns, 则ubuntu安装时会等待是否配置dns, 这时就需要人工干预了。
* 在配置时钟和时区, 刚开始这么配置 `timezone Asia/Harbin`, 就会在配置时钟时等待将近半分钟, 后来配置选项 `--utc` 就解决这个问题了。

最后根据最开始给出的自动部署流程图, 了解每个服务, 在不同阶段的作用。

总得来说, 部署方式有以下几种:

1. dhcp + tftp : 联网手动部署
2. dhcp + tftp + kickstart : 联网自动部署
3. dhcp + tftp + web服务器 + ubuntu镜像 : 局域网手动部署
4. dhcp + tftp + web服务器 + ubuntu镜像 + kickstart : 局域网自动部署

<!-- -->

- dhcp 就是为了在 pxe boot 时分配ip, 已经在Ubuntu安装刚开始时会自动配置ip
- tftp 是pxe boot时要传输kernel等引导一个系统起来
- web服务器提供解压后系统镜像的访问以及ks.cfg的访问(ks.cfg也可以通过比如ftp, nfs等方式传输)
- kickstart 是为了自动化

配置文件我放到Github上: [PXE-Deploy](https://github.com/tankywoo/PXE-Deploy)


## 参考资料 ##

* [PXELINUX](http://www.syslinux.org/wiki/index.php/PXELINUX) *
* [PXE 安装系统配置 Howto(clanzx)](http://blog.clanzx.net/2013/08/21/pxe.html) *
* [pxelinux.cfg文件的语法](http://www.syslinux.org/wiki/index.php/SYSLINUX#How_do_I_Configure_SYSLINUX.3F) *
* [pxelinux.cfg文件的语法2](http://www.syslinux.org/wiki/index.php/Comboot/menu.c32) *
* [kickstart 选项](http://man.ddvip.com/os/redhat9.0cut/s1-kickstart2-options.html) *
* [Anaconda/Kickstart 选项](https://fedoraproject.org/wiki/Anaconda/Kickstart/zh-cn) *
* [Kickstart Oracle Linux from Ubuntu](http://www.perkin.org.uk/posts/kickstart-oracle-linux-from-ubuntu.html) *
* [DHCP+tftp+pxe+kickstart自动安装Linux系统](http://my.oschina.net/alanlqc/blog/147649) *
* [PXE网络批量安装ubuntu](http://www.williamsang.com/archives/1842.html)
* [PXE安装Ubuntu](http://www.ialps.cn/2013/01/29/pxeinstallubuntu.html) *
* [Setting up a server for PXE network booting](http://www.debian-administration.org/articles/478)
* [(complex) partitioning in kickstart](https://www.dark.ca/2009/08/03/complex-partitioning-in-kickstart/)
* [Linux下网络启动服务器安装和配置方法(pxe+tftp+dhcpd)](http://lanlian.blog.51cto.com/6790106/1308030)
* [主流Linux版本自动化安装](http://www.xdays.info/%E4%B8%BB%E6%B5%81linux%E7%89%88%E6%9C%AC%E8%87%AA%E5%8A%A8%E5%8C%96%E5%AE%89%E8%A3%85.html)
* [Contents of the preconfiguration file (for precise)](https://help.ubuntu.com/12.04/installation-guide/i386/preseed-contents.html#preseed-partman)
