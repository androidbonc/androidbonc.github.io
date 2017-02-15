---
layout: post
title: "Gentoo /var/db/pkg 导致的包故障"
date: 2016-07-22 20:20
---

昨天在几台Gentoo机器上emerge同时安装某个软件包, 转个头回来一看，大写的懵逼。具体的输出是：

```bash
$ emerge -auv sys-fs/sshfs

These are the packages that would be merged, in order:

Calculating dependencies... done!
[ebuild  N     ] sys-fs/sshfs-2.5::gentoo  134 KiB

Total: 1 package (1 new), Size of downloads: 134 KiB

Would you like to merge these packages? [Yes/No] yes
>>> Verifying ebuild manifests
>>> Emerging (1 of 1) sys-fs/sshfs-2.5::gentoo
>>> Installing (1 of 1) sys-fs/sshfs-2.5::gentoo
>>> Recording sys-fs/sshfs in "world" favorites file...
>>> Jobs: 1 of 1 complete                        Load avg: 0.79, 0.47, 0.48
>>> Auto-cleaning packages...

 app-shells/bash
    selected: 4.3_p42-r1
   protected: 4.3_p33-r2
     omitted: none

 sys-libs/glibc
    selected: 2.21-r2
   protected: 2.20-r2
     omitted: none
...
All selected packages:
...
>>> 'Selected' packages are slated for removal.
>>> 'Protected' and 'omitted' packages will not be removed.
...
>>> Unmerging (154 of 183) sys-libs/glibc-2.21-r2...
...
 * Messages for package sys-libs/glibc-2.21-r2:

 * The ebuild phase 'postrm' has exited unexpectedly. This type of behavior
 * is known to be triggered by things such as failed variable assignments
 * (bug #190128) or bad substitution errors (bug #200313). Normally, before
 * exiting, bash should have displayed an error message above. If bash did
 * not produce an error message above, it's possible that the ebuild has
 * called `exit` when it should have called `die` instead. This behavior
 * may also be triggered by a corrupt bash binary or a hardware problem
 * such as memory or cpu malfunction. If the problem is not reproducible or
 * it appears to occur randomly, then it is likely to be triggered by a
 * hardware problem. If you suspect a hardware problem then you should try
 * some basic hardware diagnostics such as memtest. Please do not report
 * this as a bug unless it is consistently reproducible and you are sure
 * that your bash binary and hardware are functioning properly.
 * The 'postrm' phase of the 'sys-libs/glibc-2.21-r2' package has failed
 * with exit value 1.
 *
 * The problem occurred while executing the ebuild file named
 * 'glibc-2.21-r2.ebuild' located in the '/var/db/pkg/sys-
 * libs/glibc-2.21-r2' directory. If necessary, manually remove the
 * environment.bz2 file and/or the ebuild file located in that directory.
 *
 * Removal of the environment.bz2 file is preferred since it may allow the
 * removal phases to execute successfully. The ebuild will be sourced and
 * the eclasses from the current portage tree will be used when necessary.
 * Removal of the ebuild file will cause the pkg_prerm() and pkg_postrm()
 * removal phases to be skipped entirely.
```

大致就是这样，100多个包被clean了，包括一些系统组件 bash, portage……，以及最重要的glibc。乃们感受一下，这是要赶紧打车去机房救援的节奏啊。

用 Gentoo 3、4年了，第一次遇到安装某个包去卸载其它这么多包，这还得了，以后都不敢装软件了。

虽然已经无法登录了，还好已经登录的几个ssh会话还在，不过命令都残废了，包括`ls`；boss提示可以用busybox开一个sh来同步模板, 因为busybox是静态链接的，不受影响。

于是赶紧切换到`bosybox sh`了。

> 这里可以直接使用`bb`命令，即`busybox bb`，即Make the system rescue shell (/bin/bb) static so you can recover even when glibc is broken；专门用于针对glibc损坏的情况。

查看了下情况，需要的工具如rsync, nc, bash等二进制文件都还在，不过很多动态链接库都没了。

解决办法就是从其它机器把`/lib64`打一个tar包，然后nc传到故障机器，解压后覆盖回去。这时，包括bash, sshd都工作基本ok了，可以远程登录新建shell了。

然后就是和模板同步，恢复一些遗漏的文件。

感谢天、感谢地、感谢busybox ……

---

好吧，上面只是应急修复，但是根源还得找，解决完问题开开心心的赶去球场踢了一个小时球，回来后开始定位。

以前没注意安装完一个包后的提示：

```bash
>>> Auto-cleaning packages...

>>> No outdated packages were found on your system.
```

尤其第二行，默认安装完包后，会自动清理一些临时的安装数据，但是还会检查是否有outdated packages并自动清除。

看了下glibc文件，发现同时属于两个包：

```bash
$ equery b /lib64/libc.so.6
 * Searching for /lib64/libc.so.6 ...
sys-libs/glibc-2.20-r2 (/lib64/libc.so.6 -> libc-2.20.so)
sys-libs/glibc-2.21-r2 (/lib64/libc-2.21.so)
sys-libs/glibc-2.21-r2 (/lib64/libc.so.6 -> libc-2.21.so)

$ ls -alsh /lib64/libc.so.6
0 lrwxrwxrwx 1 root root 12 Feb 18 04:43 /lib64/libc.so.6 -> libc-2.21.so
```

不敢在glibc上乱测试，随便找了一个要删除的包 rsync，看了下版本以及clean信息：

```bash
$ emerge -pv --clean rsync

>>> These are the packages that would be unmerged:

 net-misc/rsync
    selected: 3.1.2
   protected: 3.1.1
     omitted: none

All selected packages: =net-misc/rsync-3.1.2

>>> 'Selected' packages are slated for removal.
>>> 'Protected' and 'omitted' packages will not be removed.


$ emerge --info net-misc/rsync

=================================================================
                        Package Settings
=================================================================

net-misc/rsync-3.1.1::gentoo was built with the following:
USE="acl iconv ipv6 xattr -static" ABI_X86="64"

net-misc/rsync-3.1.2::gentoo was built with the following:
USE="acl iconv ipv6 xattr -static -stunnel" ABI_X86="64"


$ rsync --version
rsync  version 3.1.2  protocol version 31
```

**selected**的是要删除的，**protected** 和 **omitted**的是不被删除的。

就纳闷了为啥新版本会删除，旧版本是受保护的。而且rsync应该是新版本才对。

再仔细看了下当时的报错提示，看到有提到:

```bash
 * The problem occurred while executing the ebuild file named
 * 'glibc-2.21-r2.ebuild' located in the '/var/db/pkg/sys-
 * libs/glibc-2.21-r2' directory. 
```

`/var/db/pkg/`这个目录我以前没注意，[官方解释](https://wiki.gentoo.org/wiki/Directories)是**Portage stores the state of the system.**。维护了系统安装的软件以及相关的信息，包括编译时间、计数器、CFLAGS、ebuild等。`man portage`有更详细的解释。

进去看了下，发现rsync目录有两个:

```bash
$ ls -d net-misc/rsync-3.1.*
net-misc/rsync-3.1.1  net-misc/rsync-3.1.2
```

直觉上是这块的问题，虽然Gentoo支持多版本共存，但是同一个SLOT应该只有一个版本。

测试移除老的目录net-misc/rsync-3.1.1后，-pv --clean就变为OK了，但是移回来又出问题。`strace`跟踪`emerge --info`, `equery b`等信息，发现是会遍历`/var/db/pkg/`目录。

初步已经确定问题出在这个目录。因为太晚，所以找了一台有这个问题的机器，同步到本地虚拟机，然后就回去了。

今天上午来了后，继续排查。主要是找到这个selected和protected的策略是什么。

既然是因为有两个rsync目录，那么问题就在这个目录中某一个文件，于是逐个删除，然后`emerge -pv --clean rsync`看，先开始以为是BUILD_TIME这个文件，不过我看新的包编译事件也新一些，并且删除无效；当删除`COUNTER`这个文件时，就会改为保护的是新的包。问题出在这个文件上！

并且新包的计数器比旧包的计数器小。(这个是因为后来换stage3，相当于编译计数器归0)

然后看portage的源码，搜索COUNTER相关，调用portage/dbapi/vartree.py的cpv_counter函数获取计数器，逻辑代码在\_emerge/unmerge.py的\_unmerge_display函数，其中`unmerge_action == "clean"`一段，会维护一个slotmap和pkgmap字典，如下(因为rsync有依赖，我又换了dos2unix安装测试……)：

```python
# 逻辑代码
for mypkg in vartree.dbapi.cp_list(
    portage.cpv_getkey(mymatch[0])):
    myslot = vartree.getslot(mypkg)
    if myslot not in slotmap:
        slotmap[myslot] = {}
    slotmap[myslot][vartree.dbapi.cpv_counter(mypkg)] = mypkg
    print(">>> slotmap: %s" % slotmap)  # debug

for myslot in slotmap:
    counterkeys = list(slotmap[myslot])
    if not counterkeys:
        continue
    counterkeys.sort()
    pkgmap[mykey]["protected"].add(
        slotmap[myslot][counterkeys[-1]])
    del counterkeys[-1]

    for counter in counterkeys[:]:
        mypkg = slotmap[myslot][counter]
        if mypkg not in mymatch:
            counterkeys.remove(counter)
            pkgmap[mykey]["protected"].add(
                slotmap[myslot][counter])

#be pretty and get them in order of merge:
for ckey in counterkeys:
    mypkg = slotmap[myslot][ckey]
    if mypkg not in all_selected:
        pkgmap[mykey]["selected"].add(mypkg)
        all_selected.add(mypkg)
# ok, now the last-merged package
# is protected, and the rest are selected
print(">>> pkgmap: %s" % pkgmap)  # debug

# 输出信息
>>> slotmap: {u'0': {13953L: u'app-text/dos2unix-6.0.6', 1452L: u'app-text/dos2unix-7.3-r1'}}
>>> pkgmap: [{'omitted': set([]), 'protected': set([u'app-text/dos2unix-6.0.6']), 'selected': set([u'app-text/dos2unix-7.3-r1'])}]
```

当操作是clean(即`--clean`)时，会遍历`/var/db/pkg/`，获取每个包的计数器，一个包一个字典，slotmap中0是slot数，当前情况就是同一个SLOT，有多个包，代码安装计数器排序，因为计数器是编译时递增的，正常来说新包的计数器肯定比旧包要大，所以计数器大的版本被protected, 其余的没有被指定版本保护的，都会被selected并清除。（有一个全局计数器在`/var/cache/edb/counter`，每次编译某个包，全局计数器加1，安装的包的计数器和全局计数器一样大）。

**注**：在这种混乱的情况下，`--depclean`的策略又不一样了，它是会删除旧包，因为它不读COUNTER，具体看代码吧……

问题找到了，再回顾下发生这个的一系列原因：

首先应该之前同步系统部署有问题，rsync覆盖系统时没有做`--delete`清除旧的`/var/db/pkg`目录，并且计数器也被重置过，当然也没想到Gentoo是遍历这个目录维护系统安装包的信息；其次其它包如bash, nc, rsync这些，虽然新版本被clean, 但是因为新旧版本大部分包的文件都是一致的，旧版本被protected导致实际并没有被删掉，但是glibc会被删掉，因为不同版本如libc-2.20.so, libc-2.21.so, 最终都是libc.so.6软链接指向它，所以新版本的动态库是得不到旧版本保护的；

另外，make.conf中，以前是有`AUTOCLEAN`这个选项的，现在`man make.conf`没有给出，但是其实这个选项还是支持的，我的make.conf是几年前的，就提到这个：

```bash
# Automatically clean installed packages after they are updated.
# This option will be removed and forced to yes.
AUTOCLEAN="yes"
```

目前强制为yes, 如果改为no, 则安装完包后是不会做auto clean的，效果就是`/var/db/pkg/`目录也会同时存在两个版本的文件，所以官方说改为no会导致严重问题，后来文档也不给出这个选项。

还好这次问题不算严重，通过busybox得以修复，并且还挖出了这个问题，挺刺激的一次体验 :cry
