---
layout: post
title: "ulimit相关小结"
date: 2015-08-12 17:00
---

`ulimit`经常用到控制core file size, max open file等, 它是一个shell builtin命令.

`ulimit -a`可以看到当前shell的所有ulimit配置, 并输出每一项的参数命令.

比如core file size的参数是`-c`, 则:

	# 输出当前shell的core file size 设置
	ulimit -c

	# 设置当前shell的core file size, 包括soft和hard
	ulimit -c xxx

	# 设置soft core file size (hard的参数是-H)
	ulimit -S -c xxx

ulimit设置的可以是一个数字, 或soft/hard/unlimited, 分表表示当前的soft值, hard值或者无限制

关于ulimit的soft limit和hard limit:

hard limit只能被root用户/进程增大, soft limit可以被任何用户/进程增大.

soft limit最大不能超过hard limit.

具体的解释可以看看来自[stackexchange](http://unix.stackexchange.com/questions/29577/ulimit-difference-between-hard-and-soft-limits)的这个回答:

> A hard limit can only be raised by root (any process can lower it). So it is useful for security: a non-root process cannot overstep a hard limit. But it's inconvenient in that a non-root process can't have a lower limit than its children.
> 
> A soft limit can be changed by the process at any time. So it's convenient as long as processes cooperate, but no good for security.
> 
> A typical use case for soft limits is to disable core dumps (`ulimit -Sc 0`) while keeping the option of enabling them for a specific process you're debugging (`(ulimit -Sc unlimited; myprocess)`).
> 
> The ulimit shell command is a wrapper around the `setrlimit` system call, so that's where you'll find the definitive documentation.
> 
> Note that some systems may not implement all limits. Specifically, some systems don't support per-process limits on file descriptors (Linux does); if yours doesn't, the shell command may be a no-op.

网上关于更改ulimit控制的max open file, core file size等, 或多或少我觉得都有些问题.

首先, `ulimit -a`看的是当前shell的配置, 基于此shell新建的进程都会和这个一样.

但是, **ulimit -X xxx是针对当前的shell**, 并不是全局的, 比如退出后重新登录, 则还原了.

另外, 比如有人认为某个程序没有开启core dump, 直接看`ulimit -c`输出0, 则认为没有开启, 这个是错误的认识.

ulimit和进程绑定的, 每个进程不一样, 有的支持的自己的配置文件中开启. 具体要看: `/proc/<pid>/limits`的内容.

还有人说配置在`/etc/profile`或`~/.bashrc`, 这个应该只针对当前的login shell, 对其它进程并无用.

在Ubuntu下(其它发行版还没研究 TODO), 全局的ulimit配置在`/etc/security/limits.conf`:

#   <domain>        <type>  <item>  <value>
	root             soft    core    unlimited
	root             hard    core    unlimited
	*                soft    core    unlimited
	*                hard    core    unlimited

具体可以看这个文件, 注释信息已经讲得很清晰了.

在这里, hard 其实可以不用配, 因为系统默认的core hard就是unlimited

另外, 注意, 这里的domain, 要配上通配符和root:

> NOTE: group and wildcard limits are not applied to root.
>
> To apply a limit to the root user, <domain> must be
>
> the literal username root.

编辑后, 退出当前shell, 重新登录, ulimit -c会看到全局生效了, 不需要重启机器, [参考](do changes in /etc/security/limits.conf require a reboot?)

关于core dump的打开, 编辑/etc/security/limits.conf后, 保存重启. 有以下一些现象和猜测, 暂时没有理论依据, 可能是错的:

* init(1)进程的core file还是0, 这个可以理解, limit.conf的加载在此之后
* 其它进程的ppid是1的, core file也是0
* 比如当前nginx在运行, 重启nginx, 则proc下limit中的core file变为unlimited; 如果撤销/etc/security/limits.conf, 重启nginx又变为0; 这块应该是读取了系统全局的ulimit设置
* 针对daemontools, 重启svscanboot, 也无济于事, 可能部分软件本身不支持修改ulimit; 不过, 一般正常的情况也不会这么做; 一般都是针对单个service, 在run脚本里起始处加上ulimit -X xxx配置即可.

这块可以研究的东西还是挺多的, mark一个TODO

另外, sysctl 控制core输出的格式(路径), 可以是绝对路径, 可以是当前路径, 默认是core, 表示当前的工作路径(/proc/<pid>/cwd/):

	$ sysctl -a | grep core_pattern
	kernel.core_pattern = core

这样新产生的core dump会覆盖原来的, 可以配上如:

	kernel.core_pattern = core.%e.%p.%h.%t

	kernel.core_pattern = /home/cores/core.%e.%p.%h.%t

也可以直接写proc文件:

	echo /home/cores/core.%e.%p.%h.%t > /proc/sys/kernel/core_pattern

下面这个测试代码可以产生core dump:

	#include <stdio.h>

	int main()
	{
		int *null_ptr = NULL;
		*null_ptr = 10;            //对空指针指向的内存区域写,会发生段错误
		return 0;
	}

没开启core dump和开启core dump, 发生段错误时输出是不一样的:

	$ ./test_core
	Segmentation fault

	ulimit -c unlimited

	$ ./test_core
	Segmentation fault (core dumped)

这篇[文章](http://www.cnblogs.com/hazir/p/linxu_core_dump.html)整理的挺不错的.
