---
layout: post
title: "Docker 3 -- 自建Docker Registry"
date: 2014-05-08 15:30
categories: Docker
---

官方在Github上有一个项目 [docker-registry](https://github.com/dotcloud/docker-registry), 专门用于自建Docker的Registry。

上面的README讲得很详细

简单的在dev模式下跑起来:

首先将项目clone下来，然后进入docker-registry，复制一份配置文件出来:

	cp config/config_sample.yml config/config.yml

修改`dev:`字段下的配置，主要是配置 `storage_path` ，此为docker images等存放路径。

运行 Registry:

在Ubuntu下老的方式是:

先安装一些依赖

	sudo apt-get install build-essential python-dev libevent-dev python-pip libssl-dev liblzma-dev libffi-dev
	sudo pip install .

然后运行

	gunicorn --access-logfile - --debug -k gevent -b 0.0.0.0:5000 -w 1 docker_registry.wsgi:application

新的运行方式:

	docker run -p 5000:5000 registry

后者我至今还没成功，一直卡着：

	root@tankywoo-docker:~/docker-registry-master# docker run -p 5000:5000 registry
	Unable to find image 'registry' locally
	Pulling repository registry
	e260f5a77e52: Pulling dependent layers
	873f518b98ef: Pulling dependent layers
	0b520d776e7d: Pulling dependent layers
	e8e5377f8307: Pulling dependent layers
	b04ace768d59: Pulling dependent layers
	1f7bbd131cd8: Pulling dependent layers
	7fe668a14603: Pulling dependent layers
	2930bc3d8f1e: Pulling image (latest) from registry, endpoint: https://cdn-registry-1.docker.io/v1/
	9f98cb899f46: Pulling dependent layers
	e7bac0a3804b: Pulling dependent layers
	511136ea3c5a: Download complete
	46e4dee27895: Download complete
	0e5997dad26c: Pulling metadata

使用前者，会在本地打开5000端口监听，访问可以看到:

![registry success](https://tankywoo-wb.b0.upaiyun.com/docker-registry.png!small)

	root@tankywoo-docker:~/docker-registry-master# docker images
	REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
	ubuntu              newtest             276cc641e40e        23 hours ago        388.3 MB

Tag to create a repository with the full registry location.

	root@tankywoo-docker:~/docker-registry-master# docker tag 276cc641e40e 10.2.15.190:5000/tankywoo
	root@tankywoo-docker:~/docker-registry-master# docker images
	REPOSITORY              TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
	ubuntu                  newtest             276cc641e40e        23 hours ago        388.3 MB
	10.2.15.190:5000/tankywoo   latest              276cc641e40e        23 hours ago        388.3 MB

然后push上去:

	root@tankywoo-docker:~/docker-registry-master# docker push 10.2.15.190:5000/tankywoo
	The push refers to a repository [10.2.15.190:5000/tankywoo] (len: 1)
		Sending image list
		Pushing repository 10.2.15.190:5000/tankywoo (1 tags)
		Image 511136ea3c5a already pushed, skipping
		Image f10ebce2c0e1 already pushed, skipping
		Image 82cdea7ab5b5 already pushed, skipping
		Image 5dbd9cb5a02f already pushed, skipping
		Image 74fe38d11401 already pushed, skipping
		Image fe65a2781dae already pushed, skipping
		Image 276cc641e40e already pushed, skipping
		Pushing tag for rev [276cc641e40e] on {http://10.2.15.190:5000/v1/repositories/tankywoo/tags/latest}

然后看看 mydocker目录下:

	root@tankywoo-docker:~/mydocker# find .                               [11/112]
	.
	./images
	./images/82cdea7ab5b555f53c2adf8df75b0d2ad1e49dbfc11da50df3e7ea38454ed606
	./images/82cdea7ab5b555f53c2adf8df75b0d2ad1e49dbfc11da50df3e7ea38454ed606/ancestry
	./images/82cdea7ab5b555f53c2adf8df75b0d2ad1e49dbfc11da50df3e7ea38454ed606/_checksum
	./images/82cdea7ab5b555f53c2adf8df75b0d2ad1e49dbfc11da50df3e7ea38454ed606/layer
	./images/82cdea7ab5b555f53c2adf8df75b0d2ad1e49dbfc11da50df3e7ea38454ed606/json
	./images/fe65a2781daea01c67c33f11868abe6d510833bca07b90fc681cdfe98a9196ac
	./images/fe65a2781daea01c67c33f11868abe6d510833bca07b90fc681cdfe98a9196ac/ancestry
	./images/fe65a2781daea01c67c33f11868abe6d510833bca07b90fc681cdfe98a9196ac/_checksum
	./images/fe65a2781daea01c67c33f11868abe6d510833bca07b90fc681cdfe98a9196ac/layer
	./images/fe65a2781daea01c67c33f11868abe6d510833bca07b90fc681cdfe98a9196ac/json
	...
	./repositories
	./repositories/library
	./repositories/library/tankywoo
	./repositories/library/tankywoo/_index_images
	./repositories/library/tankywoo/taglatest_json
	./repositories/library/tankywoo/json
	./repositories/library/tankywoo/tag_latest

已经有相关文件了

TODO 剩下的还得继续研究

* [HOW TO USE YOUR OWN REGISTRY](http://blog.docker.io/2013/07/how-to-use-your-own-registry/) 官方博客
* [Deploying your own Private Docker Registry](http://www.activestate.com/blog/2014/01/deploying-your-own-private-docker-registry)
