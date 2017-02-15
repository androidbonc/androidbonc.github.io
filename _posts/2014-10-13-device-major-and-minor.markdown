---
layout: post
title: "Major and Minor of Device"
date: 2014-10-13 15:00
---

[`/proc/partition`](https://www.centos.org/docs/5/html/5.2/Deployment_Guide/s2-proc-partitions.html)包含了设备的一些信息:

	$ cat /proc/partitions
	major minor  #blocks  name

	   8       48  488386584 sdd
	   8       49  488384001 sdd1
	   8        0  488386584 sda
	   8        1   16777216 sda1
	   8        2  471608344 sda2
	   8       16  488386584 sdb
	   8       17  488385560 sdb1
	   8       32  976762584 sdc
	 254        0  838860800 dm-0
	 254        1    4194304 dm-1
	 254        2  976762584 dm-2
	 254        3  488386584 dm-3
	 254        4  488384001 dm-4

> Each device file has a major ID number and a minor ID number. The major ID identifies the general class of device, and is used by the kernel to look up the appropriate driver for this type of device. The minor ID uniquely identifies a particular device within a general class.[1]

`major` 和 `minor` 分别是设备的主设备号(major number)和次设备号(minor number)

* major number 是一个设备类型的id
* minor number 是针对一个同类型设备作区分

> A device file is a file with type c ( for "character" devices, devices that do not use the buffer cache) or b (for "block" devices, which go through the buffer cache).[2]

设备(类型)分为字符设备`c` 和 块设备`b`

设备类型，主设备号，次设备号都可以通过`ls -l`看到:

	$ ls -l /dev/sda
	brw-rw---- 1 root disk 8, 0 Jun 29 12:23 /dev/sda

关于详细的device类型列表，见[the kernel documentation](https://www.kernel.org/doc/Documentation/devices.txt)


SCSI/ATA设备(`sd*`)的major number是8, 每个设备最多有15个分区, 其中0表示整块设备. 见上面的`/proc/partitions`输出, `sda` 是 `8, 0`, 而`sdb`是从16开始，是`8, 16`.

IDE设备(`hd*`)的major number是3，每个硬盘最多可以有64个分区, 同上

关于磁盘是IDE还是SCSI/ATA，可以通过`smartctl`, `lshw`, `dmesg`等命令查看.

* [The Linux Programming Interface](http://unix.stackexchange.com/questions/124225/are-the-major-minor-number-unique)
* [HOWTO - devices](http://www.tldp.org/HOWTO/Partition/devices.html)
