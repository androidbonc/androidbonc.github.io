---
layout: post
title: "LVM Found duplicate PV Problem"
date: 2014-06-27 21:10
categories: Linux
---

<!-- more -->


	root@cdn-tpl:~# pvscan
	  PV /dev/sda2                      lvm2 [449.76 GiB]
	  Total: 1 [449.76 GiB] / in use: 0 [0   ] / in no VG: 1 [449.76 GiB]
	root@cdn-tpl:~# pvcreate /dev/sdb1
	  Physical volume "/dev/sdb1" successfully created
	root@cdn-tpl:~# pvscan
	  Found duplicate PV DWs4H1LUS5bBEUTS7FI2TPzDhj1VlzCF: using /dev/sdb1 not /dev/sdb
	  PV /dev/sda2                      lvm2 [449.76 GiB]
	  PV /dev/sdb1                      lvm2 [465.76 GiB]
	  Total: 2 [915.52 GiB] / in use: 0 [0   ] / in no VG: 2 [915.52 GiB]
	root@cdn-tpl:~# pvremove /dev/sdb1
	  Found duplicate PV DWs4H1LUS5bBEUTS7FI2TPzDhj1VlzCF: using /dev/sdb not /dev/sdb1
	  Labels on physical volume "/dev/sdb1" successfully wiped

建立

root@cdn-tpl:~# fdisk /dev/sdb -l

Disk /dev/sdb: 500.1 GB, 500107862016 bytes
81 heads, 63 sectors/track, 191411 cylinders, total 976773168 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0xbfa82375

   Device Boot      Start         End      Blocks   Id  System
/dev/sdb1            2048   976773167   488385560   8e  Linux LVM





root@cdn-tpl:~# fdisk /dev/sdb -l

Disk /dev/sdb: 500.1 GB, 500107862016 bytes
255 heads, 63 sectors/track, 60801 cylinders, total 976773168 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00000000

Disk /dev/sdb doesn't contain a valid partition table
