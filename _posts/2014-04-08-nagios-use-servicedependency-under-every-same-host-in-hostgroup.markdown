---
layout: post
title: "Nagios一个主机组下每台主机的两个服务定义同一个依赖"
date: 2014-04-08 17:59
comments: true
categories: Nagios
---

<!-- more -->

今天在优化Nagios时遇到这个需求:

一个主机组下，每台主机都定义了几个服务A, B, C，服务B和C都依赖于服务A，这时就可以使用Nagios的服务依赖指令`servicedependency`。

先看[文档](http://nagios.sourceforge.net/docs/3_0/objectdefinitions.html#servicedependency)写了第一个尝试版本:

	define servicedependency{
		dependent_hostgroup_name         group_all
		dependent_service_description    service_B,service_C
		hostgroup_name                   group_all
		service_description              service_A
		execution_failure_criteria       w,u,c
		notification_failure_criteria    w,u,c
	}

这里总感觉怪怪的，因为这样写出来，意思就是任何group\_all主机组中的主机的B服务出问题了，就会检查主机组group\_all中的**所有**主机的A服务。这样明显不对，因为只应该检查相应主机，而不是这个主机组。

当然，使用 `-v` 检查配置，也暴露出问题了，直接卡在检查依赖那块，cpu到90%。

接着参考了Nagios的一篇文档[Time-Saving Tricks For Object Definitions](http://nagios.sourceforge.net/docs/3_0/objecttricks.html#servicedependency) 的 Same Host Dependencies 部分 和 nagios邮件组的一个[提问](https://www.mail-archive.com/nagios-users@lists.sourceforge.net/msg32088.html):

> 相同主机/主机组，只需要定义 host\_name/hostgroup\_name 就可以了

接着改为:

	define servicedependency{
		hostgroup_name                   group_all
		dependent_service_description    service_B,service_C
		service_description              service_A
		execution_failure_criteria       w,u,c
		notification_failure_criteria    w,u,c
	}

去掉 `dependent_hostgroup_name` 指令就可以了，检查也一会就好了。
