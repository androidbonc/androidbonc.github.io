---
layout: post
title: "Python Encoding"
date: 2015-01-21 07:30
---

## Python Source File Encoding ##

```python
#!/usr/bin/env python

u = unicode('中国', 'utf-8')
```

Without specify source file encoding on the top of source file:

	$ python without-magic-comment.py
	  File "without-magic-comment.py", line 3
	  SyntaxError: Non-ASCII character '\xe2' in file without-magic-comment.py on line 5, but no encoding declared;
	  see http://www.python.org/peps/pep-0263.html for details

Because there are `non-ascii` characters in the source file, Python parser can't interpret the source code.

The error message metioned [PEP-0263](https://www.python.org/dev/peps/pep-0263/):

> This PEP proposes to introduce a syntax to declare the encoding of a Python source file. The encoding information     is then used by the Python parser to interpret the file using the given encoding.

<!-- -->

> Python will default to ASCII as standard encoding if no other encoding hints are given.

Place magic comment into the source at the top:

```python
# coding=<encoding name>
```

or:

```python
# -*- coding: <encoding name> -*-
```

or:

```python
# vim: set fileencoding=<encoding name>
```

I usual use:

```python
# -*- coding: utf-8 -*-
```

Example:

First use `iconv` to convert the source file encoding to gb2312:

	iconv -f utf-8 -t gb2312 magic_comment.py > magic_comment_gb2312.py

The source code:

```python
#!/usr/bin/env python
# -*- coding: gb2312 -*-

import chardet
from pprint import pprint
s = '中国'

pprint(s)
print chardet.detect(s)

pprint(s.decode('gb2312'))
```

Output:

	$ python magic_comment_gb2312.py
	'\xd6\xd0\xb9\xfa'
	{'confidence': 0.7679697235616183, 'encoding': 'IBM855'}
	u'\u4e2d\u56fd'

---

## `unicode_literals` in `__future__` ##

[`unicode_literals`](https://docs.python.org/2/library/__future__.html) add in Python 2.6, I usual add this for uniform encoding environment and compatibility

The default string type is `str` in Python 2.x, after `from __future__ import unicode_literals`, the string type is unicode.

First, the normal mode without `unicode_literals`:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from pprint import pprint

s = ['abc', u'abc', '中国', u'中国']

for i in s:
        print(i, end=': ')
        pprint(type(i))
        print('')

print('------- decode:')
for i in s:
        try:
                print(i, end=': ')
                pprint(type(i.decode('utf-8')))
        except Exception as e:
                print(">>> error: " + str(e))
        finally:
                print('')

print('------- encode:')
for i in s:
        try:
                print(i, end=': ')
                pprint(type(i.encode('utf-8')))
        except Exception as e:
                print(">>> error: " + str(e))
        finally:
                print('')
```

Output:

	abc: <type 'str'>

	abc: <type 'unicode'>

	中国: <type 'str'>

	中国: <type 'unicode'>

	------- decode:
	abc: <type 'unicode'>

	abc: <type 'unicode'>

	中国: <type 'unicode'>

	中国: >>> error: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)

	------- encode:
	abc: <type 'str'>

	abc: <type 'str'>

	中国: >>> error: 'ascii' codec can't decode byte 0xe4 in position 0: ordinal not in range(128)

	中国: <type 'str'>

If add `unicode_literals`:

	abc: <type 'unicode'>

	abc: <type 'unicode'>

	中国: <type 'unicode'>

	中国: <type 'unicode'>

	------- decode:
	abc: <type 'unicode'>

	abc: <type 'unicode'>

	中国: >>> error: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)

	中国: >>> error: 'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)

	------- encode:
	abc: <type 'str'>

	abc: <type 'str'>

	中国: <type 'str'>

	中国: <type 'str'>


Use `unicode_literals`, all the string variable is unicode.

Other discuss:

* [Any gotchas using unicode_literals in Python 2.6?](http://stackoverflow.com/questions/809796/any-gotchas-using-u    nicode-literals-in-python-2-6)
* [Should I import unicode_literals?](http://python-future.org/unicode_literals.html)

---


## System Default Encoding ##

Two releated function


	sys.getdefaultencoding()
	sys.setdefaultencoding()

`getdefaultencoding()` get default string encoding, under Python 2.x, it's usual `ascii`; 

`setdefaultencoding()` change default string encoding. but you need `reload(sys)` first, the reason [Changing default encoding of Python?](http://stackoverflow.com/questions/2276200/changing-default-encoding-of-python)


First, look back the above code:

1. in normal mode, `u'中国'` can't be decoded, but `u'abc'` can.
2. `u'中国'` do decode, but error message is `'ascii' codec can't encode characters`, and raise `UnicodeEncodeError`

(Note this is just a example, **do not** decode a unicode!!!)

The reason is that:

> Python is helpful!!!

When do decode, Python check and find the variable is unicode, so it will do `encode(sys.getdefaultencoding())` first, and then decode this generated str. But when do encode, there is error.

Other discuss:

* [unicode().decode('utf-8', 'ignore') raising UnicodeEncodeError](http://stackoverflow.com/questions/5096776/unico    de-decodeutf-8-ignore-raising-unicodeencodeerror)


Another example based on above code:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from pprint import pprint

print(sys.getdefaultencoding())
reload(sys)
sys.setdefaultencoding('utf-8')
print(sys.getdefaultencoding())
print('\n-------\n')

s = ['abc', u'abc', '中国', u'中国']

for i in s:
    print(i, end=': ')
    pprint(type(i))
    print('')

print('------- decode:')

for i in s:
    try:
        print(i, end=': ')
        pprint(type(i.decode('utf-8')))
    except Exception as e:
        print(">>> error: " + str(e))
    finally:
        print('')

print('------- encode:')


for i in s:
    try:
        print(i, end=': ')
        pprint(type(i.encode('utf-8')))
    except Exception as e:
        print(">>> error: " + str(e))
    finally:
        print('')
```

Output:

	$ python defaultencoding.py
	ascii
	utf-8

	-------

	abc: <type 'str'>

	abc: <type 'unicode'>

	中国: <type 'str'>

	中国: <type 'unicode'>

	------- decode:
	abc: <type 'unicode'>


	abc: <type 'unicode'>

	中国: <type 'unicode'>

	中国: <type 'unicode'>

	------- encode:
	abc: <type 'str'>

	abc: <type 'str'>

	中国: <type 'str'>

	中国: <type 'str'>

As see output, the default string encoding is ascii, if change to `utf-8`, there is no error.

---

Supplement(2015-02-16):

	In [11]: s = u'hello world'

	In [12]: s
	Out[12]: u'hello world'

	In [13]: s.decode()
	Out[13]: u'hello world'

	In [14]: s.decode('utf-8')
	Out[14]: u'hello world'

	In [15]: unicode(s)
	Out[15]: u'hello world'

	In [16]: unicode(s, 'utf-8')
	---------------------------------------------------------------------------
	TypeError                                 Traceback (most recent call last)
	<ipython-input-16-20705e8c9e2c> in <module>()
	----> 1 unicode(s, 'utf-8')

	TypeError: decoding Unicode is not supported

The last example has error, why?

See the [doc](https://docs.python.org/2/library/functions.html#unicode):

	unicode(object='')
	unicode(object[, encoding[, errors]])

> If encoding and/or errors are given, unicode() will decode the object which can either be an 8-bit string or a character buffer using the codec for encoding.

> If no optional parameters are given, unicode() will mimic the behaviour of str() except that it returns Unicode strings instead of 8-bit strings. More precisely, if object is a Unicode string or subclass it will return that Unicode string without any additional decoding applied.

This is a little different with `decode`, which will always do nothing if the object is unicode.

So, what is the differenct between `str.decode()` and `unicode()`?

They are essentially the same, but there are some little difference, above is one of it, others:

1. `unicode` is faster than `str.decode()`, [ref](http://stackoverflow.com/a/440432/1276501)
2. `unicode` is no longer exists in Python3.x, because the string type is unicode by default. [ref](http://stackoverflow.com/a/440461/1276501)
3. The `unicode` constructor can take other types apart from strings, such as `unicode(10)`. [ref](http://stackoverflow.com/a/11861660/1276501)
4. Some encoding options are not valid for the `unicode`, but valid for the `str.decode()`. [ref](http://stackoverflow.com/a/11861660/1276501)


---

## Other References ##

* [Python Howto - unicode](https://docs.python.org/2/howto/unicode.html)
* [Pragmatic Unicode](http://nedbatchelder.com/text/unipain/unipain.html) Excellent doc, multiple pages
* [Pragmatic Unicode](http://nedbatchelder.com/text/unipain.html) single page
* [Python Wiki - Default Encoding](https://wiki.python.org/moin/DefaultEncoding)
* [Correctly using unicode in python2](https://fedorahosted.org/releases/k/i/kitchen/docs/unicode-frustrations.html)
* [Unicode in Python, and how to prevent it](http://washort.twistedmatrix.com/2010/11/unicode-in-python-and-how-to-prevent-it.html)
* [The problem I asked in Stackoverflow](http://stackoverflow.com/questions/28062518/python-decode-in-unicode-variable-with-non-ascii-character-or-without/)
* [字符编码笔记：ASCII，Unicode和UTF-8](http://www.ruanyifeng.com/blog/2007/10/ascii_unicode_and_utf-8.html)
* [怎么在Python里使用UTF-8编码](http://liguangming.com/how-to-use-utf-8-with-python)
* [Python字符编码详解](http://www.cnblogs.com/huxi/articles/1897271.html)
* [Python中的字符串编码（Encode）与解码（Decode）](http://zhangxc.com/2014/10/python-encode-decode)
* [PYTHON-进阶-编码处理小结](http://wklken.me/posts/2013/08/31/python-extra-coding-intro.html)
* [what's the difference between unicode(self) and self.__unicode__() in a Python Class?](http://stackoverflow.com/questions/11117156/whats-the-difference-between-unicodeself-and-self-unicode-in-a-python-c)

