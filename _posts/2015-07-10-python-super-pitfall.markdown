---
layout: post
title: "扯下Python的super()"
date: 2015-07-10 00:00
---

注: Python 2.7.x 环境下

今晚搜东西无意中看到这篇[Understanding Python super() with `__init__()` methods](http://stackoverflow.com/questions/576169/understanding-python-super-with-init-methods).

其实这篇老早就看过了, 不过有一篇很好的[回答](http://stackoverflow.com/a/19257335/1276501)之前没有注意到.

首先说下`super()`, 我只在类的单继承时的`__init__()`中使用过.

注意super只能用在新式类(new-style class)中, 也就是继承自object类对象的子类:

{% highlight python %}
class A(object):
	....
{% endhighlight %}

以前遇到过一个问题, 排查了半天, 才发现是老式类定义.

传统的super使用方法如:

{% highlight python %}
class Base(object):
	def __init__(self, id):
		self.id = id

class Child(Base):
	def __init__(self, id, name):
		super(Child, self).__init__(id)
		self.name = name
{% endhighlight %}

这个是Python2.2之后才支持的特性, 在之前只能:

{% highlight python %}
class Child(Base):
	def __init__(self, id, name):
		Base.__init__(self, id)
		self.name = name
{% endhighlight %}

这样做的好处就是不需要显示的在初始化时指明Child的父类名是什么, 在复杂的继承环境下, 以致会牵一发动一身.

不过就像那篇帖子top1的回答里所说:

> But the main advantage comes with multiple inheritance

super在多继承这种更复杂的环境下, 才能发挥真正的威力, 这也是[python文档](https://docs.python.org/2/library/functions.html#super)中提到的第二个使用场景. 当然至今没遇到过这种复杂环境, 所以没有发言权.

---

上面扯了一些super的基本情况, 接着该扯下帖子里top2的[回答](http://stackoverflow.com/a/19257335/1276501)了.

里面提到了这个用法:

{% highlight python %}
super(self.__class__, self).__init__()
{% endhighlight %}

关于`__class__`:

	instance.__class__ : The class to which a class instance belongs.

因为前阵子在使用多线程(`threading.Thread`)时, 写了一个基类, 然后有两个类分别继承自这个基类, 设置线程名就是类名, 这时就用到了`__class__`:

{% highlight python %}
class base_thread(threading.Thread):
	def __init__(self, **kwargs):
		threading.Thread.__init__(self)
		self.name = self.__class__.__name__
{% endhighlight %}

所以对这个比较敏感, 才留意了下这个回答, 没想到却发现了一些坑...

按照帖子里的那个回复:

> This unfortunately does not necessarily work if you want to inherit the constructor from the superclass.

例子:

{% highlight python %}
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Polygon(object):
	def __init__(self, id):
		self.id = id

class Rectangle(Polygon):
	def __init__(self, id, width, height):
		super(self.__class__, self).__init__(id)
		self.shape = (width, height)

class Square(Rectangle):
	pass

p = Polygon(10)
print p.id

r = Rectangle(5, 1, 2)
print r.id

s = Square(20, 2, 4)
print s.id
{% endhighlight %}

运行结果:

	% python test.py
	10
	5
	Traceback (most recent call last):
	  File "test.py", line 65, in <module>
		s = Square(20, 2, 4)
	  File "test.py", line 53, in __init__
		super(self.__class__, self).__init__(id)
	TypeError: __init__() takes exactly 4 arguments (2 given)

执行到Square类时, 报错说应该有4个参数, 但是实际上只有两个.

简化下代码, 并加一些调试输出:

{% highlight python %}
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Polygon(object):
	def __init__(self, id):
		print('in Polygon, self.__class__ is %s' % self.__class__)
		self.id = id

class Rectangle(Polygon):
	def __init__(self, id, width, height):
		super(self.__class__, self).__init__(id)
		#super(Rectangle, self).__init__(id)
		print('in Rectangle, self.__class__ is %s' % self.__class__)
		self.shape = (width, height)

p = Polygon(10)
print p.id

r = Rectangle(5, 1, 2)
print r.id
{% endhighlight %}

结果是:


	% python test.py
	in Polygon, self.__class__ is <class '__main__.Polygon'>
	10
	in Polygon, self.__class__ is <class '__main__.Rectangle'>
	in Rectangle, self.__class__ is <class '__main__.Rectangle'>
	5

可以看出来, 在Rectangle初始化时, 通过super调用父类Polygon进行初始化, 而 `__class__`还是Rectangle.

所以在上一个例子中, Square因为和Rectangle的初始化方法一样, 所以初始化时会调用:

	super(Square, self).__init__(id)

即:

	Rectangle.__init__(id)

但是实际上Rectangle接收4个参数的初始化, 所以这里报错.

接着考虑, 解决参数个数不一致的问题? 那么就让参数多一致:

{% highlight python %}
#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Polygon(object):
	def __init__(self, id, width, weight):
		print('in Polygon, self.__class__ is %s' % self.__class__)
		self.id = id

class Rectangle(Polygon):
	def __init__(self, id, width, height):
		super(self.__class__, self).__init__(id, width, height)
		#super(Rectangle, self).__init__(id)
		print('in Rectangle, self.__class__ is %s' % self.__class__)
		self.shape = (width, height)

class Square(Rectangle):
	def __init__(self, id, width, height):
		super(self.__class__, self).__init__(id, width, height)
		#super(Rectangle, self).__init__(id)
		print('in Square, self.__class__ is %s' % self.__class__)
		self.shape = (width, height)


p = Polygon(10, 3, 6)
print p.id

r = Rectangle(5, 1, 2)
print r.id

s = Square(20, 2, 4)
print s.id
{% endhighlight %}

运行报错:

	% python test.py
	in Polygon, self.__class__ is <class '__main__.Polygon'>
	10
	in Polygon, self.__class__ is <class '__main__.Rectangle'>
	in Rectangle, self.__class__ is <class '__main__.Rectangle'>
	5
	Traceback (most recent call last):
	  File "test.py", line 30, in <module>
		s = Square(20, 2, 4)
	  File "test.py", line 18, in __init__
		super(self.__class__, self).__init__(id, width, height)
	  File "test.py", line 11, in __init__
		super(self.__class__, self).__init__(id, width, height)
	  File "test.py", line 11, in __init__

	  ...

	  File "test.py", line 11, in __init__
		super(self.__class__, self).__init__(id, width, height)
	  File "test.py", line 11, in __init__
		super(self.__class__, self).__init__(id, width, height)
	  File "test.py", line 11, in __init__
		super(self.__class__, self).__init__(id, width, height)
	RuntimeError: maximum recursion depth exceeded while calling a Python object

在Rectangle的super这一样发生了无限循环.

在Square的super函数里:

	super(self.__class__, self).__init__(id, width, height)

相当于:

	Rectangle.__init__(id, width, height)

而此时在Retangle的super函数里, `__class__`还是等于Square, 所以`super(self.__class__, self)`就是Rectangle自身, 所以在这里发生了死循环.

唯一的做法就是在Square中重定义`__init__`, 并且和`__class__`无关.


这块有点绕, 需要理解下.
