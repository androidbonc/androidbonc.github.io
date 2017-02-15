---
layout: post
title: "Linux FTP Command timeout problem"
date: 2013-09-15 19:35
comments: true
categories: Linux
---

<!-- more -->

The remote server is a virtual host, so I can only download file by ftp.

Gentoo install `net-ftp/ftp`.


When I use `ftp x.x.x.x`, login in and use `ls` to list remote files:

	16:07 root@linode-gentoo /opt
	% ftp X.X.X.X
	Connected to X.X.X.X
	220 ProFTPD 1.3.4a Server ready.
	Name (X.X.X.X:root): wutianqi   # Enter username
	234 AUTH SSL successful
	[SSL Cipher DHE-RSA-AES256-SHA]
	331 Password required for wutianqi
	Password:                       # Enter password
	230 User wutianqi logged in     # Login in OK
	Remote system type is UNIX.
	Using binary mode to transfer files.
	ftp> cd backups
	250 CWD command successful
	ftp> get xxxx.tar.gz
	local: xxxx.gz remote: xxxx.tar.gz
	200 PORT command successful
	425 Unable to build data connection: Connection timed out # Timeout!!!
	ftp>

So I google and fount the reasom.

* [ANT FTP upload file: 425 Unable to build data connection: Connection timed out](http://stackoverflow.com/a/8035797/1276501)
* [Can't connect to FTP server: 425 Unable to build data connection: Connection timed out](http://superuser.com/questions/356138/cant-connect-to-ftp-server-425-unable-to-build-data-connection-connection-tim)
* [FTP Connection Issues. Active And Passive FTP Modes.](http://hosting.intermedia.net/support/kb/?id=1146)

The default mode of ftp command is `Active Mode`, as above posts suggest: use `Passive Mode`:

	17:04 root@linode-gentoo /root
	% ftp -p X.X.X.X
	zsh: correct 'ftp' to 'sftp' [nyae]? n
	Connected to X.X.X.X
	220 ProFTPD 1.3.4a Server ready.
	Name (X.X.X.X:root): wutianqi
	234 AUTH SSL successful
	[SSL Cipher DHE-RSA-AES256-SHA]
	331 Password required for wutianqi
	Password:
	230 User wutianqi logged in         # Login in OK
	Remote system type is UNIX.
	Using binary mode to transfer files.
	ftp> ls
	227 Entering Passive Mode (216,18,218,180,136,244).
	ftp: connect: Connection timed out        # Also Timeout!!! Fuck!!!
	ftp> ls
	421 Service not available, remote server has closed connection
	Passive mode refused.
	ftp>

But if I use ftp clinet in windows such as `FileZilla`, or `wget` by ftp, there is no problem.

This puzzled me, and I can't find the reason, I have leave message to the master of virtual host to inquire about the problem.

PS: I think I should change to use `lftp` or `pftp`...


Append:

I check that the iptables in my Linode VPS is stoped.

lftp also can't connect. But can connect from my local linux host.

