---
layout: post
title: "通过netcat或iperf测试网络带宽"
date: 2014-03-18 00:42
comments: true
categories: Linux
---

<!-- more -->

`nc`是个好东西~~~

用到的有功能有:

* 传输文件
* 测试带宽
* 发包测试
* ...

关于测试网络带宽:

	# 主机A
	nc -l -p 22222 < /dev/zero

	# 主机B
	nc ip_of_hostA 22222 > /dev/null

然后顺便也搜到[网上这篇](http://nerdicism.com/2010/10/shell-hint-messure-bandwidth-with-netcat-nc-and-pipe-view-pv/)的方法，发现了 `pv`(monitor the progress of data through a pipe) 这个命令。

比如:

	# 主机A
	nc -l -p 22222 < /dev/null
	# 主机B
	nc localhost 22222 | pv

然后可以显示传输的总流量大小和速率:

	2.66GiB 0:01:10 [  40MiB/s ] [                 <=>                      ]

另外还看到很多人推荐使用 `iperf`(tool to measure IP bandwidth using UDP or TCP) 工具，看它的介绍就是用来测试带宽的:

	# Server
	tankywoo@gentoo-local::~/ » iperf -s
	------------------------------------------------------------
	Server listening on TCP port 5001
	TCP window size: 85.3 KByte (default)
	------------------------------------------------------------
	[  4] local 127.0.0.1 port 5001 connected with 127.0.0.1 port 56071
	[ ID] Interval       Transfer     Bandwidth
	[  4]  0.0-10.0 sec  27.0 GBytes  23.2 Gbits/sec

	# Client
	tankywoo@gentoo-local::~/ » iperf -c localhost
	------------------------------------------------------------
	Client connecting to localhost, TCP port 5001
	TCP window size:  647 KByte (default)
	------------------------------------------------------------
	[  3] local 127.0.0.1 port 56071 connected with 127.0.0.1 port 5001
	[ ID] Interval       Transfer     Bandwidth
	[  3]  0.0-10.0 sec  27.0 GBytes  23.2 Gbits/sec

网上有两篇讲得不错的:

* [Using iPerf to Troubleshoot Speed/Throughput Issues](http://blog.softlayer.com/2011/using-iperf-to-troubleshoot-speedthroughput-issues)
* [Using iPerf to Troubleshoot Speed/Throughput Issues](http://www.slashroot.in/iperf-how-test-network-speedperformancebandwidth)

