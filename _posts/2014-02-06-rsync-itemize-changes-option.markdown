---
layout: post
title: "Rsync -i/--itemize-changes Option"
date: 2014-02-06 16:15
comments: true
categories: Linux
---

<!-- more -->

又一个在TODO里放了很久的任务，一直准备把`rsync`的`-i/--itemize-changes` 选项小结下, 看日期是2013/12/12号建的，拖到了今天，惭愧！

我习惯的rsync短参数组合选项是`-hvaiHEXA`，`-a`等价于`-rlptgoD`。不过rsync不同的版本支持的参数不一样，比如像`-X`和`-A`在2.6.9下测试就不支持。

`-i/--itemize-changes` 选项很强大，我认为可以说是必选的选项。因为这个选项可以看到哪些文件被同步了，已经修改了哪些内容/属性。我使用rsync命令的次数也很多了，包括有时多台虚拟机之间同步同一个系统等，就遇到过一些问题，印象中当时是/etc/sudoers文件被设置了`-i`权限([chattr](http://linux.die.net/man/1/chattr), mac下用`chflags`命令)，导致当时复制过来的模板系统有问题，后来检查后就是通过这里以及相关的输出信息看出来了。

------

**声明**：

rsync 的版本不同，很多都有变化，这里参考的的是 `2.6.9` 下的man手册和程序。

比如在gentoo下我使用的是 `rsync 3.0.9`, 则输出的信息长度是11位。所以一定要根据当前的版本和文档来确定。

`-i/--itemize-changes`的效果等价于`--out-format='%i %n%L'`。默认不会输出未更新的文件，使用两个`-i` 可以输出未更新文件。

**注**: 在`2.6.9`版本下有问题，虽然文档说不会输出，但实际输出了未更新文件，而在`3.0.9`下测试则是按照文档描述显示的。

它控制的输出信息是9个字符的长度，格式是`YXcstpogz`。

其中Y和X都是替换符, 每个都有几个可选的字符使用。

`Y` 控制更新的类型:

* `<` 表示文件被传送到远程一端(send)
* `>` 表示文件被传送到本地一端(received)
* `c` 表示item有修改/新建, 比如新建目录, 软链接变化等
* `h` 表示是一个硬链接(依赖--hard-links选项)
* `.` 表示文件没有被更新（尽管它的属性可能被修改)

`c` 这个我也不是很明白, 原文是:

> A c means that a local change/creation is occurring for the item(such as the creation of a directory or the changing of a symlink, etc.).

首先不明白这里用到的 `item` 和上面的`>/<` 里的 `file` 有什么区别；所以这里的修改新建等不知和文件的修改新建有何区别，因为文件的修改新建等都是`>` 或 `<`。

个人猜测这里的 item 应该指除了 file 以外的, 比如 directory, soft/hard link等。

另外一个就是 `.`，这里也有点疑问, 想不出有哪些属性会被修改？ **TODO**

`X` 控制文件类型:

* `f` 文件(file)
* `d` 目录(directory)
* `L` 软链接(symlink)
* `D` 设备文件(device)
* `S` 特殊文件, 比如套接字(sockets)和有名管道(fifos)

后面7位都表示实际的字符, 如果相应的属性被更新, 则输出响应位置的字符, 否则输出`.`表示未更新。有三个例外的情况:

* 一个新建的文件, 每一位都是`+`
* 如果是同一个文件(即没变化)，每一位都是` ` (空格)
* 如果有未知的属性, 则每一位都是`?`(这个一般出现在和老版本rsync通讯时)

下面说明剩下7个字符的含义(括号表示需要使用的选项, 除了c, 其余的都已经被-a选项包含了):

* `c` 表示使用128位的MD4 checksum检查文件不一样(--checksum)
* `s` 表示文件大小不一样
* `t` 表示 modification time 不一样(-t/--times)
* `p` 表示权限不一样(-p/--perms)
* `o` 表示属主不一样(-o/--owner, 且需要超级用户权限)
* `g` 表示所属用户组不一样(-g/--group, 且需要设置用户组的权限)
* `z` 保留位, 保留给以后的属性用

举例:

	# 两个目录 a 和 b
	# 其中 a/f1 和 b/f1 内容不一样
	# a/f2 内容和属性和 b/f2 一样
	# f5 是指向f1的硬链接
	# c 是一个目录
	TankyWoo@Mac-OS::/tmp/ » tree a
	a
	├── c                    # 目录
	├── f1
	├── f2
	├── f3
	├── f4 -> /tmp/a/f1
	└── f5

	1 directory, 4 files
	TankyWoo@Mac-OS::/tmp/ » tree b
	b
	├── f1
	├── f2
	└── f4 -> /tmp/b/f2

	0 directories, 3 files

	TankyWoo@Mac-OS::/tmp/ » rsync -hvaiHE --checksum  a/ b/ -n
	building file list ... done
	.d..t.... ./
	>fcst.... f1
	.f        f2                   # 什么都没有更新
	>f+++++++ f3                   # 新建 f3 文件
	cL..T.... f4 -> /tmp/a/f1      # symlink有变化
	hf+++++++ f5 => f1             # h指示为硬链接
	cd+++++++ c/                   # 新建目录c

	sent 287 bytes  received 65 bytes  704.00 bytes/sec
	total size is 57  speedup is 0.16

