---
layout: post
title: "Python的function和unbound/bound method"
date: 2015-07-10 09:00
---

例子扩展自[unbound method和bound method](http://pyzh.readthedocs.org/en/latest/python-questions-on-stackoverflow.html#unbound-methodbound-method), 原文[Class method differences in Python: bound, unbound and static](http://stackoverflow.com/questions/114214/class-method-differences-in-python-bound-unbound-and-static).

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-

	class A(object):
		def foo(self):
			pass

		@staticmethod
		def bar():
			pass

	print 'A.foo: %s' % A.foo
	print 'A().foo: %s' % A().foo
	print "A.__dict__['foo']: %s" % A.__dict__['foo']
	print "A.__dict__['foo'].__get__(None, A): %s" % A.__dict__['foo'].__get__(None, A)
	print "A.__dict__['foo'].__get__(A(), A): %s" % A.__dict__['foo'].__get__(A(), A)
	print '-------------------'
	print 'A.bar: %s' % A.bar
	print 'A().bar: %s' % A().bar
	print "A.__dict__['bar']: %s" % A.__dict__['bar']
	print "A.__dict__['bar'].__get__(None, A): %s" % A.__dict__['bar'].__get__(None, A)
	print "A.__dict__['bar'].__get__(A(), A): %s" % A.__dict__['bar'].__get__(A(), A)

输出:

	% python bind.py
	A.foo: <unbound method A.foo>
	A().foo: <bound method A.foo of <__main__.A object at 0x10c983190>>
	A.__dict__['foo']: <function foo at 0x10c967f50>
	A.__dict__['foo'].__get__(None, A): <unbound method A.foo>
	A.__dict__['foo'].__get__(A(), A): <bound method A.foo of <__main__.A object at 0x10c9831d0>>
	-------------------
	A.bar: <function bar at 0x10c96f5f0>
	A().bar: <function bar at 0x10c96f5f0>
	A.__dict__['bar']: <staticmethod object at 0x10c9811a0>
	A.__dict__['bar'].__get__(None, A): <function bar at 0x10c96f5f0>
	A.__dict__['bar'].__get__(A(), A): <function bar at 0x10c96f5f0>

> As you can see if you access the `foo` attribute on the class you get back an `unbound method`, however inside the class storage (the dict) there is a `function`.
