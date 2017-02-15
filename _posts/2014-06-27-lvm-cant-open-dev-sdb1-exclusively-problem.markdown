---
layout: post
title: "LVM 'Can’t open /dev/sdb1 exclusively. Mounted filesystem?' Problem"
date: 2014-06-27 16:00
categories: Linux
---

<!-- more -->

在将几块盘做LVM时，遇到一个之前都没遇到过的问题:

	root@ubuntu:~# pvcreate /dev/sdc1
	  Can't open /dev/sdc1 exclusively.  Mounted filesystem?

首先第一反应就是查看这个分区是否已经在使用了，但是没有。

查看硬盘的一些信息:

	root@ubuntu:~# cat /proc/partitions
	major minor  #blocks  name

	   8        0  488386584 sda
	   8        1   16777216 sda1
	   8        2  471608344 sda2
	   8       32  488386584 sdc
	   8       33  488386584 sdc1
	   8       16  488386584 sdb
	   8       17  488385560 sdb1
	   8       48  488386584 sdd
	   8       49  488384001 sdd1
	 254        0  838860800 dm-0
	 254        1    4194304 dm-1
	 254        2  488386584 dm-2
	 254        3  488386584 dm-3
	 254        5  488384001 dm-5
	 254        4  488384001 dm-4


	root@ubuntu:~# fdisk /dev/sdc -l

	Disk /dev/sdc: 500.1 GB, 500107862016 bytes
	81 heads, 63 sectors/track, 191411 cylinders, total 976773168 sectors
	Units = sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes
	Disk identifier: 0xbbbab9b8

	   Device Boot      Start         End      Blocks   Id  System
	/dev/sdc1            2048   976773167   488385560   8e  Linux LVM

接着看一些底层的信息:

dmsetup 是一个底层的逻辑卷管理， dm 应该是 `Device Mapper`的简称。

	root@ubuntu:~# dmsetup status
	35000c50026716847: 0 976773168 multipath 2 0 0 0 1 1 A 0 1 0 8:48 A 0
	vg_data-lv_home: 0 976764928 linear
	vg_data-lv_home: 976764928 700956672 linear
	35000c5002670f03e: 0 976773168 multipath 2 0 0 0 1 1 A 0 1 0 8:32 A 0
	35000c5002670f03e-part1: 0 976768002 linear
	35000c50026716847-part1: 0 976768002 linear
	vg_data-lv_swap: 0 8388608 linear


	root@ubuntu:~# dmsetup ls
	35000c50026716847       (254, 2)
	vg_data-lv_home (254, 0)
	35000c5002670f03e       (254, 3)
	35000c5002670f03e-part1 (254, 5)
	35000c50026716847-part1 (254, 4)
	vg_data-lv_swap (254, 1)

可以看到 35000c5002670f03e 和 35000c50026716847 组成了multipath(多路径)

	root@ubuntu:~# multipath -ll
	35000c50026716847 dm-2 ATA,GB0500EAFJH
	size=466G features='0' hwhandler='0' wp=rw
	`-+- policy='round-robin 0' prio=1 status=active
	  `- 3:0:0:0 sdd 8:48 active ready running
	35000c5002670f03e dm-3 ATA,GB0500EAFJH
	size=466G features='0' hwhandler='0' wp=rw
	`-+- policy='round-robin 0' prio=1 status=active
	  `- 2:0:0:0 sdc 8:32 active ready running

	root@ubuntu:~# ll /dev/mapper/
	total 0
	drwxr-xr-x  2 root root     180 Jun 28 01:39 ./
	drwxr-xr-x 14 root root   13060 Jun 28 17:17 ../
	lrwxrwxrwx  1 root root       7 Jun 28 01:39 35000c5002670f03e -> ../dm-3
	lrwxrwxrwx  1 root root       7 Jun 28 01:39 35000c5002670f03e-part1 -> ../dm-5
	lrwxrwxrwx  1 root root       7 Jun 28 01:39 35000c50026716847 -> ../dm-2
	lrwxrwxrwx  1 root root       7 Jun 28 01:39 35000c50026716847-part1 -> ../dm-4
	crw------T  1 root root 10, 236 Jun 28 01:39 control
	lrwxrwxrwx  1 root root       7 Jun 28 01:39 vg_data-lv_home -> ../dm-0
	lrwxrwxrwx  1 root root       7 Jun 28 01:39 vg_data-lv_swap -> ../dm-1

使用 `dmsetup remove xxx` 移除掉就可以创建PV了:

	root@ubuntu:~# dmsetup remove 35000c5002670f03e-part1
	root@ubuntu:~# dmsetup remove 35000c5002670f03e

	root@ubuntu:~# pvcreate /dev/sdc1
	  Physical volume "/dev/sdc1" successfully created

也可以使用`dmsetup remove_all`移除所有。

TODO: 继续研究
