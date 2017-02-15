---
layout: post
title: "Python Packaging"
date: 2013-12-04 21:23
comments: true
categories: Python
---

<!-- more -->

## 各种纷乱的关系 ##

* distutils
* setuptools
* distutils2
* easy\_install
* pip

[distutils](http://docs.python.org/2/library/distutils.html) : The distutils package provides support for building and installing additional modules into a Python installation.

[setuptools](https://pypi.python.org/pypi/setuptools) : Easily download, build, install, upgrade, and uninstall Python packages.

[distutils2](https://pypi.python.org/pypi/Distutils2) : Distutils2 is the packaging library that supersedes Distutils.

[easy_install](https://pythonhosted.org/setuptools/easy_install.html) : Easy Install is a python module (easy_install) bundled with setuptools that lets you automatically download, build, install, and manage Python packages.

[pip](https://pypi.python.org/pypi/pip) : A tool for installing and managing Python packages.


总的来说, distutils, setuptools, distutils2 都是用于打包的; pip, easy_install 都是用于包管理(安装/卸载/升级等).

目前, 推荐打包工具是 setuptoosl, 包管理工具是 pip.

另外, 关于打包这块, StackOverflow上有一篇帖子 [Differences between distribute, distutils, setuptools and distutils2?](http://stackoverflow.com/questions/6344076/differences-between-distribute-distutils-setuptools-and-distutils2)

[Python打包的艺术（一）- 综述](http://blog.chinaunix.net/uid-15174104-id-3863249.html) 这篇文章讲的很赞, 把几者之间的关系都理清了.

## 关于打包 ##

其他 Pythoner 都总结过了, 推荐几篇:

* [制作一个 python egg](http://blog.jkey.lu/2013/04/11/create-python-egg/) 用的是 distutils
* [怎样制作一个 Python Egg](http://liluo.org/blog/2012/08/how-to-create-python-egg/)
* [Python egg 学习笔记](http://www.worldhello.net/2010/12/08/2178.html)
* [Python包管理工具setuptools详解](http://yansu.org/2013/06/07/learn-python-setuptools-in-detail.html) 讲的很详细的一篇文章.

## 关于PyPI ##

全称 Python Package Index

> The Python Package Index is a repository of software for the Python programming language.

[PyPI 地址](https://pypi.python.org/pypi)

支持 帐号/密码 和 OpenID 两种方式注册.

注册后, 可以添加自己的ssh公钥, 这样以后提交时就可以通过ssh直接提交.

TODO：
后来了台电脑，提交报错：

> Upload failed (401): You must be identified to edit package information

解决方法，编辑 `$HOME/.pypirc`:

	[server-login]
	username:tankywoo
	password:******

填写用户名和密码

参考 [这篇回复](http://stackoverflow.com/questions/1569315/setup-py-upload-is-failing-with-upload-failed-401-you-must-be-identified-t)

## 其他不错的文章 ##

* [Python 打包指南](http://www.ibm.com/developerworks/cn/opensource/os-pythonpackaging/)
* [A small introduction to Python Eggs](http://mrtopf.de/blog/en/a-small-introduction-to-python-eggs/)

引用 Python打包指南 的最后一段话 : "总的说来，您花费一些时间来学习打包的艺术与科学是值得的。".
