---
layout: post
title: "The Problem of Newline at End of File"
date: 2013-10-19 14:06
comments: true
categories: Python
---

<!-- more -->

Recently I wrote the unit test code the `simiki`. A problem puzzled me.

First, I use python to print the generated output html, and redirect write a expected\_output.html by `>`.

But when I test the result, return False.

So I write the result by python's file.write. And find the reason.

I use `md5sum` to check if they are the same, but not:

	$ tankywoo@linuxmint::tests/ (dev*) » md5sum input.html expected_output.html 
	d977c9d6adb7a14ed5fc5faab8728741  input.html
	9fa7b4e342c9034fa4f8d48cc6cc3a5d  expected_output.html

And diff them:

	$ tankywoo@linuxmint::tests/ (dev*) » diff input.html expected_output.html 
	51c51
	< </html>
	\ No newline at end of file
	---
	> </html>

Note the `No newline at end of file`!!!

Use `hexdump`:

	$ tankywoo@linuxmint::tests/ (dev*) » hexdump -C input.html | tail -n 2
	00000540  73 63 72 69 70 74 3e 0a  3c 2f 68 74 6d 6c 3e     |script>.</html>|
	0000054f
	$ tankywoo@linuxmint::tests/ (dev*) » hexdump -C expected_output.html | tail -n 2
	00000540  73 63 72 69 70 74 3e 0a  3c 2f 68 74 6d 6c 3e 0a  |script>.</html>.|
	00000550

There is a more `0a` symbol in expected\_output.html.

In `man ascii`:

	   Oct   Dec   Hex   Char                 
	   ───────────────────────────────────────
	   012   10    0A    LF  '\n' (new line)  

The `0a` is newline symbol.

The end I thought that the `print` in python will append a newline at the end.

So I use `print(html, end="")` the will be ok.

------

PS: The `cat` command will also find there is no newline after at the end:

	$ tankywoo@linuxmint::tests/ (dev*) » cat input.html| tail -n 2
	</html>%
	$ tankywoo@linuxmint::tests/ (dev*) » cat expected_output.html| tail -n 2
	</html>

Note the percent sign, this indictes that there is no newline symbol at the end of file.

------

Thank this article [Hg/Git diff says “No newline at end of file”](http://blog.yjl.im/2012/11/hggit-diff-says-no-newline-at-end-of.html)
