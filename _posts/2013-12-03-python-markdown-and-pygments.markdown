---
layout: post
title: "Python-Markdown and Pygments"
date: 2013-12-03 22:06
comments: true
categories: Python
---

<!-- more -->

今天在写 [simiki](https://github.com/tankywoo/simiki) 时, 发现代码高亮不起作用了.

之前以为 [Python-Markdown](https://github.com/waylan/Python-Markdown) 只要使用 codehilite 的扩展属性就可以了.

后来看代码:

```python
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
    from pygments.formatters import HtmlFormatter
    pygments = True
except ImportError:
    pygments = False

```

依然会调用 [Pygments](http://pygments.org/).

而我使用了virtualenv, 开发环境还没有装 Pygments.
