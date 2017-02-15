---
layout: post
title: "关于Nagios主机的Parents依赖"
date: 2014-04-11 11:04
comments: true
categories: Nagios
---

<!-- more -->

今天Nagios报警里碰到一个问题:

网关节点 gw 机器和后端一堆子节点 host1, host2... 配置了 `parents` 依赖关系。 现在这个机房出问题了，按我以前的理解来说只有gw这台机器会报警，其余的后端子节点都不会报警。

但是实际上 gw机器报了 `DOWN` , host1, host2 ... 等都报了 `UNREACHABLE`。

后来又翻了下文档，发现有些位置以前理解错了。

首先主机的检测及最后的状态比较特殊，因为检测的结果依然是 OK, WARNING, UNKNOWN, CRITICAL 这四个。但是主机最终的报警是三种状态: UP, DOWN, UNREACHABLE。这里就涉及到一个状态转换的问题，在官方 [hostchecks](http://nagios.sourceforge.net/docs/3_0/hostchecks.html) 这篇文档讲了主机检测及状态是如何最终确认的。

因为每个主机的parents都是 gw 这一台机器，所以当 后端机器检查宕机了，会检查parents机器gw，因为只有一个parents机器，所以当gw机器也检测为宕机后，根据官方提供的状态转换表，后端子机器的状态是 UNREACHABLE。

因为主机的parents只涉及到状态的改变，如果只想收到 parents 节点的报警，可以在主机的 `notification_options` 设置里把 `u` 选项去掉。

另外关于主机的这两个状态(DOWN 和 UNREACHABLE)，可以看看官方的[Determining Status and Reachability of Network Hosts](http://nagios.sourceforge.net/docs/3_0/networkreachability.html) 这篇文章。
