---
layout: post
title: "GPT Parition with grub2"
date: 2013-11-25 14:08
comments: true
categories: Linux
---

`MBR` 只能处理大小为 `2T` 以内的硬盘, 针对大小大于 `2T` 的硬盘, 需要改为 `GPT` 分区, 否则多余的空间没法处理.

可以通过 `parted` 的 `mklabel` 子命令来处理.

`Ubuntu`(12.04, 之前的不清楚) 使用的是 `grub2`, 这种情况有点特殊:

> If you have a GPT partition table, you will need a small BIOS boot partition. 1MB is enough. It will hold stage 2 of the bootloader and you don't need to format the partition with a filesystem - grub2-install will overwrite ist anyway.

参考: [Gentoo Wiki - Grub2](http://wiki.gentoo.org/wiki/GRUB2#BIOS.2FMBR_or_BIOS.2FGPT)

需要先分出一个 1MB 的分区, 增加一个 `bios_grub` 标记, 不需要格式化分区.

	(parted) set 1 bios_grub on

<!-- -->

	$ parted -l
	Model: LSI Logical Volume (scsi)
	Disk /dev/sda: 7996GB
	Sector size (logical/physical): 512B/512B
	Partition Table: gpt

	Number  Start   End     Size    File system     Name  Flags
	 1      17.4kB  2000kB  1983kB                        bios_grub
	 2      2097kB  9000MB  8998MB  ext3
	 3      9000MB  309GB   300GB   ext4
	 4      7991GB  7996GB  4995MB  linux-swap(v1)
