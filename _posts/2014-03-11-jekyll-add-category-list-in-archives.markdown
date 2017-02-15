---
layout: post
title: "Jekyll add category list in archives"
date: 2014-03-11 13:56
comments: true
categories: Blog
---

<!-- more -->

Archives 页面显示是所有文章的列表, 想把每个分类目录的文章列表也专门显示出来。

首先需要在文章的 Meta 信息里指定目录:

	category: "测试分类目录"

然后这个分类目录名就是"测试分类目录"。

然后在archives模板增加:

(把里面的反斜线都去掉，这里为了防止被解析，不知道如果禁止文章里的模板语句被解析，囧!)

	{\% for category in site.categories %}
	<li><a name="{\{ category | first }}">{\{ category | first }}</a>
	<ul>
	{\% for posts in category %}
		{\% for post in posts %}
		{\% if post.url %}
		<li><a href="{\{ site.baseurl }}{\{ post.url }}">{\{ post.title }}</a></li>
		{\% endif %}
		{\% endfor %}
	{\% endfor %}
	</ul>
	</li>
	{\% endfor %}

这里加了 `if` 语句判断是因为我本地测试发现文章列表 posts 里的第一篇是 category目录名, 所以没有url，在页面上显示是空白的一行，把这行筛选掉就可以了。

参考了Jekyll文档:

* [Variables](http://jekyllrb.com/docs/variables/)
* [Templates](http://jekyllrb.com/docs/templates/)
