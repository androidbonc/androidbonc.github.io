---
layout: post
title: "Ubuntu list file for package 'xxx' is missing final newline"
date: 2015-05-19 16:00
---

某台Ubuntu机器在通过`apt-get install a_package`时出现错误:

	(Reading database ... 90%dpkg: unrecoverable fatal error, aborting:
	 files list file for package 'libjpeg-turbo8' is missing final newline
	 E: Sub-process /usr/bin/dpkg returned an error code (2))

查看file:

	$ file /var/lib/dpkg/info/libjpeg-turbo8\:amd64.*
	/var/lib/dpkg/info/libjpeg-turbo8:amd64.list:     8086 relocatable (Microsoft)
	/var/lib/dpkg/info/libjpeg-turbo8:amd64.md5sums:  data
	/var/lib/dpkg/info/libjpeg-turbo8:amd64.postinst: ACB archive data
	/var/lib/dpkg/info/libjpeg-turbo8:amd64.postrm:   data
	/var/lib/dpkg/info/libjpeg-turbo8:amd64.shlibs:   ASCII text, with no line terminators
	/var/lib/dpkg/info/libjpeg-turbo8:amd64.symbols:  data

现在变成了如 relocatable 和data这样的文件, 之前也出现过, 应该是文件系统问题造成文件损坏.

手动删掉这些文件, 然后安装, 出现:

	(Reading database ...
	dpkg: warning: files list file for package `libjpeg-turbo8' missing, assuming package has no files currently installed.
	(Reading database ... 90%dpkg: unrecoverable fatal error, aborting:
	 files list file for package 'libjpeg8' is missing final newline
	E: Sub-process /usr/bin/dpkg returned an error code (2)

本删除的包提示缺失, 且另外一个包又出现前面的问题, 删除所有出现missing final newline的包, 然后需要`--reinstall`:

	$ apt-get install --reinstall libjpeg8 libjpeg-turbo8 python-six python-urllib3 htop

修复后可以正常安装原先欲安装的包了.
