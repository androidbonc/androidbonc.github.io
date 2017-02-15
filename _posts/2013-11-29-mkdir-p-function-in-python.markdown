---
layout: post
title: "mkdir -p function in python"
date: 2013-11-29 15:09
comments: true
categories: Python
---

[mkdir -p functionality in python](http://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python)

`mkdir -p` functionality as follows:

```python
	import os, errno

	def mkdir_p(path):
		try:
			os.makedirs(path)
		except OSError as exc: # Python >2.5
			if exc.errno == errno.EEXIST and os.path.isdir(path):
				pass
			else: raise
```

Update

> For Python ≥ 3.2, os.makedirs has an optional third argument exist_ok that, when true, enables the mkdir -p functionality —unless mode is provided and the existing directory has different permissions than the intended ones; in that case, OSError is raised as previously.
