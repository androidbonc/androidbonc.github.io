---
layout: post
title: "LVM Resize"
date: 2015-06-13 23:00
---

之前一篇 [use lvm]({% post_url 2013-12-12-use-lvm %}) 总结了lvm的pv/vg/lv创建使用等基本方法.

这里总结下lv的reduce/extend等方法.

基本环境: /dev/sda3, /dev/sda4 分别1G大小的pv

初始将/dev/sda3加入到vg:

	$ vgcreate vg_data /dev/sda3

默认PE是4MB, 所以1G有255个PE

创建lv, 大小分配125个PE

	$ lvcreate -l 125 -n lv_data vg_data

这里也可以通过百分比来创建, 如:

	$ lvcreate -l 50%VG -n lv_data vg_data

当前的状态:

	$ pvdisplay /dev/sda3
	  --- Physical volume ---
	  PV Name               /dev/sda3
	  VG Name               vg_data
	  PV Size               1.00 GiB / not usable 4.00 MiB
	  Allocatable           yes
	  PE Size               4.00 MiB
	  Total PE              255
	  Free PE               130
	  Allocated PE          125
	  PV UUID               0ife1n-hdHA-m6gA-rjCE-uyPD-tzaS-LE8jKo

	$ vgdisplay
	  --- Volume group ---
	  VG Name               vg_data
	  System ID
	  Format                lvm2
	  Metadata Areas        1
	  Metadata Sequence No  4
	  VG Access             read/write
	  VG Status             resizable
	  MAX LV                0
	  Cur LV                1
	  Open LV               0
	  Max PV                0
	  Cur PV                1
	  Act PV                1
	  VG Size               1020.00 MiB
	  PE Size               4.00 MiB
	  Total PE              255
	  Alloc PE / Size       125 / 500.00 MiB
	  Free  PE / Size       130 / 520.00 MiB
	  VG UUID               ZieGlO-7dJM-1qVh-zMjF-MugH-qC0a-nVGPOU

	$ lvdisplay
	  --- Logical volume ---
	  LV Path                /dev/vg_data/lv_data
	  LV Name                lv_data
	  VG Name                vg_data
	  LV UUID                eM1pNB-v36r-26H4-yc9I-fFse-IlZQ-G2eJbx
	  LV Write Access        read/write
	  LV Creation host, time gentoo-local, 2015-05-25 07:29:25 +0800
	  LV Status              available
	  # open                 0
	  LV Size                500.00 MiB
	  Current LE             125
	  Segments               1
	  Allocation             inherit
	  Read ahead sectors     auto
	  - currently set to     256
	  Block device           254:0

显示lv大小500M, vg总大小1020M

格式化后挂载到/mnt/lvm下

	$  df -lh
	Filesystem                   Size  Used Avail Use% Mounted on
	...
	/dev/mapper/vg_data-lv_data  485M   11M  449M   3% /mnt/lvm

## 扩容 ##

使用`lvresize`扩容, 加100个PE:

	$ lvresize -l +100 /dev/vg_data/lv_data
	  Extending logical volume lv_data to 900.00 MiB
	  Logical volume lv_data successfully resized

	$ pvdisplay /dev/sda3
	  --- Physical volume ---
	  PV Name               /dev/sda3
	  VG Name               vg_data
	  PV Size               1.00 GiB / not usable 4.00 MiB
	  Allocatable           yes
	  PE Size               4.00 MiB
	  Total PE              255
	  Free PE               30
	  Allocated PE          225
	  PV UUID               0ife1n-hdHA-m6gA-rjCE-uyPD-tzaS-LE8jKo

	$ lvdisplay
	  --- Logical volume ---
	  LV Path                /dev/vg_data/lv_data
	  LV Name                lv_data
	  VG Name                vg_data
	  LV UUID                eM1pNB-v36r-26H4-yc9I-fFse-IlZQ-G2eJbx
	  LV Write Access        read/write
	  LV Creation host, time gentoo-local, 2015-05-25 07:29:25 +0800
	  LV Status              available
	  # open                 1
	  LV Size                900.00 MiB
	  Current LE             225
	  Segments               1
	  Allocation             inherit
	  Read ahead sectors     auto
	  - currently set to     256
	  Block device           254:0

	$ df -h
	Filesystem                   Size  Used Avail Use% Mounted on
	...
	/dev/mapper/vg_data-lv_data  485M   11M  449M   3% /mnt/lvm

lvdisplay显示LV大小变了, 但是df看到实际还没变.

这里使用`dumpe2fs`可以看到文件系统block的使用情况:

	$ dumpe2fs /dev/vg_data/lv_data

使用`resize2fs`来进行实际扩容, 加到700M:

	$ resize2fs /dev/vg_data/lv_data 700M
	resize2fs 1.42 (29-Nov-2011)
	Filesystem at /dev/vg_data/lv_data is mounted on /mnt/lvm; on-line resizing required
	old_desc_blocks = 2, new_desc_blocks = 3
	The filesystem on /dev/vg_data/lv_data is now 716800 blocks long.

	$ df -lh
	Filesystem                   Size  Used Avail Use% Mounted on
	...
	/dev/mapper/vg_data-lv_data  678M   11M  635M   2% /mnt/lvm

注意这里, resize2fs 可以进行在线(on-line)扩容.

## 缩容 ##

缩容是扩容的**逆过程**, 操作大部分类似, 不过无法进行在线缩容, 且缩容要注意的就是剩余的空间是否能放下所有原来的数据, 以及数据迁移的问题.

一个使用场景: 现在/dev/sda3, /dev/sda4都加入到lv中了, 需要将/dev/sda3取下来, 只留下/dev/sda4

接着上面的操作, 来初始当前的环境, 把/dev/sda3剩余PE和/dev/sda4的所有PE都给LV扩容:

	$ vgextend vg_data /dev/sda4
	  Volume group "vg_data" successfully extended

	$ lvresize -l +285 /dev/vg_data/lv_data
	  Extending logical volume lv_data to 1.99 GiB
	  Logical volume lv_data successfully resized

	$ resize2fs /dev/vg_data/lv_data  # 不接size则默认使用所有剩余空间扩容
	resize2fs 1.42 (29-Nov-2011)
	Filesystem at /dev/vg_data/lv_data is mounted on /mnt/lvm; on-line resizing required
	old_desc_blocks = 5, new_desc_blocks = 8
	The filesystem on /dev/vg_data/lv_data is now 2088960 blocks long.

	$ df -h
	Filesystem                   Size  Used Avail Use% Mounted on
	...
	/dev/mapper/vg_data-lv_data  2.0G   11M  1.9G   1% /mnt/lvm

创建一个300M的数据:

	$ dd if=/dev/zero of=/mnt/lvm/a.block bs=1000000 count=300

/dev/sda3的PE是255个, 现在要将/dev/sda3移除, 先通过`resize2fs`进行实际容量缩小:

	$ resize2fs /dev/vg_data/lv_data 1000M
	resize2fs 1.42 (29-Nov-2011)
	Filesystem at /dev/vg_data/lv_data is mounted on /mnt/lvm; on-line resizing required
	resize2fs: On-line shrinking not supported

	$ umount /mnt/lvm

	$ resize2fs /dev/vg_data/lv_data 1000M
	resize2fs 1.42 (29-Nov-2011)
	Please run 'e2fsck -f /dev/vg_data/lv_data' first.

	$ e2fsck -f /dev/vg_data/lv_data
	e2fsck 1.42 (29-Nov-2011)
	Pass 1: Checking inodes, blocks, and sizes
	Pass 2: Checking directory structure
	Pass 3: Checking directory connectivity
	Pass 4: Checking reference counts
	Pass 5: Checking group summary information
	/dev/vg_data/lv_data: 12/518160 files (0.0% non-contiguous), 369565/2088960 blocks

	$ resize2fs /dev/vg_data/lv_data 1000M
	resize2fs 1.42 (29-Nov-2011)
	Resizing the filesystem on /dev/vg_data/lv_data to 1024000 (1k) blocks.
	The filesystem on /dev/vg_data/lv_data is now 1024000 blocks long.

可以看到, `resize2fs`不能进行在线缩容, 且缩容前还需要`e2fsck`检查磁盘

重新挂载上:

	$ mount /dev/vg_data/lv_data /mnt/lvm

	$ df -lh
	Filesystem                   Size  Used Avail Use% Mounted on
	...
	/dev/mapper/vg_data-lv_data  969M  297M  630M  33% /mnt/lvm

`lvresize`减小LV容量:

	$ lvresize -l -255 /dev/vg_data/lv_data
	  WARNING: Reducing active and open logical volume to 1020.00 MiB
	  THIS MAY DESTROY YOUR DATA (filesystem etc.)
	Do you really want to reduce lv_data? [y/n]: y
	  Reducing logical volume lv_data to 1020.00 MiB
	  Logical volume lv_data successfully resized

	$ lvdisplay
	  --- Logical volume ---
	  LV Path                /dev/vg_data/lv_data
	  LV Name                lv_data
	  VG Name                vg_data
	  LV UUID                eM1pNB-v36r-26H4-yc9I-fFse-IlZQ-G2eJbx
	  LV Write Access        read/write
	  LV Creation host, time gentoo-local, 2015-05-25 07:29:25 +0800
	  LV Status              available
	  # open                 1
	  LV Size                1020.00 MiB
	  Current LE             255
	  Segments               1
	  Allocation             inherit
	  Read ahead sectors     auto
	  - currently set to     256
	  Block device           254:0

	$ pvdisplay
	  --- Physical volume ---
	  PV Name               /dev/sda3
	  VG Name               vg_data
	  PV Size               1.00 GiB / not usable 4.00 MiB
	  Allocatable           yes (but full)
	  PE Size               4.00 MiB
	  Total PE              255
	  Free PE               0
	  Allocated PE          255
	  PV UUID               0ife1n-hdHA-m6gA-rjCE-uyPD-tzaS-LE8jKo

	  --- Physical volume ---
	  PV Name               /dev/sda4
	  VG Name               vg_data
	  PV Size               1.00 GiB / not usable 4.00 MiB
	  Allocatable           yes
	  PE Size               4.00 MiB
	  Total PE              255
	  Free PE               255
	  Allocated PE          0
	  PV UUID               gp2cuI-9g7g-KPXk-jbVH-fKqC-3mV0-5jN7yV

因为/dev/sda4是后添加的, 这里减少LV空间, 释放的PE实际是/dev/sda4的PE

接着通过`pvmove`把/dev/sda3的PE移到/dev/sda4:

	$ pvmove /dev/sda3 /dev/sda4
	  /dev/sda3: Moved: 1.6%
	  /dev/sda3: Moved: 100.0%

	$ pvdisplay
	  --- Physical volume ---
	  PV Name               /dev/sda3
	  VG Name               vg_data
	  PV Size               1.00 GiB / not usable 4.00 MiB
	  Allocatable           yes
	  PE Size               4.00 MiB
	  Total PE              255
	  Free PE               255
	  Allocated PE          0
	  PV UUID               0ife1n-hdHA-m6gA-rjCE-uyPD-tzaS-LE8jKo

	  --- Physical volume ---
	  PV Name               /dev/sda4
	  VG Name               vg_data
	  PV Size               1.00 GiB / not usable 4.00 MiB
	  Allocatable           yes (but full)
	  PE Size               4.00 MiB
	  Total PE              255
	  Free PE               0
	  Allocated PE          255
	  PV UUID               gp2cuI-9g7g-KPXk-jbVH-fKqC-3mV0-5jN7yV

然后进行一些收尾操作:

	$  vgreduce vg_data /dev/sda3
	  Removed "/dev/sda3" from volume group "vg_data"

	$ pvremove /dev/sda3
	  Labels on physical volume "/dev/sda3" successfully wiped

## 其它 ##

* `pvdisplay -m` 可以看到哪些PE和LV/LE的对应关系

## 参考 ##

* 鸟哥私房菜
* [How to Manage and Use LVM (Logical Volume Management) in Ubuntu](http://www.howtogeek.com/howto/40702/how-to-manage-and-use-lvm-logical-volume-management-in-ubuntu/)
