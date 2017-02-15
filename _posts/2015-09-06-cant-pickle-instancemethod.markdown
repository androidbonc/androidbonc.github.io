---
layout: post
title: "Python Can't pickle type 'instancemethod' 问题"
date: 2015-09-06 21:00
---

最近给[Simiki](http://simiki.org/)从单进程改为多进程时, 遇到这个报错.

给一个正常的简化的版本:

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	import multiprocessing

	def func(x):
		print(x * x)

	class Klass(object):
		def __init__(self):
			print "Constructor ... %s" % multiprocessing.current_process().name

		def __del__(self):
			print "... Destructor %s" % multiprocessing.current_process().name

		def func(self, x):
			print(x * x)

		def run(self):
			pool = multiprocessing.Pool(processes=3)
			for num in range(8):
				pool.apply_async(func, args=(num,))
			pool.close()
			pool.join()

	if __name__ == '__main__':
		_kls = Klass()
		_kls.run()

这里加上构造函数和析构函数, 是因为后面在这里会有问题.

另外, 这里有个比较奇怪的现象, 原先实例类时, 变量名是kls, 但是析构出错, 改为als没有问题, 试了很多变量名, 有的有问题, 有的没问题, <strike>还不清楚原因</strike>

	Constructor ... MainProcess
	Exception AttributeError: "'NoneType' object has no attribute 'current_process'" in <bound method Klass.__del__ of <__main__.Klass object at 0x103a1ce10>> ignored

原因已经找到, 参考[`__del__`](https://docs.python.org/2/reference/datamodel.html#object.__del__)文档:

> Starting with version 1.5, Python guarantees that globals whose name begins with a single underscore are deleted from their module before other globals are deleted; if no other references to such globals exist, this may help in assuring that imported modules are still available at the time when the `__del__()` method is called.

对于普通变量, Python无法保证`__del__`和对象销毁的顺序, 如果变量名以下划线开头, 可以保证此变量在其它导入模块之前调用.

具体可以看看我在StackOverflow上的[提问](http://stackoverflow.com/questions/32443135/python-strange-multiprocessing-with-variable-name)

正常执行结果:

	Constructor ... MainProcess
	0
	1
	4
	9
	16
	25
	36
	49
	... Destructor MainProcess

如果把func移到类中, 改为method, 则问题来了:

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	import multiprocessing

	class Klass(object):
		def __init__(self):
			print "Constructor ... %s" % multiprocessing.current_process().name

		def __del__(self):
			print "... Destructor %s" % multiprocessing.current_process().name

		def func(self, x):
			print(x * x)

		def run(self):
			pool = multiprocessing.Pool(processes=3)
			for num in range(8):
				pool.apply_async(self.func, args=(num,))
			pool.close()
			pool.join()

	if __name__ == '__main__':
		_kls = Klass()
		_kls.run()


执行报错:

	Constructor ... MainProcess
	Exception in thread Thread-2:
	Traceback (most recent call last):
	  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/threading.py", line 808, in __bootstrap_inner
		self.run()
	  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/threading.py", line 761, in run
		self.__target(*self.__args, **self.__kwargs)
	  File "/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/multiprocessing/pool.py", line 342, in _handle_tasks
		put(task)
	PicklingError: Can't pickle <type 'instancemethod'>: attribute lookup __builtin__.instancemethod failed

搜到这个问题[Can't pickle <type 'instancemethod'> when using python's multiprocessing Pool.map()](http://stackoverflow.com/questions/1816958/cant-pickle-type-instancemethod-when-using-pythons-multiprocessing-pool-ma)

原因是multiprocessing会对调用的函数做序列化, 然后method不可被序列化. 具体参考[python2 - pickle](https://docs.python.org/2/library/pickle.html#what-can-be-pickled-and-unpickled)的文档, 里面列出了可被序列化的对象:

* None, True, and False
* integers, long integers, floating point numbers, complex numbers
* normal and Unicode strings
* tuples, lists, sets, and dictionaries containing only picklable objects
* functions defined at the top level of a module
* built-in functions defined at the top level of a module
* classes that are defined at the top level of a module
* instances of such classes whose `__dict__` or the result of calling `__getstate__()` is picklable (see section The pickle protocol for details).

---

关于解决思路, 众说纷坛, 有利有弊.

最简单的思路? 感谢这个兄弟的[思路](https://virusdefender.net/index.php/archives/318/), 加一个全局的代理函数, 他也注意到了后面的几个方法会出现析构多次, 但是这个其实也会这样:

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	import multiprocessing

	def proxy(cls_instance, i):
		return cls_instance.func(i)

	class Klass(object):
		def __init__(self):
			print "Constructor ... %s" % multiprocessing.current_process().name

		def __del__(self):
			print "... Destructor %s" % multiprocessing.current_process().name

		def func(self, x):
			print(x * x)

		def run(self):
			pool = multiprocessing.Pool(processes=3)
			for num in range(8):
				#pool.apply_async(self.func, args=(num,))
				pool.apply_async(proxy, args=(self, num,))
			pool.close()
			pool.join()

	if __name__ == '__main__':
		_kls = Klass()
		_kls.run()

执行代码:

	Constructor ... MainProcess
	0
	1
	4
	... Destructor PoolWorker-1
	9
	... Destructor PoolWorker-2
	16
	... Destructor PoolWorker-1
	36
	... Destructor PoolWorker-3
	25
	... Destructor PoolWorker-2
	49
	... Destructor PoolWorker-1
	... Destructor PoolWorker-3
	... Destructor PoolWorker-2
	... Destructor MainProcess

注意到这里线程池中的worker析构了8次, 每个worker进程析构了2-3次, 主进程析构了1次.

还有一个介绍的比较多的就是用[`copy_reg`](https://docs.python.org/2/library/copy_reg.html)将MethodType注册为可序列化来解决:

参考这个[回答](http://stackoverflow.com/a/25161919/1276501)的模板:

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	import copy_reg
	import types

	def _pickle_method(m):
		if m.im_self is None:
			return getattr, (m.im_class, m.im_func.func_name)
		else:
			return getattr, (m.im_self, m.im_func.func_name)

	copy_reg.pickle(types.MethodType, _pickle_method)

或者这个[回答](http://stackoverflow.com/a/7309686/1276501)的模板:

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	from copy_reg import pickle
	from types import MethodType

	def _pickle_method(method):
		func_name = method.im_func.__name__
		obj = method.im_self
		cls = method.im_class
		return _unpickle_method, (func_name, obj, cls)

	def _unpickle_method(func_name, obj, cls):
		for cls in cls.mro():
			try:
				func = cls.__dict__[func_name]
			except KeyError:
				pass
			else:
				break
		return func.__get__(obj, cls)

	pickle(MethodType, _pickle_method, _unpickle_method)

这里用到了[`mro()`](https://docs.python.org/2/library/stdtypes.html#class.mro)

* `im_self` is the class instance object;
* `im_func` is the function object;
* `im_class` is the class of `im_self` for bound methods or the class that asked for the method for unbound methods;

具体见[文档](https://docs.python.org/2/reference/datamodel.html)

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-

	class Klass(object):
		def func(self):
			pass

		def main(self):
			print 'self.func.im_self: %s' % self.func.im_self
			print 'self.func.im_class: %s' % self.func.im_class
			print 'self.func.im_func: %s' % self.func.im_func

	_kls = Klass()
	_kls.main()

	print '---'

	print '_kls.func.im_self: %s' % _kls.func.im_self
	print '_kls.func.im_class: %s' % _kls.func.im_class
	print '_kls.func.im_func: %s' % _kls.func.im_func

	print '---'

	print 'Klass.func.im_self: %s' % Klass.func.im_self
	print 'Klass.func.im_class: %s' % Klass.func.im_class
	print 'Klass.func.im_func: %s' % Klass.func.im_func

执行结果:

	self.func.im_self: <__main__.Klass object at 0x101a0a390>
	self.func.im_class: <class '__main__.Klass'>
	self.func.im_func: <function func at 0x1019f1f50>
	---
	_kls.func.im_self: <__main__.Klass object at 0x101a0a390>
	_kls.func.im_class: <class '__main__.Klass'>
	_kls.func.im_func: <function func at 0x1019f1f50>
	---
	Klass.func.im_self: None
	Klass.func.im_class: <class '__main__.Klass'>
	Klass.func.im_func: <function func at 0x1019f1f50>

接着回来, 上面的方法, 即:

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	import multiprocessing
	import copy_reg
	import types

	def _pickle_method(m):
		if m.im_self is None:
			return getattr, (m.im_class, m.im_func.func_name)
		else:
			return getattr, (m.im_self, m.im_func.func_name)

	copy_reg.pickle(types.MethodType, _pickle_method)

	class Klass(object):
		def __init__(self):
			print "Constructor ... %s" % multiprocessing.current_process().name

		def __del__(self):
			print "... Destructor %s" % multiprocessing.current_process().name

		def func(self, x):
			print(x * x)

		def run(self):
			pool = multiprocessing.Pool(processes=3)
			for num in range(8):
				pool.apply_async(self.func, args=(num,))
			pool.close()
			pool.join()

	if __name__ == '__main__':
		_kls = Klass()
		_kls.run()

执行代码:

	Constructor ... MainProcess
	0
	1
	4
	... Destructor PoolWorker-1
	9
	... Destructor PoolWorker-2
	16
	... Destructor PoolWorker-1
	36
	... Destructor PoolWorker-3
	25
	... Destructor PoolWorker-1
	49
	... Destructor PoolWorker-2
	... Destructor PoolWorker-1
	... Destructor PoolWorker-3
	... Destructor MainProcess

同上.

另一个方法是, 参考这个[回答](http://stackoverflow.com/a/6975654/1276501), 定义[`__call__`](https://docs.python.org/2/library/stdtypes.html#instance.__class__). 这样就可以将类本身, 如这里的self传给`apply_async`, 因为顶层定义的类是可被序列化的:

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	import multiprocessing

	class Klass(object):
		def __init__(self):
			print "Constructor ... %s" % multiprocessing.current_process().name

		def __del__(self):
			print "... Destructor %s" % multiprocessing.current_process().name

		def __call__(self, x):
			return self.func(x)

		def func(self, x):
			print(x * x)

		def run(self):
			pool = multiprocessing.Pool(processes=3)
			for num in range(8):
				#pool.apply_async(self.func, args=(num,))
				pool.apply_async(self, args=(num,))
			pool.close()
			pool.join()

	if __name__ == '__main__':
		_kls = Klass()
		_kls.run()

执行代码:

	Constructor ... MainProcess
	0
	1
	4
	... Destructor PoolWorker-1
	9
	... Destructor PoolWorker-2
	16
	... Destructor PoolWorker-3
	25
	... Destructor PoolWorker-1
	36
	... Destructor PoolWorker-2
	49
	... Destructor PoolWorker-3
	... Destructor PoolWorker-1
	... Destructor PoolWorker-2
	... Destructor MainProcess

这个[回答](http://stackoverflow.com/a/10217089/1276501)的方法其实和之前设置的代理函数一样, 都是把method提升到global:

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	import multiprocessing

	def call_it(instance, name, args=(), kwargs=None):
		"""indirect caller for instance methods and multiprocessing"""
		if kwargs is None:
			kwargs = {}
		return getattr(instance, name)(*args, **kwargs)

	class Klass(object):
		def __init__(self):
			print "Constructor ... %s" % multiprocessing.current_process().name

		def __del__(self):
			print "... Destructor %s" % multiprocessing.current_process().name

		def func(self, x):
			print(x * x)

		def run(self):
			pool = multiprocessing.Pool(processes=3)
			for num in range(8):
				#pool.apply_async(self.func, args=(num,))
				pool.apply_async(call_it, args=(self, 'func', (num,)))
			pool.close()
			pool.join()

	if __name__ == '__main__':
		_kls = Klass()
		_kls.run()

执行代码:

	Constructor ... MainProcess
	0
	1
	4
	... Destructor PoolWorker-1
	9
	... Destructor PoolWorker-1
	36
	... Destructor PoolWorker-3
	25
	... Destructor PoolWorker-2
	16
	... Destructor PoolWorker-1
	49
	... Destructor PoolWorker-3
	... Destructor PoolWorker-1
	... Destructor PoolWorker-2
	... Destructor MainProcess

关于析构8次的问题，看了`copy_reg`, `pickle`, `multiprocessing`的代码, 还是没什么头绪. 坑爹!

这块考虑, 最还还是把多进程调用的函数抽离出来放在全局是最安全的; 毕竟其它的方案又丑陋, 并且最主要的是各种黑魔法, 完全不清楚内部细节.


---

另外, Python3.3+ 解决了这个问题, 所以在Python3下是可运行的, 这里有个[讨论](http://bbs.chinaunix.net/thread-4111379-1-1.html)
