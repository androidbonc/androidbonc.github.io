---
layout: post
title: "Docker 2 -- 关于Dockerfile"
date: 2014-05-08 15:30
categories: Docker
---

Dockerfile是一个镜像的表示，可以通过Dockerfile来描述构建镜像的步骤，并自动构建一个容器

所有的 Dockerfile 命令格式都是:

	INSTRUCTION arguments

虽然指令忽略大小写，但是**建议使用大写**。

### FROM 命令 ###

	FROM <image>

或

	FROM <image>:<tag>

这个设置基本的镜像，为后续的命令使用，所以应该作为Dockerfile的第一条指令。

比如:

	FROM ubuntu

如果没有指定 `tag` ，则默认tag是`latest`，如果都没有则会报错。

### RUN 命令 ###

RUN命令会在上面`FROM`指定的镜像里执行任何命令，然后提交(commit)结果，提交的镜像会在后面继续用到。

两种格式:

	RUN <command> (the command is run in a shell - `/bin/sh -c`)

或:

	RUN ["executable", "param1", "param2" ... ]  (exec form)

RUN命令等价于:

	docker run image command
	docker commit container_id


### 注释 ###

使用 `#` 作为注释

如:

	# Memcached
	#
	# VERSION       1.0

	# use the ubuntu base image provided by dotCloud
	FROM ubuntu

	# make sure the package repository is up to date
	RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
	RUN apt-get update

	# install memcached
	RUN apt-get install -y memcached

### MAINTAINER 命令 ###

	MAINTAINER <name>

MAINTAINER命令用来指定维护者的姓名和联系方式

如:

	MAINTAINER Guillaume J. Charmes, guillaume@dotcloud.com

### ENTRYPOINT 命令 ###

有两种语法格式，一种就是上面的(shell方式):

	ENTRYPOINT cmd param1 param2 ...

第二种是 `exec` 格式:

	ENTRYPOINT ["cmd", "param1", "param2"...]

如:

	ENTRYPOINT ["echo", "Whale you be my container"]

ENTRYPOINT 命令设置在容器启动时执行命令

	root@tankywoo-docker:~# cat Dockerfile
	FROM ubuntu
	ENTRYPOINT echo "Welcome!"

	root@tankywoo-docker:~# docker run 62fda5e450d5
	Welcome!


### USER 命令 ###

比如指定 memcached 的运行用户，可以使用上面的 `ENTRYPOINT` 来实现:

	ENTRYPOINT ["memcached", "-u", "daemon"]

更好的方式是：

	ENTRYPOINT ["memcached"]
	USER daemon

### EXPOSE 命令 ###

EXPOSE 命令可以设置一个端口在运行的镜像中暴露在外

	EXPOSE <port> [<port>...]

比如memcached使用端口 11211，可以把这个端口暴露在外，这样容器外可以看到这个端口并与其通信。

	EXPOSE 11211

一个完整的例子:

	# Memcached
	#
	# VERSION       2.2
	
	# use the ubuntu base image provided by dotCloud
	FROM ubuntu
	
	MAINTAINER Victor Coisne victor.coisne@dotcloud.com
	
	# make sure the package repository is up to date
	RUN echo "deb http://archive.ubuntu.com/ubuntu precise main universe" > /etc/apt/sources.list
	RUN apt-get update
	
	# install memcached
	RUN apt-get install -y memcached
	
	# Launch memcached when launching the container
	ENTRYPOINT ["memcached"]
	
	# run memcached as the daemon user
	USER daemon
	
	# expose memcached port
	EXPOSE 11211

上面是官方例子，国内建议换成163或sohu的源，不然太慢了。

	root@tankywoo-docker:~# docker build -t tankywoo  - < dck                       [38/480]
	Uploading context  2.56 kB
	Uploading context
	Step 0 : FROM ubuntu
	 ---> 99ec81b80c55
	Step 1 : MAINTAINER Victor Coisne victor.coisne@dotcloud.com
	 ---> Using cache
	 ---> 2b58110877f6
	Step 2 : RUN echo "deb http://mirrors.163.com/ubuntu/ precise main restricted universe multiverse" > /etc/apt/sources.list
	 ---> Running in f55a4a8bb069
	 ---> d48c6a965398
	Step 3 : RUN apt-get update
	 ---> Running in da091a1dd6e7
	Ign http://mirrors.163.com precise InRelease
	Get:1 http://mirrors.163.com precise Release.gpg [198 B]

	....

	Processing triggers for libc-bin (2.19-0ubuntu6) ...
	Processing triggers for ureadahead (0.100.0-16) ...
	 ---> 2886671b5b86
	Step 5 : ENTRYPOINT ["memcached"]
	 ---> Running in e8aeeab92cb6
	 ---> 7148293a4053
	Step 6 : USER daemon
	 ---> Running in 288766b19606
	 ---> 235e7f630ffa
	Step 7 : EXPOSE 11211
	 ---> Running in c6f881b9d51f
	 ---> 666c5d65f396
	Successfully built 666c5d65f396
	Removing intermediate container f55a4a8bb069
	Removing intermediate container da091a1dd6e7
	Removing intermediate container f23631d3d45a
	Removing intermediate container e8aeeab92cb6
	Removing intermediate container 288766b19606
	Removing intermediate container c6f881b9d51f

### ENV 命令 ###

用于设置环境变量

	ENV <key> <value>

设置了后，后续的`RUN`命令都可以使用

使用此dockerfile生成的image新建container，可以通过 `docker inspect` 看到这个环境变量:

	root@tankywoo-docker:~# docker inspect 49bfc7a9817f
		...
		"Env": [
			"name=tanky",
			"HOME=/",
			"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
		],
		...

里面的name=tanky就是设置的。

也可以通过在docker run时设置或修改环境变量:

	docker run -i -t --env name="tanky" ubuntu:newtest /bin/bash

### ADD 命令 ###

从src复制文件到container的dest路径:

	ADD <src> <dest>

* `<src>` 是相对被构建的源目录的`相对路径`，可以是文件或目录的路径，也可以是一个远程的文件url
* `<dest>` 是container中的`绝对路径`


### VOLUME 命令 ###

	VOLUME ["<mountpoint>"]

如:

	VOLUME ["/data"]

创建一个挂载点用于共享目录

具体参考 [Docker 4 -- 总结]({{ site.baseurl  }}{% post_url 2014-05-08-docker-4-summary %})

### WORKDIR 命令 ###

	WORKDIR /path/to/workdir

配置`RUN`, `CMD`, `ENTRYPOINT` 命令设置当前工作路径

可以设置多次，如果是相对路径，则相对前一个 WORKDIR 命令

比如:

	WORKDIR /a WORKDIR b WORKDIR c RUN pwd

其实是在 /a/b/c 下执行 pwd

### CMD 命令 ###

有三种格式:

* `CMD ["executable","param1","param2"]` (like an exec, preferred form)
* `CMD ["param1","param2"]` (as default parameters to ENTRYPOINT)
* `CMD command param1 param2` (as a shell)

一个Dockerfile里只能有一个`CMD`，如果有多个，只有最后一个生效。

> The main purpose of a CMD is to provide defaults for an executing container. These defaults can include an executable, or they can omit the executable, in which case you must specify an ENTRYPOINT as well.

TODO 还没搞清楚这个的作用

### ONBUILD ###

TODO

总结一下，基本常用的命令是: `FROM`, `MAINTAINER`, `RUN`, `ENTRYPOINT`, `USER`, `PORT`, `ADD`

## 一些例子 ##

* [docker-wordpress-nginx](https://github.com/eugeneware/docker-wordpress-nginx)  A Dockerfile that installs the latest wordpress, nginx and php-fpm.
* [rails-meets-docker](https://github.com/gemnasium/rails-meets-docker)  

## 参考 ##

* [Dockerfile tutorial](https://www.docker.io/learn/dockerfile/)
* [Docker - Reference - Dockerfile](http://docs.docker.io/reference/builder/)
