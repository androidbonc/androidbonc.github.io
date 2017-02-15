---
layout: post
title: "Primary/Supplementary Group, GID/EGID"
date: 2015-06-23 15:00
---

昨天排查一个问题, 代码里有个地方读取了/var/log/syslog, 文件的用户/组是syslog:adm, 执行用户是usera, 属于组adm

之前是通过:

	sudo -u usera python /path/to/script

后来改为:

	setuidgid usera python /path/to/script

然后就出问题了. [`setuidgid`](http://cr.yp.to/daemontools/setuidgid.html)是daemontools的一个组件, 查看文档:

> setuidgid sets its uid and gid to account's uid and gid, removing **all supplementary groups**. It then runs child.

最简单的测试:

	$ sudo -u usera id
	uid=1000(usera) gid=1000(usera) groups=1000(usera),4(adm),...

	$ setuidgid usera id
	uid=1000(usera) gid=1000(usera) groups=1000(usera)

---

看到上面提到的`supplementary group`, 对这块的概念理解不是很清晰, 所以好好查了下.

首先, 每个文件都有 用户 和 群组 的概念, 如上所说的.

每个用户有 uid 和 gid 的概念, `/etc/passwd`可以看到每个用户的uid

新建用户时, 会在`/etc/group`下也添加一个同名的组:

	root@gentoo-local::init.d/ » grep -ir 'usera' /etc/passwd /etc/group
	/etc/passwd:usera:x:1003:1003::/home/usera:/bin/bash
	/etc/group:usera:x:1003:

这个组是`初始群组(initial group)`, 所以第四栏是空

也可以把用户添加到其它群组:

	usermod -a -G groupname username

`-a`表示append.

新建群组`groupadd`:

	groupadd groupname

现在我把一个新建用户加到了adm和testgroup两个群组:

	$ id
	uid=1003(usera) gid=1003(usera) groups=1003(usera),4(adm),2000(testgroup)

可以看到:

uid和gid都是1003, 加入的群组有usera,adm,testgroup

使用`newgrp`修改用户usera的gid, 只能修改为支持的群组之一:

	$ newgrp testgroup
	$ id
	uid=1003(usera) gid=2000(testgroup) groups=1003(usera),4(adm),2000(testgroup)
	$ touch newfile
	$ ls -al newfile
	-rw-r--r-- 1 usera testgroup 0 May 31 06:49 newfile

针对用户群组, 有两个概念:

* primary group
* supplementary group(secondary group)

当用户登录后, 配置的默认群组就是Primary Group, 也就是id结果中的gid, 或/etc/passwd的第4栏.

剩下的群组, 也就是id命令groups里除了primary group的所有群组, 就是Supplementary Group

(这块在<鸟哥私房菜>中, 提到`groups`输出的第一个组是primary group, 这块有问题, 至少我在Gentoo下测试不是这样的)

针对进程, 有:

* real id (UID, GID, 或者RUID, RGID)
* effective id (EUID, EGID)
* save id (SUID, SGID)

正常情况下, UID == EUID; 但是如果有如seteuid更改EUID, UID != EUID

这篇[回答](http://unix.stackexchange.com/questions/76634/what-is-a-process-gid-and-what-purpose-does-it-serve)不错:

> At any time, each process has an effective user ID, an effective group ID, and a set of supplementary group IDs. These IDs determine the privileges of the process. They are collectively called the persona of the process, because they determine "who it is" for purposes of access control.

还有[GID, current, primary, supplementary, effective and real group IDs?](http://unix.stackexchange.com/a/18203/45725)

修改UID会一起修改相应的EUID

	#include <stdio.h>
	#include <unistd.h>

	void show(){
		printf(
				"         UID           GID  \n"
				"Real      %d            %d  \n"
				"Effective %d            %d  \n",
				getuid (),     getgid (),
				geteuid(),     getegid()
		);
	}

	int main(void) {
		show();

		setuid(1003);	// try seteuid(1003)

		show();
		return 0;
	}

输出:

			  UID           GID
	Real      0             0
	Effective 0             0
			  UID           GID
	Real      1003          0
	Effective 1003          0

如果改为`seteuid(1003)`:

			  UID           GID
	Real      0             0
	Effective 0             0
			  UID           GID
	Real      0             0
	Effective 1003          0
