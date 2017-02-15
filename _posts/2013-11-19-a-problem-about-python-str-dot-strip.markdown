---
layout: post
title: "A Problem About Python str.strip"
date: 2013-11-19 23:19
comments: true
categories: Python
---

<!-- more -->

一直误以为 Python 的 `str.strip` 是用于删除指定的 <strike>前缀/后缀</strike> .

直到今天写一个脚本时遇到了问题, 举个例子:

```
	In [1]: a = "abc-amn"

	In [2]: b = "abc-"

	In [3]: a.lstrip(b)
		Out[3]: 'mn'
```

本来是准备从 a 中删除前缀 b, 预想中的结果应该是 amn, 实际是 mn.

[文档](http://docs.python.org/2/library/stdtypes.html#str.strip)上其实说明和举例都很清楚了...

> The chars argument is not a prefix or suffix; rather, all combinations of its values are stripped

```
	>>> 'www.example.com'.strip('cmowz.')
	'example'
```

