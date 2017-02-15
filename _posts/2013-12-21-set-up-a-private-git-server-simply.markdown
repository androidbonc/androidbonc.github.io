---
layout: post
title: "Set Up a Private Git Server - Simply"
date: 2013-12-21 16:10
comments: true
categories: Git
---

<!-- more -->

## 最简单的方法 ##

以下一些文件的基本权限(属主和权限等)不作专门说明.

### 1. 首先系统新建一个用户 ###

名称就叫 git:

	sudo useradd -m git

`-m` 表示同时建立这个用户的home目录. 默认是 `/home/git`, 具体控制base_dir 和 home_dir这些, 可以看 useradd 的 man 手册.

默认新建的用户是没有密码的, 无法登录.

### 2. 新建一个裸仓库 ###

	# 把公钥放到 /home/git/.ssh/authorized_keys
	# 可以通过 ssh 方式先登录git用户
	ssh git@localhost
	# 建一个裸仓库
	git init --bare example.git

### 3. 其他用户或远程克隆 ###

切回原来的用户:

	git clone git@localhost:example.git

因为 example.git 是放在 git 用户的 home目录, 所以都不需要加路径.

远程clone:

	git clone git@x.x.x.x:/home/git/example.git

### 4. 安全性 ###

查看用户的登录权限:

	tankywoo@gentoo-jl::~/ » sudo grep 'git' /etc/passwd /etc/shadow
	/etc/passwd:git:x:1001:1001::/home/git:/bin/bash
	/etc/shadow:git:!:16060:0:99999:7:::

可以看到上面提到的不能用密码登录, `/etc/shadow` 的第三个字段是 `!` , 可以 `man 5 shadow` :

> If the password field contains some string that is not a valid result of crypt(3), for instance `!` or `*`, the user will not be able to use a unix password to log in (but the user may log in the system by other means).

但是上面就用到了ssh方式登录, git 提供了 `git-shell` 的 login-shell 来做一些安全性的限制:

	# 查看 git-shell 路径
	$ which git-shell
	/usr/bin/git-shell
	# 修改 git 用户的 login shell
	sudo usermod -s /usr/bin/git-shell git

再次确认:

	tankywoo@gentoo-jl::~/ » grep 'git' /etc/passwd
	git:x:1001:1001::/home/git:/usr/bin/git-shell

通过 ssh 登录会发现无法登录了:

	tankywoo@gentoo-jl::~/ » ssh git@localhost
	Last login: Sat Dec 21 17:43:21 CST 2013 from localhost on pts/19
	fatal: Interactive git shell is not enabled.
	hint: ~/git-shell-commands should exist and have read and execute access.
	Connection to localhost closed.

更多可以看 git-shell 的文档: [git-shell Manual Page](http://git-scm.com/docs/git-shell.html)

> git-shell - Restricted login shell for Git-only SSH access

这种简单的方式, 公钥就可以完全交给 `~/.ssh/authorized_keys` 来管理.
