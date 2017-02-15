---
layout: post
title: "Linux history Command"
date: 2013-11-26 03:12
comments: true
categories: Linux
---

<!-- more -->

`Bash` 提供了两个命令 `shell builtin` 命令来管理 history, 一个是 `fc`, 一个是 `history`

	tankywoo@gentoo-jl ~ $ echo $SHELL
	/bin/bash
	tankywoo@gentoo-jl ~ $ type history
	history is a shell builtin
	tankywoo@gentoo-jl ~ $ type fc
	fc is a shell builtin

可以通过配置 `HISTTIMEFORMAT` 环境变量来配置输出的时间格式.

在 `Zsh` 下, history 就是 `fc -l`

	tankywoo@gentoo-jl::~/ » echo $SHELL 
	/bin/zsh
	tankywoo@gentoo-jl::~/ » type history
	history is an alias for fc -l
	tankywoo@gentoo-jl::~/ » type fc
	fc is a shell builtin

在 `Zsh` 下, 键入 `fc -l -` 然后 `Tab` 使用 `Auto Completion` 功能:

	tankywoo@gentoo-jl::~/ » fc -l -
	-D               -- print elapsed times
	-E               -- dd.mm.yyyy format time-stamps
	-d               -- print time-stamps
	-f               -- mm/dd/yyyy format time-stamps
	-i               -- yyyy-mm-dd format time-stamps
	-m               -- treat first argument as a pattern
	-n               -- suppress line numbers
	-r               -- reverse order of the commands

另外, fc 还有一个用法:

	fc -l 20 30      # List commands 20 throuth 30
	fc -l -5         # List the last five commands
	fc -l cat        # List the last command beginning with cat
	fc -l 1          # List all the commands

<!-- -->

* 针对 `Bash`, 可以通过 `help` 命令列出所有的 `builtin commands`, 参考[Linux / Unix Bash Shell List All Builtin Commands](http://www.cyberciti.biz/faq/linux-unix-bash-shell-list-all-builtin-commands/). 且 `help -m xxx` 可以查看 xxx 内置命令的文档。
* 针对 `Zsh`, 可以参考手册 [Shell Builtin Commands](http://zsh.sourceforge.net/Doc/Release/Shell-Builtin-Commands.html)

参考:

* [Bash History Builtins](http://www.gnu.org/software/bash/manual/html_node/Bash-History-Builtins.html#Bash-History-Builtins)
* [How To Search Shell Command History](http://www.cyberciti.biz/faq/linux-unix-shell-history-search-command/)
* [Linux and Unix fc and history command](http://www.computerhope.com/unix/uhistory.htm)
* [Retrieve Linux command line history by date](http://superuser.com/questions/397527/retrieve-linux-command-line-history-by-date)
* [Command History - Linux in a Nutshell](http://docstore.mik.ua/orelly/linux/lnut/ch07_06.htm)
