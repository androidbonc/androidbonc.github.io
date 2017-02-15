---
layout: post
title: "Rsyslog Rotate Log by Size"
date: 2014-02-28 13:56
comments: true
categories: Linux
---

Rsyslog 到目前的版本(v8) 还没有支持 Log Rotation 功能，不过可以通过其它方式进行一些简单的rotate操作。

简单的实现 Log Rotation 使用的是 `OUTPUT CHANNELS`。

Output channels 通过 `$outchannel` 命令来定义的，语法格式:

	$outchannel name,file-name,max-size,action-on-max-size

* $outchannel name : 是定义的 outchannel 名称，后面需要使用到
* file-name : 是用来写入日志的文件名
* max-size : 是文件允许的最大大小，大小是 Byte
* action-on-max-size : 当文件大小超过 max-size, 会触发 action-on-max-size 这个命令

<!-- more -->

注意: 

> action-on-max-size  a command to be issued when the max size is reached. This command always has exactly one parameter. The binary is that part of action-on-max-size before the first space, its parameter is everything behind that space.

action-on-max-size 是一个命令，总是有一个参数。命令的第一个空格之前是执行的命令，空格后面是参数。

上面的命令仅仅是定义了这个 channel, 要使用它，还需要使用一个选择器，选择器包含这个channel名称，channel前面使用输出操作 `:omfile:$`，例如：

	*.* :omfile:$mychannel

这里表示所有的facilities的所有property都是用名叫 mychannel 这个 outchannel 。

注：Output Channels 在以后会被其他方式代替，所以如果升级到以后的版本，要注意是否还支持这个语法，以及是否会有内置更方便的方式。

实例：

	# 定义名叫log_rotation的outchannel, 限制文件大小是 104857600, 单位是Byte, 也就是100M。当大小超过100M，则会执行 rm /var/log/t.log。
	$outchannel log_rotation,/var/log/t.log,104857600,rm /var/log/t.log 
	# 使用这个outchannel, 当程序名以 logrecord 开始。
	:programname,startswith,"logrecord" :omfile:$log_rotation 

更详细可以参考: [Log rotation with rsyslog](http://www.rsyslog.com/doc/log_rotation_fix_size.html)

Rsyslog Wiki 还有一个以日期为单位的的 Log Rotation 方式：[DailyLogRotation](http://wiki.rsyslog.com/index.php/DailyLogRotation)

更强悍的方式是使用 `logrotate` 工具, 还没有研究过:

	*  app-admin/logrotate
		  Latest version available: 3.8.7
		  Latest version installed: [ Not Installed ]
		  Size of files: 57 kB
		  Homepage:      https://fedorahosted.org/logrotate/
		  Description:   Rotates, compresses, and mails system logs
		  License:       GPL-2
