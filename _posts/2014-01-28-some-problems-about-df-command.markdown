---
layout: post
title: "Some Problems About df Command"
date: 2014-01-28 09:51
comments: true
categories: Linux
---

<!-- more -->

主要围绕三个问题:

* Why Used + Avail != Size ?
* What is 1K-blocks ?
* How to calculate the Used% ?

最近发现有个机器的某个分区, 在 `df -h` 下看使用情况, 显示已使用和总大小还差几个G, 却显示使用率是100%, 且 `Used + Avail != Size`。

拿本机说明:

	tankywoo@gentoo-jl::~/ » df -h
	Filesystem                   Size  Used Avail Use% Mounted on
	/dev/sda3                     15G  5.9G  8.2G  42% /

	tankywoo@gentoo-jl::~/ » df
	Filesystem                  1K-blocks    Used Available Use% Mounted on
	/dev/sda3                    15481840 6163320   8532088  42% /

上面一个是以 Human Readable 的方式来显示的, 下面是以 1K-blocks的方式显示。

看第一个: 5.9 + 8.2 < 15 , 虽然换算成可读方式会有误差, 但是差的也太多了, 明显有问题。

于是网上搜了下, 才知道有 `Reserved Space` 这个东西。

使用 `tune2fs` 可以看到:

	tankywoo@gentoo-jl::~/ » sudo tune2fs -l /dev/sda3
	tune2fs 1.42 (29-Nov-2011)
		Block count:              3932160
		Reserved block count:     196608
		Free blocks:              1392744
		Block size:               4096

注意 `Reserved block count`, 这个就是保留的空间。

在 `man tune2fs` 里有解释:

> -m reserved-blocks-percentage
> 
> Set  the percentage of the filesystem which may only be allocated by privileged processes.   Reserving some number of filesystem blocks for use by privileged processes is done to avoid filesystem fragmentation, and to allow  system  daemons,  such  as  syslogd(8),  to  continue  to function correctly after non-privileged processes are prevented from writing to the filesystem.  Normally, the default percentage of reserved blocks is 5%.

当文件系统不可写, 比如空间满了, 这些预留的空间就可以保证特权用户(root)进程正常执行。一般会预留 5% 的blocks。

	(15481840 - 6163320 - 8532088) / 15481840 ≈ 5%

计算可以看到, 确实是5%。

当然这个是针对 ext2 / ext3 / ext4 的。[参考](http://simpleans.blogspot.jp/2012/10/reserved-blocks-in-linux.html)

不过就像 man 手册里说的, `tune2fs -m` 可以修改这个大小。

比如:

	# 预留 1% 的空间
	tune2fs -m 1 /dev/sda1
	# 关闭预留空间
	tune2fs -m 0 /dev/sda1

	# 实际操作
	tankywoo@gentoo-jl::~/ » sudo tune2fs -l /dev/sda3 | grep 'Reserved block count'
	Reserved block count:     196608
	tankywoo@gentoo-jl::~/ » sudo tune2fs -m 1 /dev/sda3
	tune2fs 1.42 (29-Nov-2011)
	Setting reserved blocks percentage to 1% (39321 blocks)
	tankywoo@gentoo-jl::~/ » sudo tune2fs -l /dev/sda3 | grep 'Reserved block count'
	Reserved block count:     39321


接着就是另外两个问题了, 前面提到了 `1K-blocks`, 但是它的大小和单位是多少, 我找了半天没找到。

`man df` 只有这句话:

> Disk space is shown in 1K blocks by default, unless the environment variable `POSIXLY_CORRECT` is set, in which case 512-byte blocks are used.

后来去 [Super User](http://superuser.com/questions/707669/what-is-1k-blocks-in-df-and-how-to-calculate-use-percentage) 上求助, 感谢[Sami Laine](http://superuser.com/users/260419/sami-laine) 直接拿出源码说明。

	1450   if (human_output_opts == -1)
	1451     {
	1452       if (posix_format)
	1453         {
	1454           human_output_opts = 0;
	1455           output_block_size = (getenv ("POSIXLY_CORRECT") ? 512 : 1024);
	1456         }
	1457       else
	1458         human_options (getenv ("DF_BLOCK_SIZE"),
	1459                        &human_output_opts, &output_block_size);
	1460     }

配合man手册可以看到, 在设置了 `POSIXLY_CORRECT` 环境变量后, 一个 block 是 512-byte, 没有设置则是默认的 1K blocks, 即一个block 是 1024-byte。

	15481840(blocks) * 1024(B)/blocks / 1024 / 1024 / 1024 = 14.76G(约15G)

最后一个问题, 如何计算出 `Used%`, 即使用率。

因为知道了既然有`Reserved Space`, 那么我先猜测使用率是 Used/Size, 但是这样算出来是约等于39%, 如果加上5%的预留空间, 则又44%了, 始终不是42%。

和上面那个问题一起问的, 也给出了源码:

	 799   bv->used = UINTMAX_MAX;
	 800   bv->negate_used = false;
	 801   if (known_value (bv->total) && known_value (bv->available_to_root))
	 802     {
	 803       bv->used = bv->total - bv->available_to_root;
	 804       bv->negate_used = (bv->total < bv->available_to_root);
	 805     }
	 806 }

不过显然这段代码只说明了 used是如何计算的, 但是并没有使用率的计算, 于是我自己下载了一份 [coreutils](http://www.gnu.org/software/coreutils/) 的源码, 版本8.22。

主要涉及到 `src/df.c` 和 `lib/fsusage.h` 这两个文件。

可以看到:

	 133 /* Displayable fields.  */
	 134 typedef enum
	 135 {
	 136   SOURCE_FIELD, /* file system */
	 137   FSTYPE_FIELD, /* FS type */
	 138   SIZE_FIELD,   /* FS size */
	 139   USED_FIELD,   /* FS size used  */
	 140   AVAIL_FIELD,  /* FS size available */
	 141   PCENT_FIELD,  /* percent used */
	 142   ITOTAL_FIELD, /* inode total */
	 143   IUSED_FIELD,  /* inodes used */
	 144   IAVAIL_FIELD, /* inodes available */
	 145   IPCENT_FIELD, /* inodes used in percent */
	 146   TARGET_FIELD, /* mount point */
	 147   FILE_FIELD    /* specified file name */
	 148 } display_field_t;

percent used 使用enum类型的`PCENT_FILED` 表示。继续搜索这个字段。

	 968         case PCENT_FIELD:
	 969         case IPCENT_FIELD:
	 970           {
	 971             double pct = -1;
	 972             if (! known_value (v->used) || ! known_value (v->available))
	 973               ;
	 974             else if (!v->negate_used
	 975                      && v->used <= TYPE_MAXIMUM (uintmax_t) / 100
	 976                      && v->used + v->available != 0
	 977                      && (v->used + v->available < v->used)
	 978                      == v->negate_available)
	 979               {
	 980                 uintmax_t u100 = v->used * 100;
	 981                 uintmax_t nonroot_total = v->used + v->available;
	 982                 pct = u100 / nonroot_total + (u100 % nonroot_total != 0);
	 983               }
	 984             else

982行显示了这个比例是如何求出的。 `nonroot_total` 是减去 reserved space 后的大小, 也就是这个比例是 used / (total - reserved) 求出来的, 并且只要不是整除, 都会加1。

另外其余部分代码时, 也会看到 free 和 avail, free 是总空闲空间, 也就是 avail + reserved = free。这也是网上有些人说用 gparted 可以看到 free 空间大小。

这几个问题算是之前困扰我有一段时间了, 也一直没抽时间去解决, 现在终于解决了.

> Man doc -> Google -> Source Code -> Ask for help

以后有问题如果手册和网上没有, 有能力的话还是应该直接去分析源码了, 实在不行再提问。
