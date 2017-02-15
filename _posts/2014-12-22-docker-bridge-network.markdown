---
layout: post
title: "Docker 网络桥接"
date: 2014-12-22 13:40
---

首先本地安装`bridge-utils`工具，这是一个管理网络桥接的工具:

	sudo apt-get install bridge-utils

使用的工具是`brctl`

## 默认nat网络 ##

默认 docker continer 的网络是走的 `nat`. 一般选择的是 `172.17.0.0/16` 段，大部分情况下这个内网网段未使用.

另外启动docker时，会修改`ip_forward`为1. 也可以手动确认下:

	sysctl net.ipv4.ip_forward

启动 docker 时会在宿主机的 `nat表` 和 `filter表` 自动添加一些规则:

	$ iptables -t nat -L -nv
	Chain PREROUTING (policy ACCEPT 22 packets, 1530 bytes)
	 pkts bytes target     prot opt in     out     source               destination
		0     0 DOCKER     all  --  *      *       0.0.0.0/0            0.0.0.0/0            ADDRTYPE match dst-type LOCAL

	Chain INPUT (policy ACCEPT 0 packets, 0 bytes)
	 pkts bytes target     prot opt in     out     source               destination

	Chain OUTPUT (policy ACCEPT 0 packets, 0 bytes)
	 pkts bytes target     prot opt in     out     source               destination
		0     0 DOCKER     all  --  *      *       0.0.0.0/0           !127.0.0.0/8          ADDRTYPE match dst-type LOCAL

	Chain POSTROUTING (policy ACCEPT 22 packets, 1530 bytes)
	 pkts bytes target     prot opt in     out     source               destination
		0     0 MASQUERADE  all  --  *      !docker0  172.17.0.0/16        0.0.0.0/0

	Chain DOCKER (2 references)
	 pkts bytes target     prot opt in     out     source               destination

	$ iptables -L -nv
	Chain FORWARD (policy DROP 0 packets, 0 bytes)
	 pkts bytes target     prot opt in     out     source               destination
		0     0 ACCEPT     all  --  *      docker0  0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED
		0     0 ACCEPT     all  --  docker0 !docker0  0.0.0.0/0            0.0.0.0/0
		0     0 ACCEPT     all  --  docker0 docker0  0.0.0.0/0            0.0.0.0/0

这种默认的网络配置可以让用户无需关心docker网络

在宿主机上使用 `ip addr` 可以看到网络:

	$ ip addr
	1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN
		link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
		inet 127.0.0.1/8 scope host lo
		   valid_lft forever preferred_lft forever
		inet6 ::1/128 scope host
		   valid_lft forever preferred_lft forever
	2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP qlen 1000
		link/ether d4:ae:52:c8:13:58 brd ff:ff:ff:ff:ff:ff
		inet 10.8.255.181/24 brd 10.8.255.255 scope global eth0
		   valid_lft forever preferred_lft forever
	3: eth1: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN qlen 1000
		link/ether d4:ae:52:c8:13:59 brd ff:ff:ff:ff:ff:ff
	4: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN
		link/ether 56:84:7a:fe:91:99 brd ff:ff:ff:ff:ff:ff
		inet 172.17.42.1/16 scope global docker0
		   valid_lft forever preferred_lft forever

可以看到`docker0`, 这个是docker启动时在宿主机上创建的虚拟网卡, 用来管理docker container的网络

使用`brctl show`可以看到虚拟机的网络关系:

	$ brctl show
	bridge name     bridge id               STP enabled     interfaces
	docker0         8000.56847afe9799       no              veth7a3b118

其中`veth7a3b118`是docker container的虚拟网卡， docker每新建一个container, `docker0`就会创建一个新的虚拟网卡，名称以`veth`开头，其余是随机的. 

在container上实际看到的是eth0这些.

container上的eth0 和 宿主机上的veth7a3b118 类似一个 PIPE.


在这种情况下, 发现**可以ping通外网，但是ping不通同网段内网**.

抓包排查后发现是 `raw`表的 `CT notrack` 导致, 除非去掉规则的这些规则，但是这样容易导致`conntrack`表满.

> CT  
>    The CT target allows to set parameters for a packet or its associated connection. The target attaches a "template" connection tracking entry to the packet, which is then used by the conntrack core when initializing a new ct  entry.  This target is thus only valid in the "raw" table.
> 
>   --notrack  
>       Disables connection tracking for this packet.

来至[Docker - Network Configuration](https://docs.docker.com/articles/networking/)的一段话:

> `docker0` is no ordinary interface.
> It is a virtual Ethernet bridge that automatically forwards packets between any other network interfaces that are attached to it. 
> This lets containers communicate both with the host machine and with each other.
> Every time Docker creates a container, it creates a pair of “peer” interfaces that are like opposite ends of a pipe — a packet sent on one will be received on the other.
> It gives one of the peers to the container to become its eth0 interface and keeps the other peer, with a unique name like vethAQI2QT, out in the namespace of the host machine.
> By binding every `veth*` interface to the docker0 bridge, Docker creates a virtual subnet shared between the host machine and every Docker container.

## 改桥接网络 ##

尝试使用docker的桥接来解决这个问题.

将原来eth0的网络配置留空改为手动, 然后配置一个新的桥接网卡br0:

	$ more /etc/network/interfaces
	auto lo
	iface lo inet loopback

	#auto eth0
	#iface eth0 inet static
	#       address 10.8.255.181/255.255.255.0
	#       gateway 10.8.255.1

	auto eth0
	iface eth0 inet manual

	auto br0
	iface br0 inet static
			address 10.8.255.181/255.255.255.0
			gateway 10.8.255.1
			bridge_ports eth0
			bridge_stp off

新建了一个 `br0` 的桥接虚拟网卡.

然后将原来的`eth0`加入这个桥接中

重启网络.

以上也可以手动来操作:

	brctl addbr br0  # 新建一个桥接虚拟网卡
	ip link set br0 up
	ip addr add 10.8.255.181/24 dev br0
	ip addr del 10.8.255.181/24 dev eth0
	brctl addif br0 eth0   # 将eth0加入到br0
	ip route del default
	ip route add default via 10.8.255.1 dev br0

然后以`--privileged=true`的方式启动一个container. 因为默认情况下是false, 没有一些特权, 如修改网络的路由等.

使用[pippework](https://github.com/jpetazzo/pipework)工具建立宿主与container的桥接网络

	pipework br0 $CONTAINER_ID 10.8.255.183/24

手动分配给虚拟机一个和宿主机同网段的ip

pipework 是一个LXC的网络管理工具，封装了一些复杂的命令，使操作变得简单容易.

直接从github上clone下来，将脚本cp到`$PATH`下, 如`/usr/loca/bin`下.

另外里面用到了`arping`，如果没有则需要安装.

这时container上就会有两个网卡eth0和eth1, eth0是172.17段的一个随机ip, eth1是上面配置的10.8.255.183.

用`brctl show` 可以看到:

	$ brctl show
	bridge name     bridge id               STP enabled     interfaces
	br0             8000.42d1f01a84ce       no              eth0
															veth1pl6171
	docker0         8000.56847afe9799       no              veth31b66dd

默认路由是eth0的172.17段, 手动删除改为走10.8.255.1:

	ip route del default
	ip rotue add default via 10.8.255.1 dev eth1

这时按理来说网络应该是通了，container也可以ping通内外网. 但是实际没有, 排查发现线上iptables规则filter表`FORWARD链`的默认策略是`DROP`.

因为`docker0`口是自动控制网络，已经添加了相关的规则，`br0`也可以参照添加规则:

	*filter
	:FORWARD DROP [0:0]
	:INPUT ACCEPT [0:0]
	:OUTPUT ACCEPT [0:0]
	# other rules...
	[0:0] -A FORWARD -o br0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
	[0:0] -A FORWARD -i br0 ! -o br0 -j ACCEPT
	[0:0] -A FORWARD -i br0 -o br0 -j ACCEPT

显示效果:

	Chain FORWARD (policy DROP 0 packets, 0 bytes)
	 pkts bytes target     prot opt in     out     source               destination
		0     0 ACCEPT     all  --  *      docker0  0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED
		0     0 ACCEPT     all  --  docker0 !docker0  0.0.0.0/0            0.0.0.0/0
		0     0 ACCEPT     all  --  docker0 docker0  0.0.0.0/0            0.0.0.0/0
		0     0 ACCEPT     all  --  *      br0     0.0.0.0/0            0.0.0.0/0            ctstate RELATED,ESTABLISHED
		0     0 ACCEPT     all  --  br0    !br0    0.0.0.0/0            0.0.0.0/0
		0     0 ACCEPT     all  --  br0    br0     0.0.0.0/0            0.0.0.0/0

这样网络就OK了.

## 继续改进 ##

修改`/etc/default/docker`修改默认的桥接网络为br0:

	$ more /etc/default/docker
	DOCKER_OPTS="-b=br0"

删掉docker0:

	$ service docker stop
	docker stop/waiting
	$ ip link set docker0 down
	$ brctl delbr docker0
	$ service docker start

启动container, 这时eth0就是和宿主一个网段的ip.

但是这个ip是docker br0自动给container分配的.

如果不想让其配置网络，可以在`docker run`时指定`--net=none`:

	docker run -i -t --net=none --privileged=true ubuntu /bin/bash

然后使用pipework创建container网络:

	pipework br0 $CONTAINER_ID 10.8.255.183

这时container创建的是eth1, 可以指定container创建的网卡名:

	pipework br0 -i eth0 $CONTAINER_ID 10.8.255.183

最后再在container中加一条默认路由就可以了

## 参考 ##

* [Docker - Network Configuration](https://docs.docker.com/articles/networking/)
* [FOUR WAYS TO CONNECT A DOCKER CONTAINER TO A LOCAL NETWORK](http://blog.oddbit.com/2014/08/11/four-ways-to-connect-a-docker/)
* [使用pipework桥接docker](http://kumu-linux.github.io/blog/2014/06/04/docker-pipework/)
* [docker 实战---多台物理主机的联网，容器桥接到物理网络(三）](http://blog.csdn.net/smallfish1983/article/details/38820441)
