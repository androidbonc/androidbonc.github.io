---
layout: post
title: "Detect OS for Shell"
date: 2014-06-09 13:38
categories: Linux
---

<!-- more -->

[.dotfiles](https://github.com/tankywoo/dotfiles) 里的 .zsh/aliases.zsh 要设置一些别名，对于 `ls` 命令的，要设置默认为颜色输出。

Linux下是:

	alias ls='ls --color=auto'

Mac下是:

	alias ls='ls -hG'

这时就要检测系统并做相应设置。

首先`uname`就可以满足，如果不指定参数，默认参数就是`-s`, 即Kernel Name。平时用的较多的参数是`-a` 和 `-r`。

比如这里只对Linux和Mac做处理，其余的使用原生的就行。

	if [[ "$(uname)" == "Darwin" ]]; then
		# For Mac OS
		alias ls='ls -hG'
	elif [[ "$(uname)" == "Linux" ]];then
		# For Linux
		alias ls='ls --color=auto'
	else
			:
	fi

另外，还有提到`OSTYPE`环境变量

Linux下:

	tankywoo@gentoo-local::~/ » echo $OSTYPE
	linux-gnu

Mac下:

	TankyWoo@Mac::~/ » echo $OSTYPE
	darwin13.0

可以改为:

	if [[ "$OSTYPE" == "linux-gnu"  ]]; then
		alias ls='ls --color=auto'
	elif [[ "$OSTYPE" == "darwin"*  ]]; then
		alias ls='ls -hG'
	else
		:
	fi

更多可以看看:

* [Detect the OS from a Bash script](http://stackoverflow.com/questions/394230/detect-the-os-from-a-bash-script)
* [How to check if running in Cygwin, Mac or Linux?](http://stackoverflow.com/questions/3466166/how-to-check-if-running-in-cygwin-mac-or-linux)
