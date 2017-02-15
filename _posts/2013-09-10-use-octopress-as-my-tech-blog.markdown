---
layout: post
title: "Use octopress as my tech blog"
date: 2013-09-10 21:48
comments: true
categories: Octopress
---

<!-- more -->

[Octopress](http://octopress.org/) is a very great blog framework. I use it as my tech blog.

The [Install Tutorial](http://octopress.org/docs/) is very detailed. Step by step, the environment can be setup easily.

When I install octopress, there are some problems below.

## cannot load such file -- json ##

But when I run `rake generate` after `rake setup_github_pages` in doc [Deploying to Github Pages](http://octopress.org/docs/deploying/github/), there throw an error:

	20:41 tankywoo@gentoo-jl /home/tankywoo/octopress
	% rake generate
	## Generating Site with Jekyll
	directory source/stylesheets/ 
	   create source/stylesheets/screen.css 
	Configuration from /home/tankywoo/octopress/_config.yml
	/home/tankywoo/octopress/plugins/config_tag.rb:1:in `require': cannot load such file -- json (LoadError)
			from /home/tankywoo/octopress/plugins/config_tag.rb:1:in `<top (required)>'
			from /home/tankywoo/.gem/ruby/1.9.1/gems/jekyll-0.12.0/lib/jekyll/site.rb:78:in `require'
			from /home/tankywoo/.gem/ruby/1.9.1/gems/jekyll-0.12.0/lib/jekyll/site.rb:78:in `block (2 levels) in setup'
			from /home/tankywoo/.gem/ruby/1.9.1/gems/jekyll-0.12.0/lib/jekyll/site.rb:77:in `each'
			from /home/tankywoo/.gem/ruby/1.9.1/gems/jekyll-0.12.0/lib/jekyll/site.rb:77:in `block in setup'
			from /home/tankywoo/.gem/ruby/1.9.1/gems/jekyll-0.12.0/lib/jekyll/site.rb:76:in `each'
			from /home/tankywoo/.gem/ruby/1.9.1/gems/jekyll-0.12.0/lib/jekyll/site.rb:76:in `setup'
			from /home/tankywoo/.gem/ruby/1.9.1/gems/jekyll-0.12.0/lib/jekyll/site.rb:31:in `initialize'
			from /home/tankywoo/.gem/ruby/1.9.1/gems/jekyll-0.12.0/bin/jekyll:238:in `new'
			from /home/tankywoo/.gem/ruby/1.9.1/gems/jekyll-0.12.0/bin/jekyll:238:in `<top (required)>'
			from /home/tankywoo/.gem/ruby/1.9.1/bin/jekyll:23:in `load'
			from /home/tankywoo/.gem/ruby/1.9.1/bin/jekyll:23:in `<main>'

I have searched the two posts:

* [Adventures in Ruby](http://warewolf.github.io/blog/2013/04/28/adventures-in-ruby/)
* [{RUBY} json not found by package](http://forums.gentoo.org/viewtopic-t-960332.html?sid=53f1db817289a2bebd65d615eef39a07)

I change the `Gemfile` in `octopress`, add:

	gem 'json', '1.7.7'

and then:

	bundle install

All right:

	20:54 tankywoo@gentoo-jl /home/tankywoo/octopress
	% rake generate
	## Generating Site with Jekyll
	identical source/stylesheets/screen.css 
	Configuration from /home/tankywoo/octopress/_config.yml
	Building site: source -> public
	Successfully generated site: source -> public

## Add Custom Domain ##

After add domain, then:

	rake generate
	rake deploy

## New Post ##

I create a new post as the doc [Blogging Basics](http://octopress.org/docs/blogging/) says:

	21:31 tankywoo@gentoo-jl /home/tankywoo/octopress
	% rake new_post["Use octopress as my tech blog"]
	zsh: no matches found: new_post[Use octopress as my tech blog]

I use `zsh`, so:

	21:32 tankywoo@gentoo-jl /home/tankywoo/octopress
	% rake new_post\["Use octopress as my tech blog"\]
	mkdir -p source/_posts
	Creating new post: source/_posts/2013-09-10-use-octopress-as-my-tech-blog.markdown

After solve all the problems, my tech blog is ok.
