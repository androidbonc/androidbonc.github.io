---
layout: post
title: "Python Universal Newlines"
date: 2015-01-11 16:10
---

关于Python的`Universal Newlines`, 在[Glossary](https://docs.python.org/2/glossary.html)解释:

> A manner of interpreting text streams in which all of the following are recognized as ending a line: the Unix end-of-line convention '\n', the Windows convention '\r\n', and the old Macintosh convention '\r'. See PEP 278 and PEP 3116, as well as str.splitlines() for an additional use.

通用换行, 是对跨平台的换行符做一个归一化的处理. 将Unix, Mac, Dos三个平台的换行符统一为Unix的换行符`\n`

内置的[`open`](https://docs.python.org/2/library/functions.html#open)函数通过`U`支持这个方式:

> In addition to the standard fopen() values mode may be `'U'` or `'rU'`. Python is usually built with universal newlines support; supplying `'U'` opens the file as a text file, but lines may be terminated by any of the following: the Unix end-of-line convention `'\n'`, the Macintosh convention `'\r'`, or the Windows convention `'\r\n'`. All of these external representations are seen as `'\n'` by the Python program. If Python is built without universal newlines support a mode with `'U'` is the same as normal text mode. Note that file objects so opened also have an attribute called newlines which has a value of None (if no newlines have yet been seen), `'\n'`, `'\r'`, `'\r\n'`, or a tuple containing all the newline types seen.

> Python enforces that the mode, after stripping `'U'`, begins with `'r'`, `'w'` or `'a'`.

---

新建三个文件, 内容都是:

	one say 'Hello World'
	two say 'Hello World'

文本格式分别是 Unix, Mac, Dos:

	$ file text_*.txt
	text_mac.txt:  ASCII text, with CR line terminators
	text_unix.txt: ASCII text
	text_win.txt:  ASCII text, with CRLF line terminators

测试脚本:

{% highlight python %}
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tanky Woo @ 2015-01-11
from pprint import pprint

def open_without_U(fn):
	print('  open file without U mode:')
	with open(fn, 'r') as fd:
		pprint(fd.readlines())

def open_with_U(fn):
	print('  open file with U mode:')
	with open(fn, 'rU') as fd:
		pprint(fd.readlines())


if __name__ == '__main__':
	for fn in ('text_unix.txt', 'text_mac.txt', 'text_win.txt'):
		print('>>> {}:'.format(fn))
		open_without_U(fn)
		open_with_U(fn)
		print('')
{% endhighlight %}

测试结果:

	>>> text_unix.txt:
	  open file without U mode:
	["one say 'Hello World'\n", "two say 'Hello World'\n"]
	  open file with U mode:
	["one say 'Hello World'\n", "two say 'Hello World'\n"]

	>>> text_mac.txt:
	  open file without U mode:
	["one say 'Hello World'\rtwo say 'Hello World'\r"]
	  open file with U mode:
	["one say 'Hello World'\n", "two say 'Hello World'\n"]

	>>> text_win.txt:
	  open file without U mode:
	["one say 'Hello World'\r\n", "two say 'Hello World'\r\n"]
	  open file with U mode:
	["one say 'Hello World'\n", "two say 'Hello World'\n"]

Python 的 `readlines()` 会对 `\n` 以及 `\r\n` 做处理，但是不会对 `\r` 做处理，和平台性无关(其实感觉这里应该根据平台相应的换行符来处理的)。这个是直接查看Python的源码`fileobject.c`的`get_line`函数看到的.

所以如结果显示.

这里也可以通过`str.splitlines([keepends])`来处理.

{% highlight python %}
def open_without_U(fn):
	print('  open file without U mode:')
	with open(fn, 'r') as fd:
		content = fd.read()
		pprint(content.splitlines())
{% endhighlight %}

测试结果:

	>>> text_unix.txt:
	  open file without U mode:
	["one say 'Hello World'", "two say 'Hello World'"]
	  open file with U mode:
	["one say 'Hello World'\n", "two say 'Hello World'\n"]

	>>> text_mac.txt:
	  open file without U mode:
	["one say 'Hello World'", "two say 'Hello World'"]
	  open file with U mode:
	["one say 'Hello World'\n", "two say 'Hello World'\n"]

	>>> text_win.txt:
	  open file without U mode:
	["one say 'Hello World'", "two say 'Hello World'"]
	  open file with U mode:
	["one say 'Hello World'\n", "two say 'Hello World'\n"]

`splitlines`可以设置参数为`True`来保持原来的换行符.

另外 `os.linesep` 也可以输出当前平台下的换行符.

`file.newlines`, 必须使用`U`模式打开文件, 在经过`read()`或`readlines()`(`readline()`不行)后, 会记录文件的原始newline.

2015-01-12补充:

`io.open`的功能更强大, 之前在simiki对universal newlines的处理中已经用到了. 它可以控制打开文件时的编码, 并且也有newline参数控制, 默认为None, read时会自动统一为universal newlines.也可以关闭掉. write时也可以选择是否更具相应平台改为相应的实际newline符.

---

对于跨平台的开发，尽量不用硬编码，而使用Python提供的相应接口。
