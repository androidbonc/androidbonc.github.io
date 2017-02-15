---
layout: post
title: "《Nagios系统监控实践》简评+笔记"
date: 2014-03-26 13:42
comments: true
categories: Nagios
---

<!-- more -->

![Nagios系统监控实践 封面](https://tankywoo-wb.b0.upaiyun.com/nagios-xi-tong-jian-kong-shi-jian.jpg)

最近花了3个晚上快速看了这本书，一些暂时不会用的内容就直接忽略了。内容组成大概是80%的基础+20%的经验。

文章的内容排版分类比较清晰(不过有个别的比如nrpe, check\_mk等在多个章节中都提到):

* 第一章讲了一些运维监控的基本思想。
* 第二章全局上介绍了Nagios的基本原理和相关内容。
* 第三章是Nagios的安装，直接忽略了
* 第四章是Nagios的配置。
* 第五章是Nagios的一个模板框架的技巧，这一章第1节非常棒。
* 第六章是围绕Nagios的扩展核心--插件
* 第七章介绍了Nagios的一些Addon组件
* 第八章围绕Nagios的性能数据这块，配合入rrdtool工具来存储和绘制
* 第九章是Nagios XI，商业版的，直接忽略了
* 第十章是Nagios事件代理(NEB)，也被我忽略了

这本书是一本入门Nagios的好书，虽然讲得不是很深，但是全局性把握到了，可以很直观全面的学习Nagios。

并且该突出的地方，也都突出了。比如在检测间隔这块(P25)有详细的配图讲解，在状态(soft state和hard state)这块，都有讲到。

因为我在接触Nagios后都是零散的阅读官方文档，有些关键的地方就没有注意到。所以这本书在刚开始学习时看到可以减少后期的学习时间成本。

而且后期对Nagios了解加深后，也可以回过头来翻一翻这本书，有些地方的经验之谈还是不错的。

这本书不是很厚，就230面左右，里面还穿插了一些配合性的工具入rrdtool, snmp 等等，也占了一些篇幅。

不过其余内容入门足够了，剩下的还是得靠Nagios官方文档(这个才是最重要的)。

---

快速扫完这本书，也学到了一些东西，在网上简单了解了下这些东西，还未做尝试(所以可能有误)，先简单记录下：

### 开发脚本模板(P72) ###

第五章第一节，提到了 **开发脚本模板**，先开始还没看明白是什么，后来发现是一个模板技巧(经验):

用主机配置为例，一般一个主机的配置是有两部分: 共性(主机模板)和特性(主机定义)组成，比如:

模板:

	define host {
		name         base_host
		....
		register     0
	}

定义:

	define host{
		use          base_host
		host_name    NAME
		alias        NAME
		address      NAME.DOMAIN
	}

这个可以保存为名叫 hosts.skel 的框架模板

定义中的NAME, DOMAIN 这些都是一些变量，可以被替代的值。

这样就可以通过一份主机列表和一个小脚本来快速填充配置。比如主机列表:

	host1.mydomain.com
	host2.mydomain.com
	host3.mydomain.com
	...

小脚本:

	#!/bin/bash
	while read i
	do
		NAME='echo ${i} | cut -d. -f1'
		DOMAIN='echo ${i} | cut -d. -f2-'
		sed -e "s/NAME/$NAME/" -e "s/DOMAIN/$DOMAIN/" hosts.skel >> hosts.cfg
	done

### 第七章 Nagios的一些扩展(P129) ###

介绍了一些Nagios的优化和调整经验。

比如使用被动检测方式，减少监控端查询的开销，配合[NSCA](http://exchange.nagios.org/directory/Addons/Passive-Checks/NSCA--2D-Nagios-Service-Check-Acceptor/details)(Nagios Service Check Acceptor) 或 [NRDP](http://exchange.nagios.org/directory/Addons/Passive-Checks/NRDP--2D-Nagios-Remote-Data-Processor/details)(Nagios Remote Data Processor)，后者可以用来取代前者。

也讲到了一些分布式的结构，比如父子节点的方式和使用事件代理模块:

父子节点模式导致节点配置比较繁杂，父和子节点都要维护差不多的配置。

使用事件代理模块，使Nagios进程运行在不同机器上，并使用专用协议互相交换信息来进行协作。如 [DNX](http://exchange.nagios.org/directory/Addons/Distributed-Monitoring/DNX/details)(Distributed Nagios Executor，分布式Nagios执行程序)、Mod Gearman 等。

这一块的内容还需要进一步的了解学习。**TODO**

### NRPE(P105) ###

[NRPE](http://exchange.nagios.org/directory/Addons/Monitoring-Agents/NRPE--2D-Nagios-Remote-Plugin-Executor/details)(Nagios Remote Plugin Executor) 官方介绍和原理图:

> NRPE allows you to remotely execute Nagios plugins on other Linux/Unix machines. This allows you to monitor remote machine metrics (disk usage, CPU load, etc.). NRPE can also communicate with some of the Windows agent addons, so you can execute scripts and check metrics on remote Windows machines as well.

![Nagios NRPE 原理图](https://tankywoo-wb.b0.upaiyun.com/nagios_nrpe.png)

NRPE是一个轻量级的C/S系统，通过它Nagios服务器可以执行存放在被监控主机上的远端插件。

监控端运行一个 `check_nrpe` 程序，远端主机运行一个 `NRPE Daemon`。

监控端 `check_nrpe` 本地配置要监控的服务，通过SSL方式连接到远端的 `NRPE Daemon`，然后 NRPE Daemon 会执行相应的检测，将检查结果返回给`check_nrpe`。

这种方式也可以降低监控端主机的运行压力。

### Check MK(P114) ###

![Check MK 原理图](https://tankywoo-wb.b0.upaiyun.com/nagios_check_mk.png)

[Check\_MK](http://mathias-kettner.com/check_mk.html) 与传统的插件不一样，它是一个运行在被监控主机上的一个Agent。

而且它的使用非常简单，不需要配置，就可以主动检测获取主机的cpu/mem/disk/net 等信息。

一篇不错的文章: [手把手打造开源新监控利器check\_mk](http://grass51.blog.51cto.com/4356355/994819)

### NagiosQL(P77) ###

[NagiosQL](http://www.nagiosql.org/) 是一个基于Web的Nagios配置工具。这个就没去了解了，基于web去配置还是没有纯文本编辑来的快捷。。。


最后，关于本书和其它的一些资源:

* [InfoQ - 作者访谈与书评：“Nagios企业监控实践（原书第2版）”](http://www.infoq.com/cn/articles/building-nagios-monitoring-infrastructure-review)
* [Nagios学习笔记](http://www.chenshake.com/nagios-study-notes/)
* [Nagios Addon Projects](http://www.nagios.org/download/addons)
