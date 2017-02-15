---
layout: post
title: "The Holes of Crontab"
date: 2014-10-05 08:00
---

cron的软件很多，这里使用 `vixie-cron`，平台`Ubuntu 12.04`

cron的配置文件可在三个地方存放:

* `/var/spool/cron/crontabs/`
* `/etc/crontab`
* `/etc/cron.d/`

`/var/spool/cron/crontabs/` 通过`crontab`命令来控制, 属于用户的, 所以这个命令设置了`guid`, 属于`crontab`用户组.

`/etc/crontab` 默认是控制 `/etc/cron.*`, 如`/etc/cron.daily`, `/etc/cron.weekly`, `/etc/cron.monthly`这些

`/etc/cron.d/` 目录下也是存放crontab的配置文件.

`/etc/crontab` 和 `/etc/cron.d/` 在配置定时任务时，需要指定用户是`root`，而`/var/spool/cron/crontabs/`已经是属于用户控制的, 所以不需要指定用户, 这是格式上的区别.

cron 设置的默认环境变量:

* `$SHELL`: `/bin/sh`
* `$PATH`: `/usr/bin:/bin`

如果没有设置相关的环境变量，会造成如`$PATH`问题导致的命令找不到.

可以在cron配置文件顶部加上:

	SHELL=/bin/bash
	PATH=/usr/bin:/bin:/sbin:/usr/sbin
	*/5 * * * * root ./run.sh >/dev/null 2>&1

* `man 8 corn`
* `man 5 crontab`
* [/etc/crontab vs /etc/cron.d vs /var/spool/cron/crontabs/](http://www.linuxquestions.org/questions/linux-newbie-8/etc-crontab-vs-etc-cron-d-vs-var-spool-cron-crontabs-853881/)
