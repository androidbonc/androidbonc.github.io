---
layout: post
title: "Nagios serviceescalation for All but Exclude One"
date: 2013-12-04 14:41
comments: true
categories: Nagios
---

<!-- more -->

最近上线一个 Nagios 插件, 因为有点问题, 报警很多. 为了这些报警邮件不影响一个分组下的其他人, 我单独把这个服务的 contacts 改为一个只有我一个人的联系组, 这样也方便调试.

不过发现在报警超过三次时, 别人还是会收到报警邮件, 看了下配置, 原来是 `serviceescalation` 造成的.

关于 Nagios 的 escalation 解释:

> Nagios supports optional escalation of contact notifications for hosts and services. Escalation of host and service notifications is accomplished by defining host escalations and service escalations in your object configuration file(s). Once a notification is escalated, the contact/groups and notification options for the object will be overridden by the escalation's settings.

From [Notification Escalations](http://nagios.sourceforge.net/docs/nagioscore/4/en/escalations.html)

原来的配置是:

	define service {
		use                    check_xxx
		hostgroup_name         test-group
		contacts               tankywoo-group
		service_description    Check XXX
	}

	define serviceescalation {
		hostgroup_name          all-groups
		service_description     *
		first_notification      3
		last_notification       0
		contacts                all
	}

意思就是定义了一个服务, 名叫 check_xxx, 报警联系组是 tankywoo-group; serviceescalation 中用到的 all-groups 是所有主机组集合, 包含test-group, 而service_description 用的是通配符 `*`.

这个相当于定义了一个默认值, 任何主机的任何服务, 在报警次数大于3次时, 就会覆盖原来的contacts, 从而给 all 这个联系组报警.


在 Nagios 文档上搜了下通配符这块, 见 [Time-Saving Tricks For Object Definitions](http://nagios.sourceforge.net/docs/3_0/objecttricks.html#serviceescalation)

里面提到了可以用 `!` 来反向选择, 即`不包括`的意思. 

接着我尝试在 `service_description` 这里做修改:

	define serviceescalation {
		hostgroup_name          all-groups
		service_description     *,!Check XXX
		first_notification      3
		last_notification       0
		contacts                all
	}

这样就相当于针对所有的服务(但是排除Check XXX这个服务).

另外关于 `serviceescalation` 的定义结构见: [Object Definitions](http://nagios.sourceforge.net/docs/nagioscore/3/en/objectdefinitions.html#serviceescalation)
