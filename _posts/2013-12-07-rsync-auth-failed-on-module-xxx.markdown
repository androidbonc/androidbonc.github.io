---
layout: post
title: "rsync auth failed on module xxx"
date: 2013-12-07 12:25
comments: true
categories: Linux
---

<!-- more -->

rsync 报错 "auth failed on module xxx", 一般有三种情况造成:

1. 密码文件格式错误:

服务端密码文件的格式是:

user:password

每个一行

2. 密码文件权限错误

密码文件的权限应该是600

3. rsync 配置错误

主要集中在注释这一块, `man 5 rsyncd.conf` 有两句话:

> The file is line-based -- that is, each newline-terminated line represents either a comment, a module name or a parameter.

> Any line beginning with a hash (#) is ignored, as are lines containing only whitespace.


意思就是配置文件是以行为基准的, 每行要么是注释, 模块或参数.

只有 `以#开始` 的行, 才被认为是注释.


比如配置文件有一句如下:

	secrets file /etc/rsyncd.secret #secret

这是, rsyncd 会认为 "/etc/rsyncd.secret\ #secret" 这个才是密码文件, 所以也会认证失败.
