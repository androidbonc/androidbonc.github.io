---
layout: post
title: "简单使用Svn Hook"
date: 2014-05-28 22:50
categories: Svn
---

<!-- more -->

首先在本地建了一个svn库:

	# 创建svn库
	$ svnadmin create testsvn
	# 进入svn库的配置目录，进行简单配置
	# authz : 设置用户组和用户组对各目录(子目录)的权限
	# passwd : 设置用户及相应密码
	# svnserve.conf : svn服务的配置
	$ cdn testsvn/conf
	$ ls
	authz  passwd  svnserve.conf

进行了一些简单的配置，然后启动服务。

Gentoo 下配置启动脚本的配置在 `/etc/conf.d/svnserve`，修改`SVNSERVE_OPTS="--root=/var/svn"` 为相应地址。

也可以直接使用命令启动:

	svnserve -d -r /path/to/svnrepo/

然后就可以checkout了:

	svn co svn://localhost/testsvn/

接下来就是尝试Svn hook。

cd到 `testsvn/hooks` 目录，Svn已经提供了9个hook模板(第一个是我自己写的):

	$ ls
	post-commit       post-lock.tmpl            post-unlock.tmpl  pre-lock.tmpl            pre-unlock.tmpl
	post-commit.tmpl  post-revprop-change.tmpl  pre-commit.tmpl   pre-revprop-change.tmpl  start-commit.tmpl

每一个都对应了一个事件。

如果要使用，需要cp一份，去掉后缀，保持和事件名一样。 hook可以用Shell，Python或其它语言写。

另外hook需要加可执行权限，否则svn commit时会报错:

	Warning: post-commit hook failed (exit code 255) with no output.

如:

	cp post-commit.tmpl post-commit
	chmod +x post-commit

根据需求暂时使用了 post-commit hook。

模板里面说明很详细，post-commit是在commit后触发的操作，执行时svn传入两个环境变量 `REPOS-PATH`仓库的路径 和 `REV` 提交的版本号。

比如这里我想获取提交者和提交log:

	REPOS="$1"
	REV="$2"

	AUTHOR=$(svnlook author -r $REV $REPOS)
	MESSAGE=$(svnlook log $REPOS -r $REV)
	#MESSAGE=$(svnlook propget --revprop -r $REV $REPOS svn:log)

获取到这些信息后我就可以做进一步的操作了，比如把这些信息以邮件方式发给管理者等。

这里用到了svn自带的一个工具`svnlook`，配合一些子命令可以获取很多信息。

还有一些其它的钩子，常用的应该就`pre-commit`和`post-commit`这两个。
