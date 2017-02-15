---
layout: post
title: "把博客从Github Pages搬到了VPS上"
date: 2014-02-19 21:20
comments: true
categories: Life
---

<!-- more -->

昨天想把博客的域名从 tech.wutianqi.com 换到 blog.tankywoo.com ，因为这个博客不会再只关注技术，我还会记录一些生活或其他方面的事。

但是，麻烦就来了，忘了Octopress强调过，基于Github Pages的自定义域名，只能指定一个域名，结果我把博客绑定到 blog.tankywoo.com 后，把老域名 tech.wutianqi.com 做CNAME到新域名，这样Github Pages服务肯定是不通过的，直接404。

无奈，只能从Github Pages上搬到我的VPS上，又多了一个麻烦。。。

迁移的过程倒是很简单。按文档来，VPS上[安装rvm](http://octopress.org/docs/setup/)，通过rvm安装ruby，根据[Deploying With Rsync](http://octopress.org/docs/deploying/rsync/)修改 `Rakefile`，然后执行deploy会把相应目录传到指定位置，配置下Nginx就可以了。

然后就是配置老域名作了`301 Redirect`:

	server {
			listen       80;
			server_name blog.tankywoo.com;
			index index.html index.htm;
			root /dir/xxx/;

	}

	server {
		server_name tech.wutianqi.com;
		rewrite ^/(.*) http://blog.tankywoo.com/$1 permanent;

	}

还是自己管理方便，对于Octopress用户，如果切换域名后，老域名的链接还想保留，估计没什么其他好方法了，只能抛弃Github Pages服务。

---

Preview时发现这篇是博客上第一篇中文标题的博客 :)

(完)
