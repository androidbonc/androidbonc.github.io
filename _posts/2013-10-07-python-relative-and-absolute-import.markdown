---
layout: post
title: "Python Relative and Absolute Import"
date: 2013-10-07 16:54
comments: true
categories: Python
---

The [PEP 328: Absolute and Relative Imports](http://docs.python.org/2/whatsnew/2.5.html#pep-328-absolute-and-relative-imports) explans very detailed.

The `absolute_import` feature is default in `Python 3.x`. (I use `Python 2.7.x`)

<!-- more -->

Use the examples pep328 gives:

	pkg
	├── __init__.py
	├── main.py
	└── string.py

The content of string.py

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

def say_hello():
	print "say hello"
```

The content of first version main.py:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string

string.say_hello()
```

	# move to the parent dir of pkg
	$ python -m pkg.main
	say hello

This will use the relative string.py module, not the Python's standard string module.

When use `absolute_import`:

From pep328:

> Once absolute imports are the default, `import string` will always find the standard library’s version.
> It’s **suggested** that users should begin using absolute imports as much as possible, so it’s preferable to begin writing `from pkg import string` in your code.

```python
from __future__ import absolute_import

#import string   # This is error because `import string` will use the standard string module
from pkg import string
string.say_hello()
```

> Relative imports are still possible by adding **a leading period** to the module name when using the `from ... import` form:

```python
from __future__ import absolute_import

from . import string # This is the same as `from pkg import string`
string.say_hello()
```

or

```python
from __future__ import absolute_import

from .string import say_hello
say_hello()
```

Use `print(string)` to see which string module to import

---
2015-02-22 Supplement:


main.py:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import string
print(string)

string.say_hello()
```

If run code by:

	cd pkg
	$ python pkg/main.py
	<module 'string' from '/path/to/my/pkg/string.pyc'>
	say hello

It will always use local string.py, because current path is the first in `sys.path`

change main.py to:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import string
print(string)

string.say_hello()
```

run code:

	cd pkg
	$ python pkg/main.py
	Traceback (most recent call last):
	  File "pkg/main.py", line 3, in <module>
		from . import string
	ValueError: Attempted relative import in non-package

This [answer](http://stackoverflow.com/a/11537218/1276501) is detailed:

> To elaborate on @Ignacio's answer: the python import mechanism works relative to the __name__ of the current file. When you execute a file directly, it doesn't have it's usual name, but has "__main__" as its name instead. So relative imports don't work. You can, as Igancio suggested, execute it using the -m option. If you have a part of your package that is mean to be run as a script, you can also use the __package__ attribute to tell that file what name it's supposed to have in the package hierarchy. See http://www.python.org/dev/peps/pep-0366/ for details.

Absolute/Relative import is to package.

In Python 2.x(by now is Python 2.7.x), the default import feature is `implicit relative import`.

As above see, it will first import the same-named module under package. Use absolute import as default, Python will only import by the `sys.path` sequence.

And if you want to use relative import, you must use `explicit relative import`


That as list in `import this`:

> Explicit is better than implicit

---
2015-08-25 Supplement:

前阵子写了一个功能脚本utils/redis.py, 封装了redis-py(import redis)实现一些功能检查:

    TankyWoo % tree
    .
    ├── main.py
    └── utils
        ├── __init__.py
        └── redis.py

    1 directory, 3 files

    TankyWoo % more main.py
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    from utils import redis

    if __name__ == '__main__':
        redis.func()

    TankyWoo % more utils/redis.py
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    from __future__ import absolute_import
    import redis

    def func():
        print redis.Redis

    if __name__ == '__main__':
        func()

这块在utils/redis.py里必须指定绝对导入, 否则就相当于导入自身了.


Ref:

1. [PEP 0328](https://www.python.org/dev/peps/pep-0328/)
2. [What's wrong with relative imports in Python?](http://programmers.stackexchange.com/questions/159503/whats-wrong-with-relative-imports-in-python)
3. [Attempted relative import in non-package even with __init__.py](http://stackoverflow.com/questions/11536764/attempted-relative-import-in-non-package-even-with-init-py)
4. [Why does PEP 8 advise against explicit relative imports?](http://www.gossamer-threads.com/lists/python/dev/1072694)
5. [Python导入的路径，绝对导入，相对导入](http://zhuhaipeng.me/blog/2014/08/26/pythondao-ru-de-lu-jing-,jue-dui-dao-ru-,xiang-dui-dao-ru/)
6. [Python 类库引入机制](https://github.com/Liuchang0812/slides/tree/master/pycon2015cn)
