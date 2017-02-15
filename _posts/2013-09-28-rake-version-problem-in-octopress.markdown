---
layout: post
title: "rake version problem in octopress"
date: 2013-09-28 13:58
comments: true
categories: Octopress
---

<!-- more -->

Recently I have updated `ruby` from 19 to 20, and `rake` also updated.

When I use `rake generate` in octopress, it throws an error:

	tankywoo::octopress/ (source*) » rake generate
	rake aborted!
	You have already activated rake 0.9.6, but your Gemfile requires rake 0.9.2.2. Using bundle exec may solve this.
	/home/tankywoo/.gem/ruby/1.9.1/gems/bundler-1.3.5/lib/bundler/runtime.rb:33:in `block in setup'
	/home/tankywoo/.gem/ruby/1.9.1/gems/bundler-1.3.5/lib/bundler/runtime.rb:19:in `setup'
	/home/tankywoo/.gem/ruby/1.9.1/gems/bundler-1.3.5/lib/bundler.rb:120:in `setup'
	/home/tankywoo/.gem/ruby/1.9.1/gems/bundler-1.3.5/lib/bundler/setup.rb:7:in `<top (required)>'
	/home/tankywoo/octopress/Rakefile:2:in `<top (required)>'
	(See full trace by running task with --trace)

One way is to use `bundle exec rake xxx` instead of `rake xxx`.

The better way is:

Modify the require rake version in `Gemfile`.

	gem 'rake', '~> 0.9'  ---> gem 'rake', '~> 0.9.6'

Then:

	bundle update rake

OK.

