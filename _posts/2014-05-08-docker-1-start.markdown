---
layout: post
title: "Docker 1 -- 开始"
date: 2014-05-08 15:30
categories: Docker
---

	 
							##        .
					  ## ## ##       ==
				   ## ## ## ##      ===
			   /""""""""""""""""\___/ ===
		  ~~~ {~~ ~~~~ ~~~ ~~~~ ~~ ~ /  ===- ~~~
			   \______ o          __/
				 \    \        __/
				  \____\______/
	 
				  |          |
			   __ |  __   __ | _  __   _
			  /  \| /  \ /   |/  / _\ |
			  \__/| \__/ \__ |\_ \__  |
	 


几个概念:

`IAAS (Infrastructure As A Service)` :

The base layer
Deals with Virtual Machines, Storage (Hard Disks), Servers, Network, Load Balancers etc

`PAAS (Platform As A Service)` :

A layer on top of IAAS
Runtimes (like java runtimes), Databases (like mySql, Oracle), Web Servers (tomcat etc)

`SAAS (Software As A Service)` :

A layer on top on PAAS
Applications like email (Gmail, Yahoo mail etc), Social Networking sites (Facebook etc)

正好在微博上看到 @[老刀IBM](http://weibo.com/1586108233/B3bGwpDKJ) 分享的一个三者关系图：

![IAAS vs PAAS vs SaaS](https://tankywoo-wb.b0.upaiyun.com/iaas_paas_saas.jpg!small)

`LXC` -- LinuX Container

借用[网上](http://segmentfault.com/a/1190000000366923)的解释:

> Docker 提供了一个可以运行你的应用程序的封套(envelope)，或者说容器。它原本是 dotCloud 启动的一个业余项目，并在前些时候开源了。它吸引了大量的关注和讨论，导致 dotCloud 把它重命名到 Docker Inc。它最初是用 Go 语言编写的，它就相当于是加在 LXC（LinuX Containers，linux 容器）上的管道，允许开发者在更高层次的概念上工作。
> 
> Docker 扩展了 Linux 容器（Linux Containers），或着说 LXC，通过一个高层次的 API 为进程单独提供了一个轻量级的虚拟环境。Docker 利用了 LXC， cgroups 和 Linux 自己的内核。和传统的虚拟机不同的是，一个 Docker 容器并不包含一个单独的操作系统，而是基于已有的基础设施中操作系统提供的功能来运行的。这里有一个 Stackoverflow 的答案，里面非常详细清晰地描述了所有 Docker 不同于纯粹的 LXC 的功能特性
> 
> Docker 会像一个可移植的容器引擎那样工作。它把应用程序及所有程序的依赖环境打包到一个虚拟容器中，这个虚拟容器可以运行在任何一种 Linux 服务器上。这大大地提高了程序运行的灵活性和可移植性，无论需不需要许可、是在公共云还是私密云、是不是裸机环境等等。


更多关于Docker，看看官方的[Learn More](https://www.docker.io/learn_more/)

## Docker的常见使用场景 ##

* Automating the packaging and deployment of applications
* Creation of lightweight, private PAAS environments
* Automated testing and continuous integration/deployment
* Deploying and scaling web apps, databases and backend services

> Please note Docker is currently under heavy development. It should not be used in production (yet).

如上提到，Docker还在开发中，**暂时还不应该用于线上产品中**。


## Interactive commandline tutorial ##

使用[Interactive commandline tutorial](https://www.docker.io/gettingstarted/#)入门，点击Start进入交互式命令行教程，直接在线交互，不需要本地安装Docker。

这个教程非常好，一定要在线使用一遍。且Docker的官方源在国内偶尔被墙，折腾起来很麻烦，所以在线学习就没这些麻烦的事情了。

### Getting Started ###

Docker包含两个程序，一个服务端，一个客户端，服务端用来管理所有容器，客户端用来控制服务端守护进程。在大部分系统，服务端和守护端都运行在同一台机器上。

查看docker 版本:

	you@tutorial:~$ docker version
	Docker Emulator version 0.1.3
	 
	Emulating:
	Client version: 0.5.3
	Server version: 0.5.3
	Go version: go1.1

线上的显示比较简单，且版本较老(0.5.3)，本地(Ubuntu12.04)下安装的，版本较新(0.10.0)。可以看到这里有 `Client version`  和 `Server version`。

	root@tankywoo-docker:~# docker version
	Client version: 0.10.0
	Client API version: 1.10
	Go version (client): go1.2.1
	Git commit (client): dc9c28f
	Server version: 0.10.0
	Server API version: 1.10
	Git commit (server): dc9c28f
	Go version (server): go1.2.1

	Last stable version: 0.10.0

思考下这里为何会显示 `Git commit` 和 `Go version` ? 

这里的Git commit是0.10.0这个release的commit id: [docker releases](_posts/2014-05-08-docker-4-summary.markdown)

因为docker是Go写的，这里应该是开发Docker使用的Go版本 ** TODO **

### Searching for images ###

最简单的方式就是通过其它地方获取容器镜像(container image)来使用。`Docker index` 是一个存放镜像的地方，可以在 <https://index.docker.io> 上看到已经有的镜像，且可以通过命令行来获取。

这里搜索一个叫 tutorial的镜像:

	you@tutorial:~$ docker search tutorial
	Found 1 results matching your query ("tutorial")
	NAME                      DESCRIPTION
	learn/tutorial            An image for the interactive tutorial

再比如本地搜索 ubuntu 镜像:

	you@tutorial:~$ docker search ubuntu
	Found 22 results matching your query ("ubuntu")
	NAME                DESCRIPTION
	shykes/ubuntu
	base                Another general use Ubuntu base image. Tag...
	ubuntu              General use Ubuntu base image. Tags availa...
	boxcar/raring       Ubuntu Raring 13.04 suitable for testing v...
	dhrp/ubuntu
	creack/ubuntu       Tags:
	12.04-ssh,
	12.10-ssh,
	12.10-ssh-l...
	crohr/ubuntu              Ubuntu base images. Only lucid (10.04) for...
	knewton/ubuntu
	pallet/ubuntu2
	erikh/ubuntu
	samalba/wget              Test container inherited from ubuntu with ...
	creack/ubuntu-12-10-ssh
	knewton/ubuntu-12.04
	tithonium/rvm-ubuntu      The base 'ubuntu' image, with rvm installe...
	dekz/build                13.04 ubuntu with build
	ooyala/test-ubuntu
	ooyala/test-my-ubuntu
	ooyala/test-ubuntu2
	ooyala/test-ubuntu3
	ooyala/test-ubuntu4
	ooyala/test-ubuntu5
	surma/go                  Simple augmentation of the standard Ubuntu...

### Downloading container images ###

容器镜像可以通过`docker pull`命令来下载，来自docker index的镜像，可以通过指定 `<username>/<repository>` 的方式来下载镜像。如果是官方信任的镜像，例如ubuntu，可以不用指定username，直接指定仓库名下载。

可以看出来，docker的方式和git非常像。

	you@tutorial:~$ docker pull learn/tutorial
	Pulling repository learn/tutorial from https://index.docker.io/v1
	Pulling image 8dbd9e392a964056420e5d58ca5cc376ef18e2de93b5cc90e868a1bbc8318c1c (precise) from ubuntu
	Pulling image b750fe79269d2ec9a3c593ef05b4332b1d1a02a62b4accb2c21d589ff2f5f2dc (12.10) from ubuntu
	Pulling image 27cf784147099545 () from tutorial

### Hello world from a container ###

> You can think about containers as a process in a box. The box contains everything the process might need, so it has the filesystem, system libraries, shell and such, but by default none of it is started or run.
> You 'start' a container by running a process in it. This process is the only process run, so when it completes the container is fully stopped.

使用`docker run`来在容器中执行命令，它最少有两个参数，一个是容器名，一个是要执行的操作。

	you@tutorial:~$ docker run learn/tutorial echo 'hello world'
	'hello world' 

### Installing things in the container ###

下面来测试安装ping工具。

因为这里是`非交互模式` 指定命令，所以要带上参数`-y`表示确认(yes)，否则会在等待accept (y/n) 时就退出了。

	you@tutorial:~$ docker run learn/tutorial apt-get install -y ping
	Reading package lists...
	Building dependency tree...
	The following NEW packages will be installed:
	  iputils-ping
	0 upgraded, 1 newly installed, 0 to remove and 0 not upgraded.
	Need to get 56.1 kB of archives.
	After this operation, 143 kB of additional disk space will be used.
	Get:1 http://archive.ubuntu.com/ubuntu/ precise/main iputils-ping amd64 3:20101006-1ubuntu1 [56.1 kB]
	debconf: delaying package configuration, since apt-utils is not installed
	Fetched 56.1 kB in 1s (50.3 kB/s)
	Selecting previously unselected package iputils-ping.
	(Reading database ... 7545 files and directories currently installed.)
	Unpacking iputils-ping (from .../iputils-ping_3%3a20101006-1ubuntu1_amd64.deb) ...
	Setting up iputils-ping (3:20101006-1ubuntu1) ...

### Save your changes ###

当作了一些操作/改动(如在container里执行命令)，可以保存这次的状态。这个称为committing(提交)。提交会保存和老镜像的差异以及新的状态。

先使用 `docker ps -l` 来找到 `container id`，然后可以通过这个container id和仓库名来保存(commit)

	you@tutorial:~$ docker ps -l
	ID                  IMAGE               COMMAND                CREATED             STATUS              PORTS
	6982a9948422        ubuntu:12.04        apt-get install ping   1 minute ago        Exit 0

直接执行 docker commit 可以看到有哪些参数

	you@tutorial:~$ docker commit
	Usage: Docker commit [OPTIONS] CONTAINER [REPOSITORY [TAG]]
	 
	Create a new image from a container's changes
	 
	  -author="": Author (eg. "John Hannibal Smith <hannibal@a-team.com>"
	  -m="": Commit message
	  -run="": Config automatically applied when the image is run. (ex: {"Cmd": ["cat", "/world"], "PortSpecs": ["22"
	]}')

不需要写出全部的id, 一般只需要前三位或前四位就行

这里的 learn/ping 就是commit新建的image name:

	you@tutorial:~$ docker commit 698 learn/ping
	effb66b31edb

### Run your new image ###

现在可以在新的仓库里执行ping命令:

	you@tutorial:~$ docker run learn/ping ping www.google.com
	PING www.google.com (74.125.239.129) 56(84) bytes of data.
	64 bytes from nuq05s02-in-f20.1e100.net (74.125.239.148): icmp_req=1 ttl=55 time=2.23 ms
	64 bytes from nuq05s02-in-f20.1e100.net (74.125.239.148): icmp_req=2 ttl=55 time=2.30 ms
	64 bytes from nuq05s02-in-f20.1e100.net (74.125.239.148): icmp_req=3 ttl=55 time=2.27 ms
	64 bytes from nuq05s02-in-f20.1e100.net (74.125.239.148): icmp_req=4 ttl=55 time=2.30 ms
	64 bytes from nuq05s02-in-f20.1e100.net (74.125.239.148): icmp_req=5 ttl=55 time=2.25 ms
	64 bytes from nuq05s02-in-f20.1e100.net (74.125.239.148): icmp_req=6 ttl=55 time=2.29 ms
	64 bytes from nuq05s02-in-f20.1e100.net (74.125.239.148): icmp_req=7 ttl=55 time=2.23 ms
	64 bytes from nuq05s02-in-f20.1e100.net (74.125.239.148): icmp_req=8 ttl=55 time=2.30 ms
	64 bytes from nuq05s02-in-f20.1e100.net (74.125.239.148): icmp_req=9 ttl=55 time=2.35 ms
	-> This would normally just keep going. However, this emulator does not support Ctrl-C, so we quit here.

### Check your running image ###

现在有一个正在运行的容器，可以通过 `docker ps` 看到所有运行中的容器:

	you@tutorial:~$ docker ps
	ID                  IMAGE               COMMAND               CREATED             STATUS              PORTS
	efefdc74a1d5        learn/ping:latest   ping www.google.com   37 seconds ago      Up 36 seconds

可以通过 `docker inspect` 指定container id来查看相应容器的信息:

	you@tutorial:~$ docker inspect efe
	[2013/07/30 01:52:26 GET /v1.3/containers/efef/json
	{
	  "ID": "efefdc74a1d5900d7d7a74740e5261c09f5f42b6dae58ded6a1fde1cde7f4ac5",
	  "Created": "2013-07-30T00:54:12.417119736Z",
	  "Path": "ping",
	  "Args": [
		  "www.google.com"
	  ],
	  "Config": {
		  "Hostname": "efefdc74a1d5",
		  "User": "",
		  "Memory": 0,
		  "MemorySwap": 0,
		  "CpuShares": 0,
		  "AttachStdin": false,
		  "AttachStdout": true,
		  "AttachStderr": true,
		  "PortSpecs": null,
		  "Tty": false,
		  "OpenStdin": false,
		  "StdinOnce": false,
		  "Env": null,
		  "Cmd": [
			  "ping",
			  "www.google.com"
		  ],
		  "Dns": null,
		  "Image": "learn/ping",
		  "Volumes": null,
		  "VolumesFrom": "",
		  "Entrypoint": null
	  },
	  "State": {
		  "Running": true,
		  "Pid": 22249,
		  "ExitCode": 0,
		  "StartedAt": "2013-07-30T00:54:12.424817715Z",
		  "Ghost": false
	  },
	  "Image": "a1dbb48ce764c6651f5af98b46ed052a5f751233d731b645a6c57f91a4cb7158",
	  "NetworkSettings": {
		  "IPAddress": "172.16.42.6",
		  "IPPrefixLen": 24,
		  "Gateway": "172.16.42.1",
		  "Bridge": "docker0",
		  "PortMapping": {
			  "Tcp": {},
			  "Udp": {}
		  }
	  },
	  "SysInitPath": "/usr/bin/docker",
	  "ResolvConfPath": "/etc/resolv.conf",
	  "Volumes": {},
	  "VolumesRW": {}

### Push your image to the index

把容器推送到远端:

	you@tutorial:~$ docker push learn/ping


## 安装 ##

Docker的安装很简单，直接阅读官方的[安装文档](https://www.docker.io/gettingstarted/#h_installation)。

> Our recommended installation path is for Ubuntu linux, because we develop Docker on Ubuntu and our installation package will do most of the work for you.

官方的Docker开发都是在Ubuntu下进行的，所以也推荐使用Ubuntu。

另外Docker要求的内核最低是`3.8`，所以最好高于这个版本，安装完可以用官网的一个脚本检测下看内核配置是否都开启了:

<https://raw.githubusercontent.com/dotcloud/docker/master/contrib/check-config.sh>

之前在Gentoo 3.7内核下安装，然后Docker就使用不了，[这是](https://github.com/dotcloud/docker/issues/5590)他们的解释

直接执行进入ubuntu的交互模式，会查看本地是否有镜像，如果没有会自动下载。

	root@tankywoo-docker:~# docker run -i -t ubuntu /bin/bash
	Unable to find image 'ubuntu' locally
	Pulling repository ubuntu
	316b678ddf48: Download complete
	99ec81b80c55: Download complete
	3db9c44f4520: Download complete
	5e019ab7bf6d: Download complete
	a7cf8ae4e998: Download complete
	74fe38d11401: Download complete
	511136ea3c5a: Download complete
	6cfa4d1f33fb: Download complete
	f10ebce2c0e1: Download complete
	ef519c9ee91a: Download complete
	e2aa6665d371: Download complete
	02dae1c13f51: Download complete
	5e66087f3ffe: Download complete
	82cdea7ab5b5: Download complete
	5dbd9cb5a02f: Download complete
	f0ee64c4df74: Download complete
	2209cbf9dcd3: Download complete
	e7206bfc66aa: Download complete
	cb12405ee8fa: Download complete
	07302703becc: Download complete
	cf8dc907452c: Download complete
	4d26dd3ebc1c: Download complete
	d4010efcfd86: Download complete

也可以使用 `docker pull ubuntu` 来下载

查看本地的镜像:

	root@tankywoo-docker:~# docker images
	REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
	ubuntu              13.10               5e019ab7bf6d        11 days ago         180 MB
	ubuntu              saucy               5e019ab7bf6d        11 days ago         180 MB
	ubuntu              12.04               74fe38d11401        11 days ago         209.6 MB
	ubuntu              precise             74fe38d11401        11 days ago         209.6 MB
	ubuntu              12.10               a7cf8ae4e998        11 days ago         171.3 MB
	ubuntu              quantal             a7cf8ae4e998        11 days ago         171.3 MB
	ubuntu              14.04               99ec81b80c55        11 days ago         266 MB
	ubuntu              latest              99ec81b80c55        11 days ago         266 MB
	ubuntu              trusty              99ec81b80c55        11 days ago         266 MB
	ubuntu              13.04               316b678ddf48        11 days ago         169.4 MB
	ubuntu              raring              316b678ddf48        11 days ago         169.4 MB
	<none>              <none>              7fe668a14603        11 days ago         447.7 MB
	ubuntu              10.04               3db9c44f4520        2 weeks ago         183 MB
	ubuntu              lucid               3db9c44f4520        2 weeks ago         183 MB
	<none>              <none>              fd31b814cbc1        4 weeks ago         166.6 MB
	<none>              <none>              1c7f181e78b9        3 months ago        0 B
	<none>              <none>              0b520d776e7d        3 months ago        466.5 MB
	<none>              <none>              873f518b98ef        3 months ago        466.4 MB
	<none>              <none>              e8e5377f8307        3 months ago        466.2 MB
	<none>              <none>              fd1184b81ee4        3 months ago        400.2 MB

查看相关的信息:

	root@tankywoo-docker:~# docker info
	Containers: 1
	Images: 23
	Storage Driver: aufs
	 Root Dir: /var/lib/docker/aufs
	  Dirs: 25
	  Execution Driver: native-0.1
	  Kernel Version: 3.8.0-25-generic
	  WARNING: No swap limit support
