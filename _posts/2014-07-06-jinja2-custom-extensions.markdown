---
layout: post
title: "Jinja2 Custom Extensions"
date: 2014-07-06 16:00
categories: Python
---

<!-- more -->

关于Jinja2自定义扩展，也就是标签， [官方文档](http://jinja.pocoo.org/docs/extensions/#module-jinja2.ext)和API介绍的比较简单，网上也没有太多的例子和讨论。

不过好在写起来不是很复杂，参考文档给出的唯一一个样例，以及网上其他人的说明， 花了几个小时给[Simiki](http://simiki.org/)写了一个类似Jekyll的`post_url`的功能。

首先所有自定义的扩展，都应该从`jinja2.ext.Extension`类继承。

给扩展注册一个名称，在模板里调用它(和调用自带标签的方式一样):

	tags = set(['ext_name'])

定义一个`parse(self, parser)`函数，重写`Extension`类的parse函数

在`parse`函数里:

获取lineno(line number)，在创建node时需要用到:

	lineno = parser.stream.next().lineno

获取调用的参数, 参数必须是一个`列表`:

	args = [parser.parse_expression()]

到这里对于不同类型扩展处理就不一样了。

暂时了解的两类扩展: `表达式扩展`和`语句块扩展`

表达式扩展形如以下格式:

	{% raw %}
	{% do_something arg1 arg2 %}
	{% endraw %}

语句块扩展形如以下格式:

	{% raw %}
	{% do_something arg1 arg2 %}
	to be done in this statement block
	...
	{% enddo_something %}
	{% endraw %}

两个的区别就是前者传参然后处理返回结果，后者是传参，并对它包含的语句块做处理。后者的样例还可以找到，前者基本没找到什么例子。


首先，需要知道哪些API的参数类型以及返回类型

在[jinja2.nodes.Node](http://jinja.pocoo.org/docs/extensions/#jinja2.nodes.Node)中介绍了4种类型:

* `Stmt`: statements
* `Expr`: expressions
* `Helper`: helper nodes
* `Template`: the outermost wrapper node

主要关注的是前两个`Stmt` 和 `Expr`

抽取几个主要的API:

	jinja2.ext.Extension.call_method(name, args=None, kwargs=None, dyn_args=None, dyn_kwargs=None, lineno=None)
		Call a method of the extension. This is a shortcut for attr() + jinja2.nodes.Call.


	class jinja2.nodes.Call(node, args, kwargs, dyn_args, dyn_kwargs)
		Calls an expression. args is a list of arguments, kwargs a list of keyword arguments (list of Keyword nodes), and dyn_args and dyn_kwargs has to be either None or a node that is used as node for dynamic positional (*args) or keyword (**kwargs) arguments.
		Node type:	Expr


	class jinja2.nodes.CallBlock(call, args, defaults, body)
		Like a macro without a name but a call instead. call is called with the unnamed macro as caller argument this node holds.
		Node type:	Stmt

对于语句块的扩展，需要获取`body`的内容，也就是语句块括起来的内容:

	body = parser.parse_statements(['name:endext_name'], drop_needle=True)

其中也设置了语句块结束的标签。

然后返回一个`CallBlock`:

	return nodes.CallBlock(self.call_method('_func_do_something', args),
											[], [], body).set_lineno(lineno)

其中`_func_do_something`是类中自定义的一个处理函数，用来处理传进去的参数等内容。

而针对表达式的扩展，因为`parse()`函数期望返回的是`Stmt`，所以也需要返回`CallBlock`:

	return nodes.CallBlock(self.call_method("_func_do_something", args),
											[], [], []).set_lineno(lineno)

只不过设置`body=[]` 就可以了。

我先开始返回`Call`类型，是一个`Expr`，就不行:

	return self.call_method('_func_do_something', args).set_lineno(lineno)

先开始以为在`parse()`函数直接返回`call_method`的结果就行了，因为没有`body`，并不关心，后来发现是错的，还是需要返回`CallBlock`，只不过把`body`设为`[]`就可以了。

感觉这里有机会还得再看看，按理说不应该这么处理的: `parse()`函数返回的应该是一个`Statement Node` TODO

其它的依葫芦画瓢就可以了。


这篇[回复](http://stackoverflow.com/a/1796953/1276501)让我把自定义扩展的大概思路理清了。然后在这个[回复](http://stackoverflow.com/questions/5972458/help-with-custom-jinja2-extension)看到了上面提到的问题，需要返回CallBlock。

另外还有几个其他人写的扩展可以参考:

* [coffin](https://github.com/coffin/coffin/blob/master/coffin/template/defaulttags.py)
* [pygment-extension](https://raw.githubusercontent.com/larrymyers/python-utils/master/pygments_extension.py)
* [csrf\_token extension](https://raw.githubusercontent.com/larrymyers/python-utils/master/pygments_extension.py)
* [jinja2-markdown](https://github.com/qnub/Jinja2-Markdown/blob/master/jinja2_markdown/extensions.py)
* [我写的page\_url](https://github.com/tankywoo/simiki/commit/60a8da8a95464c71d2879c89586fd50c9c8d10ce)
