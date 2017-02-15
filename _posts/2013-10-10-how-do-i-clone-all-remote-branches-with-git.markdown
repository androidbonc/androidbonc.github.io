---
layout: post
title: "How do I Clone All Remote Branches with Git"
date: 2013-10-10 14:48
comments: true
categories: Git
---

<!-- more -->

This is a good question I found in StackOverflow.

Url [How do I clone all remote branches with Git?](http://stackoverflow.com/questions/67699/how-do-i-clone-all-remote-branches-with-gite)

The top rate answer is very good:

First, clone a remote Git repository and cd into it:

	$ git clone git://example.com/myproject
	$ cd myproject

Next, look at the local branches in your repository:

	$ git branch
	* master

But there are other branches hiding in your repository! You can see these using the -a flag:

	$ git branch -a
	* master
	  remotes/origin/HEAD
	  remotes/origin/master
	  remotes/origin/v1.0-stable
	  remotes/origin/experimental

If you just want to take a quick peek at an upstream branch, you can check it out directly:

	$ git checkout origin/experimental

But if you want to work on that branch, you'll need to create a local tracking branch:

	$ git checkout -b experimental origin/experimental

Now, if you look at your local branches, this is what you'll see:

	$ git branch
	* experimental
	  master

You can actually track more than one remote repository using git remote.

	$ git remote add win32 git://example.com/users/joe/myproject-win32-port
	$ git branch -a
	* master
	  remotes/origin/HEAD
	  remotes/origin/master
	  remotes/origin/v1.0-stable
	  remotes/origin/experimental
	  remotes/win32/master
	  remotes/win32/new-widgets

At this point, things are getting pretty crazy, so run gitk to see what's going on:

	$ gitk --all &
