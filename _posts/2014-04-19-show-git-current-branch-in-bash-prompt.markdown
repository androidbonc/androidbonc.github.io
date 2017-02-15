---
layout: post
title: "Show Git Current Branch in Bash Prompt"
date: 2014-04-19 11:32
comments: true
categories: Git
---

<!-- more -->

环境: Ubuntu 12.04

安装 `bash-completion`，Ubuntu 12.04 默认已经安装好了。

相关脚本在 `/etc/bash_completion`, 在 `~/.bashrc` 中source这个脚本。

Ubuntu 12.04的`~/.bashrc` 最下面已经有这段source脚本，默认是注释掉的，去掉注释即可:

	# enable programmable completion features (you don't need to enable
	# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
	# sources /etc/bash.bashrc).
	#if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
	#	. /etc/bash_completion
	#fi

然后配置`PS1`:

	PS1='\[\033[01;32m\]\u@\h\[\033[01;34m\] \w\[\033[01;33m\]$(__git_ps1)\[\033[01;34m\] \$\[\033[00m\] '

此时会显示当前分支名。

如果当前分支下有改动，也可以增加提示，开启环境变量:

	GIT_PS1_SHOWDIRTYSTATE=1

测试:

	root@ubuntu ~/test-git (master) # vi af
	root@ubuntu ~/test-git (master *) # git add af
	root@ubuntu ~/test-git (master +) # git ci -m 'update'

参考 [Show current Git branch and status in your prompt](http://www.bramschoenmakers.nl/en/node/624)

其实 bash-completion 是许多工具completion的一个集合，如果不想一次把这个大项目source进去，可以按需求只source相关的completion脚本:

比如git的completion脚本是 `/etc/bash_completion.d/git`。

另外在[github上](https://github.com/git/git/tree/master/contrib/completion)，git组织也维护了这个相关的脚本。

如果只需要prompt提示的功能，则可以直接下载这个项目里的`git-prompt.sh`，然后source，配置和上面一样。具体可以看看[这篇](http://code-worrier.com/blog/git-branch-in-bash-prompt/)
