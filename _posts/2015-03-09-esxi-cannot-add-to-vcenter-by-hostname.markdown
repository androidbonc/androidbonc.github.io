---
layout: post
title: "解决ESXi无法通过域名加入到vCenter"
date: 2015-03-09 15:00
---

最近有台ESXi, 无法通过内网域名加入到vCenter, 但是直接通过内网IP可以.

查看到DNS配置中这个机器的域名有一个IPv4和一个IPv6的记录.

通过SSH登录vCenter, ping IPv4的地址可以, ping6 IPv6的地址则不通.

首先vCenter的IPv6路由都是正确的, 问题出在ESXi上.

考虑到之前有Nagios的服务, 检查SSH服务时, SSH服务的IPv6配置有问题, 导致检查报错.

怀疑这里类似, 因为通过内网域名添加主机, 会解析这个域名, 获取到IPv4和IPv6的地址.

vCenter内部可能会对这两个地址都做一个存活性检查, 导致在IPv6处超时而无法加上.

首先, 在ESXi上开启对IPv6的支持:

> 配置 -> 网络 -> 右上角的"属性" -> 勾选 在该主机系统上启用IPv6支持

然后重启ESXi, 不然后续的IPv6设置不会出现.

另外, 在ESXi上配置上IPv6的IP/GW

> 配置 -> 网络 -> 标准交换机的"属性" -> 编辑"Management Network" -> 切换到 "IP 设置" 页 -> 添加 IPv6地址, 以及编辑IPv6的VMkernel默认网关

配置好后, 在vCenter就可以ping6通ESXi的IPv6地址了.

再通过域名添加ESXi即可,

其实这里在域名记录里, 将IPv6地址删掉, 也可以解决这个问题.
