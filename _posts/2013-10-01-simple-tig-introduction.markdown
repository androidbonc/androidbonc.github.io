---
layout: post
title: "Simple Tig Introduction"
date: 2013-10-01 15:57
comments: true
categories: Git
---

# Tig #

> Tig is an ncurses-based text-mode interface for git. It functions mainly as a Git repository browser, but can also assist in staging changes for commit at chunk level and act as a pager for output from various Git commands.

From [Tig](http://jonas.nitro.dk/tig/).

`Tig` use `vi` shortkeys mode, compact perfectly with `Git` , is very powerful.

<!-- more -->

Such a good tool, but many Giters do not know, is so awesome.

![The main and diff view](http://jonas.nitro.dk/tig/screenshots/main-view-split.png)

## Some Simple Usage ##

	# Just enter tig in a git repo
	# tig will list all the commits
	# Choose a commit and enter, tig will show the diff and log
	$ tig

	# Pager Mode
	$ git show | tig

## Read More ##

* [Tig](http://jonas.nitro.dk/tig/)
* [Tig Manual](http://jonas.nitro.dk/tig/manual.html)
* [Tig Github](https://github.com/jonas/tig)
* [git? tig!](http://blogs.atlassian.com/2013/05/git-tig/)
* [Using Tig: A Text Interface for Git](http://ericjmritz.wordpress.com/2013/05/16/using-tig-a-text-interface-for-git/)
* [tig, the ncurses front-end to Git](http://gitready.com/advanced/2009/07/31/tig-the-ncurses-front-end-to-git.html)
