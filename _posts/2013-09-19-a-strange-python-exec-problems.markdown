---
layout: post
title: "A strange python-exec problems"
date: 2013-09-19 15:57
comments: true
categories: Gentoo
---

<!-- more -->

Many python tools in `/usr/bin` is a softlink to `/usr/bin/python-exec`:

	$ ll /usr/bin | grep python-exec
	lrwxrwxrwx   1 root root          11 Apr 24 22:24 django-admin.py -> python-exec
	lrwxrwxrwx   1 root root          11 Apr  4 15:44 easy_install -> python-exec
	lrwxrwxrwx   1 root root          11 Sep 18 23:51 layman -> python-exec
	lrwxrwxrwx   1 root root          11 Sep 18 23:51 layman-updater -> python-exec
	lrwxrwxrwx   1 root root          11 Jun 18 08:00 markdown2 -> python-exec
	lrwxrwxrwx   1 root root          11 Sep 19 11:51 pip -> python-exec
	lrwxrwxrwx   1 root root          11 Apr 24 22:09 pygmentize -> python-exec
	-rwxr-xr-x   1 root root        1397 Sep 19 11:50 python-exec
	-rwxr-xr-x   1 root root       10320 Sep 19 11:50 python-exec-c
	...

I use `pip` and `layman`, and find they are strange.

The content of `/usr/bin/python-exec`:

```python
#!/usr/bin/python2.7
# EASY-INSTALL-ENTRY-SCRIPT: 'Pygments==1.6','console_scripts','pygmentize'
__requires__ = 'Pygments==1.6'
import sys
from pkg_resources import load_entry_point

sys.exit(
	load_entry_point('Pygments==1.6', 'console_scripts', 'pygmentize')()
)
```


First I check this script:

	% equery belongs python-exec
	 * Searching for python-exec ... 
	dev-python/python-exec-0.3.1 (/usr/bin/python-exec)

Find it belongs to `dev-python/python-exec-0.3.1`.

And the package info:

	*  dev-python/python-exec
		  Latest version available: 0.3.1
		  Latest version installed: 0.3.1
		  Size of files: 72 kB
		  Homepage:      https://bitbucket.org/mgorny/python-exec/
		  Description:   Python script wrapper
		  License:       BSD

Then I read the help information of this script, the function of this script is to **pymentize** the codesnippet.

	$ python-exec -l python -f html -o /tmp/test.file
	#this is the input#
	print 'hello world'
	....

`Ctrl-d` to eof input.

It will write the input to /tmp/test.file, and use pygments to colorful the code.

I check the python-exec package code source, be sure this is not the right content.

The right content:

```python
#!/usr/bin/python-exec-c
# vim:fileencoding=utf-8:ft=python
# (c) 2012 Michał Górny
# Released under the terms of the 2-clause BSD license.
#
# This is not the script you are looking for. This is just a wrapper.
# The actual scripts of this application were installed with -python*,
# -pypy* or -jython* suffixes. You are most likely looking for one
# of those.

from __future__ import with_statement
import os, os.path, sys

try:
	from epython import EPYTHON
except ImportError:
	EPYTHON = os.path.basename(sys.executable)
	if '' and EPYTHON.endswith(''):
		EPYTHON = EPYTHON[:-len('')]

# In the loop:
# sys.argv[0] keeps the 'bare' name
# __file__ keeps the 'full' name

while True:
	__file__ = sys.argv[0] + '-' + EPYTHON

	try:
		kwargs = {}
		if sys.version_info[0] >= 3:
			import tokenize

			# need to provide encoding
			with open(__file__, 'rb') as f:
				kwargs['encoding'] = tokenize.detect_encoding(f.readline)[0]

		with open(__file__, 'r', **kwargs) as f:
			data = f.read()
	except IOError:
		# follow symlinks (if supported)
		try:
			sys.argv[0] = os.path.join(os.path.dirname(sys.argv[0]),
					os.readlink(sys.argv[0]))
		except (OSError, AttributeError):
			# no more symlinks? then it's time to fail.
			sys.stderr.write('This Python implementation (%s) is not supported by the script.\n'
					% EPYTHON)
			sys.exit(127)
	else:
		break

sys.argv[0] = __file__
exec(data)
```

It is a simple wrapper to wrap python tools under `/usr/bin`.

For some reason(I have not found), another software(maybe pygments) overwrite the `/usr/bin/python-exec`.

Reinstall `python-exec` and solve this strange problem:

	emerge -avD python-exec

Disable python-exec to be changed by other package:

	emerge --oneshort python-exec:2
