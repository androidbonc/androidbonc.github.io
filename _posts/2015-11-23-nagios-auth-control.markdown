---
layout: post
title: "Nagios权限管理 - 实现指定人员只能查看指定主机"
date: 2015-11-23 21:00
---

一个很常见的需求: 对于某些人员, 只允许其在Nagios Web管理页面查看指定的主机

首先确保Nagios配置和用户的帐号是OK的, 也就是配置正确后, 登录Nagios Web, 是可以看到期望的主机列表.

首先是`cgi.cfg`的配置, 具体可以参考 [CGI Configuration File Options](https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/configcgi.html)

`use_authentication` 控制是否开启权限管理. 默认开启.

	This option controls whether or not the CGIs will use the authentication and authorization functionality when determining what information and commands users have access to.I would strongly suggest that you use the authentication functionality for the CGIs. If you decide not to use authentication, make sure to remove the command CGI to prevent unauthorized users from issuing commands to Nagios. The CGI will not issue commands to Nagios if authentication is disabled, but I would suggest removing it altogether just to be on the safe side. More information on how to setup authentication and configure authorization for the CGIs can be found here.

	* 0 = Don't use authentication functionality
	* 1 = Use authentication and authorization functionality (default)

另外就是一系列`authorized_*`开头的配置项:

	authorized_for_system_information=
	authorized_for_configuration_information=
	authorized_for_system_commands=
	authorized_for_all_services=
	authorized_for_all_hosts=
	authorized_for_all_service_commands=
	authorized_for_all_host_commands=
	authorized_for_read_only=

后面都接的用户名, 逗号分隔.

`authorized_for_all_hosts/authorized_for_all_service` 控制用户是否有权限查看主机/服务的状态; `authorized_for_all_host_commands/authorized_for_all_service_commands`控制用户是否有权限去下发一些命令.

`authorized_for_read_only`配置用户是只读权限, 只能看, 不能做一些管理类的操作, 进入一个主机或服务的状态页面, 没有右边的管理栏.

上面是一些全局性的控制, 更细粒度的控制在自定义的配置文件中. 首先自习看几遍 [Authentication And Authorization In The CGIs](https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/cgiauth.html)

Nagios的认证对象分为两个:

* authenticated user: web server配置的账户/密码, 并且被Nagios配置授权
* authenticated contact: 本质是一个authenticated user, 不过他的username和contact定义的name是一样. 这样他就能访问配置了指定他contact的主机/服务.

我们需要的就是后者.

**简单的说就是定义一个contact对象, 并且这个对象的 `contact_name` 和 `username` 一致.**

举一个具体的例子(无关配置省略), 一般情况:

	def contact {
		contact_name                   Ops
		email                          user_a@example.com,user_b@example.com,...
	}

	define host {
		use                            generic-host
		host_name                      Server1
		alias                          Server1
		contacts                       Ops
		...
	}

	define service {
		use                            generic-service
		host_name                      Server1
		service_description            HTTP
		contacts                       Ops
		...
	}

现在想让user_a这个用户登录Nagios后可以看到Server1的状态. 需要修改为:

	def contact {
		contact_name                   user_a
		email                          user_a@example.com
	}

	define host {
		use                            generic-host
		host_name                      Server1
		alias                          Server1
		contacts                       Ops,user_a
		...
	}

另外, 也可以保留原来的风格, 将Ops这个contact改为一个contact_group:

	def contact {
		contact_name                   user_a
		email                          user_a@example.com
	}

	def contact {
		contact_name                   user_b
		email                          user_b@example.com
	}

	def contactgroup {
		contactgroup_name              Ops
		members                        user_a,user_b
	}

	define host {
		use                            generic-host
		host_name                      Server1
		alias                          Server1
		contact_groups                 Ops
		...
	}

	define service {
		use                            generic-service
		host_name                      Server1
		service_description            HTTP
		contact_groups                 Ops
		...
	}

其它参考:

* [Nagios - Is it possible to create “view only” users and let them view only specific services/servers?](http://serverfault.com/questions/436886/nagios-is-it-possible-to-create-view-only-users-and-let-them-view-only-speci)
* [Setup Nagios User to View Specific Host and Services](http://linuxsysadminblog.com/2009/05/setup-nagios-user-to-view-specific-host-and-services/)
