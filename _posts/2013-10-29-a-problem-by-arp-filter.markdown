---
layout: post
title: "A problem by arp_filter"
date: 2013-10-29 17:14
comments: true
categories: Linux
---

<!-- more -->

`arp_filter`的定义:

> arp_filter - BOOLEAN
> 	1 - Allows you to have multiple network interfaces on the same
> 	subnet, and have the ARPs for each interface be answered
> 	based on whether or not the kernel would route a packet from
> 	the ARP'd IP out that interface (therefore you must use source
> 	based routing for this to work). In other words it allows control
> 	of which cards (usually 1) will respond to an arp request.
> 
> 	0 - (default) The kernel can respond to arp requests with addresses
> 	from other interfaces. This may seem wrong but it usually makes
> 	sense, because it increases the chance of successful communication.
> 	IP addresses are owned by the complete host on Linux, not by
> 	particular interfaces. Only for more complex setups like load-
> 	balancing, does this behaviour cause problems.
> 
> 	arp_filter for the interface will be enabled if at least one of
> 	conf/{all,interface}/arp_filter is set to TRUE,
> 	it will be disabled otherwise

引用至 [ip-sysctl.txt](https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt)

------

具体场景:

ESXi只有一个 `vSwitch` 绑定在实体机的第一块物理网卡上. 

在 ESXi 上新建一个虚拟机, 虚拟机有两块虚拟网卡, 都使用的是同一个 vSwitch.

虚拟机的 eth0 当作内网, eth1 当作外网. eth0 上有自己本身配置的内网ip(10.255.11.251)和LVM的VIP(10.255.11.1).

同网段下另外一台CDN机器(10.255.11.30), 使用这个网关机器的VIP当作网关.

然后发现 VIP ping不通, 查看 arp, 发现:

	Address                  HWtype  HWaddress           Flags Mask            Iface
	10.255.11.1              ether   00:50:56:88:62:77   C                     eth0
	10.255.11.251            ether   00:50:56:88:23:c5   C                     eth0

arp缓存中, 10.255.11.251 对应的 mac 地址就是网关机器的 eth0 网卡的mac地址, 是正确的.

但是 10.255.11.1 这个VIP对应的 mac 地址是网关机器的 eth1 网卡的 mac 地址.


先清空CDN机器上 10.255.11.1 的arp缓存,  然后在网关机器下抓arp包:

	$ tcpdump -nn -p -i eth0 arp
	09:55:04.843231 ARP, Request who-has 10.255.11.1 tell 10.255.11.30, length 46
	09:55:04.843243 ARP, Reply 10.255.11.1 is-at 00:50:56:88:23:c5, length 28

	$ tcpdump -nn -p -i eth1 arp
	09:57:19.619136 ARP, Request who-has 10.255.11.1 tell 10.255.11.30, length 46
	09:57:19.619150 ARP, Reply 10.255.11.1 is-at 00:50:56:88:62:77, length 28

会发现两块网卡都收到 arp 的 request 包并 reply 了.

因为实际的情况是网关的两块虚拟网卡都共用的一个实际物理网卡

所以 arp 广播获取 mac 地址时, 两块虚拟网卡都会收到 request 包, 并各自做了回应, 实际获取到的mac与两块网卡的响应顺序有关.

解决的办法就是 `arp_filter` 这个参数.

看 arp_filter 的解释可以知道, arp_filter 是一个布尔值, 默认值是0. 简单翻译下:

> 内核可以用其他网卡来回应arp请求.
> 这看起来是错的, 但是它增大了成功通讯的可能性.
> IP地址属于整个主机, 而不是特定的接口.
> 只是在一些复杂的情况, 比如负载均衡, 会出现错误.

最后一句明确说了, 这也可以解释为何之前到现在出现这种情况, 都是 VIP 的 mac 地址有问题了.

arp_filter的值改为1 则表示控制具体应该由哪块网卡来回应arp包. 所以改为1就OK了.

查看 `arp_filter` 的配置:

	$ sysctl -a | grep arp_filter
	net.ipv4.conf.all.arp_filter = 0
	net.ipv4.conf.default.arp_filter = 0
	net.ipv4.conf.eth0.arp_filter = 0
	net.ipv4.conf.eth1.arp_filter = 0
	net.ipv4.conf.lo.arp_filter = 0
	net.ipv4.conf.tun0.arp_filter = 0
	net.ipv4.conf.tun1.arp_filter = 0

修改 `/etc/sysctl.d/local.conf` 文件, 增加:

	net.ipv4.conf.default.arp_filter = 1
	net.ipv4.conf.all.arp_filter = 1

然后重启:

	/etc/init.d/sysctl restart
