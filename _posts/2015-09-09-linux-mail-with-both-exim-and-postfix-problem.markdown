---
layout: post
title: "同时安装exim和postfix后执行mail的问题"
date: 2015-09-09 21:00
---

某台机器, 系统CentOS6, 用exim4作mta, 将邮件发送到远程的邮件服务器.

本地25端口是被exim4监听的.

python写的一个脚本连接25端口发送邮件是ok的.

但是本地一个shell脚本使用mail命令则无法发送, 且报了warning:

	postdrop: warning: unable to look up public/pickup: No such file or directory

网上搜下了, 这是postfix的报错, 修复用:

	mkfifo /var/spool/postfix/public/pickup

但是, MTA用的exim4.

首先, 我最开始忘了去考虑整套邮件系统. mail命令(使用的`mailx`), 是一个MUA; exim4, 角色是MTA.

导致我一直去关注mailx命令本身了.

抓包配合strace来分析, 使用mail发送邮件, 25端口并没有包, 且postfix报错.

然后在`/var/spool/postfix/maildrop/`下发现了阻塞发送失败的邮件.

且exim4日志里完全没有相关信息.

如果卸载掉postfix, 则可以用mail正常发邮件了.

所以可以确定, 从MUA到MTA这个过程有问题, 即邮件被postfix截获. MTA本身是工作正常的.

后来实在晕了, 就去[serverfault](http://serverfault.com/questions/721220/exim4-and-postfix-cannot-both-exists)上提问, 没过多久, 就得到解惑了.

> That is likely triggered from the [alternatives](http://serverfault.com/questions/721220/exim4-and-postfix-cannot-both-exists) system.
> 
> Simply installing postfix may have made that default MTA (by updating the symbolic link `/usr/lib/sendmail`) and because postfix was not yet configured nor running --> instant error.
> 
> You can resolve that by running `alternatives --config mta` and restoring Exim as the default.

alternatives系统, 是重新实现debian的alternatives系统.

主要用于管理命令的软链接.

	$ alternatives --display mta
	mta - status is auto.
	 link currently points to /usr/sbin/sendmail.postfix
	/usr/sbin/sendmail.exim - priority 10
	 slave mta-pam: /etc/pam.d/exim
	 slave mta-mailq: /usr/bin/mailq.exim
	 slave mta-newaliases: /usr/bin/newaliases.exim
	 slave mta-rmail: /usr/bin/rmail.exim
	 slave mta-rsmtp: /usr/bin/rsmtp.exim
	 slave mta-runq: /usr/bin/runq.exim
	 slave mta-sendmail: /usr/lib/sendmail.exim
	 slave mta-mailqman: /usr/share/man/man8/exim.8.gz
	 slave mta-newaliasesman: (null)
	 slave mta-aliasesman: (null)
	 slave mta-sendmailman: (null)
	/usr/sbin/sendmail.postfix - priority 30
	 slave mta-pam: /etc/pam.d/smtp.postfix
	 slave mta-mailq: /usr/bin/mailq.postfix
	 slave mta-newaliases: /usr/bin/newaliases.postfix
	 slave mta-rmail: /usr/bin/rmail.postfix
	 slave mta-rsmtp: (null)
	 slave mta-runq: (null)
	 slave mta-sendmail: /usr/lib/sendmail.postfix
	 slave mta-mailqman: /usr/share/man/man1/mailq.postfix.1.gz
	 slave mta-newaliasesman: /usr/share/man/man1/newaliases.postfix.1.gz
	 slave mta-aliasesman: /usr/share/man/man5/aliases.postfix.5.gz
	 slave mta-sendmailman: /usr/share/man/man1/sendmail.postfix.1.gz
	Current `best' version is /usr/sbin/sendmail.postfix.

首先, 可以看到, mta的状态是auto的, 表明这个链接是可能变化的, 具体和优先级有关.

上面有两个mta, `/usr/sbin/sendmail.exim` 和 `/usr/sbin/sendmail.postfix`, 优先级分别是10和30.

所以最后也提到了, 当前的最佳版本是postfix的MTA.

这块也可以用`alternatives --set mta /usr/sbin/sendmail.exim` 去强制指定.

如果卸载postfix后:

	$ alternatives --display mta
	mta - status is auto.
	 link currently points to /usr/sbin/sendmail.exim
	/usr/sbin/sendmail.exim - priority 10
	 slave mta-pam: /etc/pam.d/exim
	 slave mta-mailq: /usr/bin/mailq.exim
	 slave mta-newaliases: /usr/bin/newaliases.exim
	 slave mta-rmail: /usr/bin/rmail.exim
	 slave mta-rsmtp: /usr/bin/rsmtp.exim
	 slave mta-runq: /usr/bin/runq.exim
	 slave mta-sendmail: /usr/lib/sendmail.exim
	 slave mta-mailqman: /usr/share/man/man8/exim.8.gz
	 slave mta-newaliasesman: (null)
	 slave mta-aliasesman: (null)
	 slave mta-sendmailman: (null)
	Current `best' version is /usr/sbin/sendmail.exim.

alternatives管理的文件在`/etc/alternatives`, 都是一些软链接.

个人猜测一些细节, 可能有误. mail命令调用本地配置的mta, 所以有postfix时调用了postfix, 而并不是主动连接本地的25端口???
