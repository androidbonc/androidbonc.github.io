---
layout: post
title: "Linux Increase Partition Space"
date: 2014-01-12 15:19
comments: true
categories: Linux
---

<!-- more -->

对于做了lvm的分区，扩容比较方便。

非lvm分区，如果想保证在数据不丢失的情况下扩容，如果是 `ext2` / `ext3` / `ext4` 的格式，保证 **分区的起始位置不变** 的情况下，只改变结束位置，就可以通过 `resize2fs` 进行扩容/缩容。

一般的情况下是先unmount掉需要扩容的分区(通过 `lsof` 查看有哪些进程在使用指定分区)，当然，针对 `ext3` / `ext4` 的分区，在 `Linux Kernel 2.6` 已经支持了在线扩容（NOTE: on-line resize只支持扩容，不支持缩容）。(man resize2fs):

> Modern Linux 2.6 kernels will support on-line resize for file systems mounted using ext3 and ext4; ext3 file systems will require the use of file systems with the resize_inode feature enabled.

扩容主要的步骤:

0.比如虚拟机的情况下，一般在虚拟机配置上直接增加硬盘的空间；印象中以前`fdisk`可以直接看到增大后的空间大小，如果看不到，可以执行：

	echo 1 > /sys/block/sdX/device/rescan

参考[How do I get Centos VM to re-read its increased Disk size WITHOUT a reboot](http://serverfault.com/questions/306737/how-do-i-get-centos-vm-to-re-read-its-increased-disk-size-without-a-reboot)

1.修改分区表结束位置:

使用 `fdisk` / `parted` 先删除掉原来的分区，然后重新新建分区，保证分区的起始位置不变，只增大结束的位置。

2.`partprobe` 通知操作系统内核分区表有改动，重读分区表。

3.`e2fsck` 检查分区，保证没问题:

	e2fsck -f /dev/sdb1

4.`resize2fs` 扩容:

	resize2fs /dev/sdb1

5.最后重新挂载上去, `df -lTh` 确认下.

---

2016-09-07:

给vcenter server扩容，内核目前是3.0.34，分区是ext3，开启了`resize_inode`特性。按理说是可以支持on-line increase，但是实际测试时还是不行。

比如我扩容postgres db存储分区，停掉几个服务：

	service vmware-vpostgres stop
	service vmware-vpxd stop

然后卸载分区，其余步骤同上。





