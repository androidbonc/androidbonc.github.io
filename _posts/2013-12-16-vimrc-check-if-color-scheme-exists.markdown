---
layout: post
title: "vimrc check if color scheme exists"
date: 2013-12-16 01:28
comments: true
categories: Vim
---

首先 vim 提供 `try ... catch ...` 可以捕获错误.

另外 `:silent! colorscheme foo` 如果color scheme 不存在, 也不会报错.

比如:

	try
		colorscheme Tomorrow-Night-Bright
	catch /^Vim\%((\a\+)\)\=:E185/
		colorscheme desert
	endtry

参考:

* [In my .vimrc, how can I check for the existence of a color scheme?](http://stackoverflow.com/questions/5698284/in-my-vimrc-how-can-i-check-for-the-existence-of-a-color-scheme)
* [Gracefully degrading .vimrc](http://blog.sanctum.geek.nz/gracefully-degrading-vimrc/)
