---
layout: post
title: "Nagios 邮件报警增加相应主机/服务的Url"
date: 2014-03-19 23:44
comments: true
categories: Nagios
---

<!-- more -->

之前Nagios的邮件报警，是把一些主要的环境变量值获取并发送邮件。

每次看到报警邮件，都得在Web页面上先找到相应的主机/服务页面，然后再进行如acknowledge等操作，这样非常不方便。

因为 Web 页面针对主机/服务的Url，都是有特点的，比如:

主机Host页面url:

	http://xxx.com/cgi-bin/extinfo.cgi?type=1&host=$HOSTNAME$

服务Service页面url:

	http://xxx.com/cgi-bin/extinfo.cgi?type=2&host=$HOSTNAME$&service=$SERVICEDESC$

上面使用到的 `$HOSTNAME$` 和 `$SERVICEDESC$` 都是Nagios 的环境变量。

在邮件里增加了链接后，就可以很方便的直接点击url访问相关页面进行处理。

当然，还有一些想法，不知道实现起来有多复杂，比如:

1. 通过回复邮件进行acknowlegde，这个类似Github的Issue，可以在web上回复，或直接回复邮件。
2. 继续增加一些相关处理的链接，比如disable check/notification 等

暂时想到那么多，后续可以再考虑下。
