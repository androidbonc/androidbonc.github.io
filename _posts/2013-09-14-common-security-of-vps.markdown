---
layout: post
title: "Common Security of VPS"
date: 2013-09-14 13:49
comments: true
categories: Ops
---

<!-- more -->

Recently I changed vps to [Linode](http://www.linode.com/?r=cbaf3002f72433e7aa10d771ef03ec0a0e673040), OS is `Gentoo`.

To improve security, there are some steps to do:

1. Use a common user, not root.
2. SSH limit root login and password authentication.
3. Add iptables rules.


The good examples of iptables configuration:

	*filter

	#  Allow all loopback (lo0) traffic and drop all traffic to 127/8 that doesn't use lo0
	-A INPUT -i lo -j ACCEPT
	-A INPUT ! -i lo -d 127.0.0.0/8 -j REJECT

	#  Accept all established inbound connections
	-A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

	#  Allow all outbound traffic - you can modify this to only allow certain traffic
	-A OUTPUT -j ACCEPT

	#  Allow HTTP and HTTPS connections from anywhere (the normal ports for websites and SSL).
	-A INPUT -p tcp --dport 80 -j ACCEPT
	-A INPUT -p tcp --dport 443 -j ACCEPT

	#  Allow ports for testing
	-A INPUT -p tcp --dport 8080:8090 -j ACCEPT

	#  Allow ports for MOSH (mobile shell)
	-A INPUT -p udp --dport 60000:61000 -j ACCEPT

	#  Allow SSH connections
	#  The -dport number should be the same port number you set in sshd_config
	-A INPUT -p tcp -m state --state NEW --dport 22 -j ACCEPT

	#  Allow ping
	-A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT

	#  Log iptables denied calls
	# -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables denied: " --log-level 7

	#  Reject all other inbound - default deny unless explicitly allowed policy
	-A INPUT -j REJECT
	-A FORWARD -j REJECT

	COMMIT

Reference:

* [How To Set Up Your Linode For Maximum Awesomeness](http://feross.org/how-to-setup-your-linode/)
* [Securing Your Server](https://library.linode.com/securing-your-server?format=print)
