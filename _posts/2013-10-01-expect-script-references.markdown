---
layout: post
title: "Expect Script References"
date: 2013-10-01 22:21
comments: true
categories: Expect
---

> Expect is a tool for automating interactive applications such as telnet, ftp, passwd, fsck, rlogin, tip, etc. Expect really makes this stuff trivial. Expect is also useful for testing these same applications. And by adding Tk, you can also wrap interactive applications in X11 GUIs.
> Expect can make easy all sorts of tasks that are prohibitively difficult with anything else. You will find that Expect is an absolutely invaluable tool - using it, you will be able to automate tasks that you've never even thought of before - and you'll be able to do this automation ﻿quickly and easily.

From [Expect](http://www.nist.gov/el/msid/expect.cfm)

<!-- more -->

Some Good References:

* [6 Expect Script Examples to Expect the Unexpected (With Hello World)](http://www.thegeekstuff.com/2010/10/expect-examples/)
* [Expect Script Tutorial: Expressions, If Conditions, For Loop, and While Loop Examples](http://www.thegeekstuff.com/2011/01/expect-expressions-loops-conditions/)
* [Using Expect Scripts to Automate Tasks](http://www.admin-magazine.com/Articles/Automating-with-Expect-Scripts)

Another reference is a Simple Introduction, download[pdf]:

* [Expect - A Tool For Automating Interactive Programs](https://www.dropbox.com/s/xablovs3k2n7uft/Expect%20-%20A%20Tool%20For%20Automating%20Interactive%20Programming.pdf)

Exploring Expect is a Expect book, download[pdf]:

* [Exploring Expect](http://ishare.iask.sina.com.cn/f/11167730.html)

The `Man of Expect` is also very good and need to read.

Another references:

* [Expect Home Page](http://expect.sourceforge.net/)
* [Examples of Expect usage](http://wiki.tcl.tk/11583)

Last, a simple example use expect to login by ssh and execute free command to see the memory:

	#!/usr/bin/expect
	spawn ssh root@x.x.x.x
	expect "password: "
	send "PASSWORD\r"

	expect "# "
	send "free -mt\r"

	expect "# "
	send "exit\r"
