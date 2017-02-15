---
layout: post
title: "mke2fs missing mtab file problem"
date: 2015-05-29 16:00
---

用livecd部署机器, livecd没有lvm软件包相关命令, 但是部署的系统里有.

所以在装了根分区后, 通过chroot到部署系统, 创建lv, 然后mke2fs格式化分区(ext4):

    mke2fs -t ext4 -L /home /dev/vg_data/lv_home

不过出现了报错:

    Creating journal (xxx blocks): mke2fs: Can't check if filesystem is mounted due 
    to missing mtab file while trying to create journal

![mke2fs-mtab-problem-screenshot](https://tankywoo-wb.b0.upaiyun.com/mke2fs-mtab-problem-screenshot.png!small)

原因是`/etc/mtab`文件没有, 因为之前通过rsync module同步时, 这个文件在exclude列表里.

通过`blkid`可以看到, 格式化分区是失败的, 并没有这个分区.

这时尝试mount肯定是失败的, 不过这个过程是建立一个空的`/etc/mtab`文件, 当`/etc/mtab`文件存在时, 就可以正常执行mke2fs格式化分区了.

当然也可以手动touch一个空文件, 或者:

    grep -v rootfs /proc/mounts > /etc/mtab

---

关于`/etc/fstab`和`/etc/fstab`:

`/etc/fstab`一般是手动配置好的静态内容的文件, 系统启动时通过读这个文件将设备挂载到正确的挂载点.

`/etc/mtab`则是一个动态的文件, 显示的是当前挂载的设备, 通过`mount`和`umount`命令都会导致这个文件的改变. 格式上和`/etc/fstab`是一样的. 不过第5列和第6列是无意义的, 都是0.

stackoverflow上有两篇回答不错, 引用下.

[回答1](http://serverfault.com/a/267612/173472):


> **mtab** lists currently mounted file systems and is used by the **mount** and **unmount** commands when you want to list your mounts or unmount all.  It's not used by the kernel, which maintains its own list (in /proc/mounts or /proc/self/mounts).  Its structure is the same as [fstab (see manpage)](http://linux.die.net/man/5/fstab).
> 
> Separated by whitespace, its 6 columns are:
> 
>  1. Mount device if applicable
>  2. Mount point
>  3. File system
>  4. Mount options
>  5. Used by the dump command, 0 to ignore
>  6. Used by the fsck command (which order to check at boot), 0 to ignore
> 
> To clarify, mtab *does* contain values in the 5th and 6th columns in order to have the same structure as fstab, even though these columns are only meaningful when used in fstab.


[回答2](http://serverfault.com/a/267615/173472):

> The `/etc/mtab` file shares the same structure as `/etc/fstab`. According to [this site](http://www.tuxfiles.org/linuxhelp/fstab.html) the 5th and 6th column in `/etc/fstab` are used to store "Dump and fsck options". The 5th column is used to determine if dumping of the partition should be made, and the 6th to decide if an fsck must be processed on the partition.
> 
> In `/etc/mtab`, however, this two options loose their sense. Indeed, these two options are used when mounting the partitions, and `/etc/mtab` lists the partitions that are already mounted. If I understand it correctly, these option are not useful in `/etc/mtab`. They may be here for compatibility reasons with `/etc/fstab`, as the content of `/etc/mtab` must be directly usable in `/etc/fstab`
