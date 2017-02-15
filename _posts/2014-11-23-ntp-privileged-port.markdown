---
layout: post
title: "NTP Privileged Port"
date: 2014-11-23 11:00
---

某个机房，发现ntp服务有问题。

于是停掉服务手动用`ntpdate`测试了很多国内外的ntp server，发现都不通:

    no server suitable for synchronization found

又尝试使用 `-d` 调试模式:

> -d     Enable the debugging mode, in which ntpdate will go through all the steps, but not adjust the local clock. Information useful for general  debugging will also be printed.

发现是OK的.

接着看到`-u`参数:

> -u     Direct  ntpdate  to use an unprivileged port for outgoing packets. This is most useful when behind a firewall that blocks incoming traffic to privi‐leged ports, and you want to synchronize with hosts beyond the firewall. Note that the -d option always uses unprivileged ports.


可以正常连通. 此参数将出去的包使用非特权端口(默认是123)。并且`-d`参数会使用非特权端口.

进而抓包查看, 发现确实123端口的udp包被拦截了, 所以怀疑机房有防护设备.

因为 ntp 服务器没法配置使用非特权端口，所以暂时处理的唯一办法就是通过vpn从内网走，绕过机房防护设备.

Refer to [StackOverflow](http://stackoverflow.com/a/240251/1276501):

> If you're going to run ntpd, you need to fix your network/firewall/NAT so that ntpd can have full unrestricted access to UDP port 123 in both directions.

> If this is not possible, you may need to run ntpd on the firewall itself, so that it can have full unrestricted access to UDP port 123 in both directions, and then have it serve time to your internal clients.

> If that's not possible, your only other option may be to buy the necessary hardware to connect to one or more of your own computers and run your own Stratum 1 time server or buy a pre-packaged Stratum 1 time server.
