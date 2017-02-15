---
layout: post
title: "IPv6 'dadfailed' Problem"
date: 2013-09-27 17:37
comments: true
categories: Linux
---

<!-- more -->

Two gateway machines, use `keepalive`.

The IPv6 address display:

	inet6 x:x:x:x::1/64 scope global tentative dadfailed

and can't `ping6` this address.

The reason is when another master machine is down, but the ipv6 address is not delete, and the new master machine can't use this address.

To prevent this:

	$ sysctl -a | grep accept_dad
	net.ipv6.conf.all.accept_dad = 0
	net.ipv6.conf.default.accept_dad = 0
	net.ipv6.conf.eth0.accept_dad = 0
	net.ipv6.conf.eth1.accept_dad = 0
	net.ipv6.conf.lo.accept_dad = -1
	net.ipv6.conf.tun0.accept_dad = -1
	net.ipv6.conf.tun1.accept_dad = -1

	# Than change the physic netcard's value to 0
	$ sysctl -w net.ipv6.conf.eth0.accept_dad=0
	$ sysctl -w net.ipv6.conf.eth1.accept_dad=0

	# Than delete the keepalive vip and create it

The meaning of `accept_dad`:

	accept_dad - INTEGER
		Whether to accept DAD (Duplicate Address Detection).
			0: Disable DAD
			1: Enable DAD (default)
			2: Enable DAD, and disable IPv6 operation if MAC-based duplicate
				link-local address has been found.

From [ip-sysctl.txt in kernel docs](https://www.kernel.org/doc/Documentation/networking/ip-sysctl.txt)
