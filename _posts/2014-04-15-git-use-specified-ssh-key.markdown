---
layout: post
title: "Git use Specified SSH Key"
date: 2014-04-15 10:40
comments: true
categories: Git
---

<!-- more -->

##Use `~/.ssh/config`##

	Host gitolite-as-alice
	  HostName git.company.com
	  User git
	  IdentityFile /home/whoever/.ssh/id_rsa.alice

	Host gitolite-as-bob
	  HostName git.company.com
	  User git
	  IdentityFile /home/whoever/.ssh/id_dsa.bob

Then you just use `gitolite-as-alice` and `gitolite-as-bob` instead of the hostname in your URL:

	git remote add alice git@gitolite-as-alice:whatever.git
	git remote add bob git@gitolite-as-bob:whatever.git

Also can see [this](http://stackoverflow.com/a/7927828/1276501) and [this](http://superuser.com/a/232406/251495)

This way is simple, but every link and every one should add a config.

##Use `$GIT_SSH`##

`$GIT_SSH` is an environment variable in git, which can be seen in `man git`:

	GIT_SSH
	   If this environment variable is set then git fetch and git push will use **this
	   command** instead of ssh when they need to connect to a remote system. The
	   $GIT_SSH command will be given exactly two arguments: the username@host (or
	   just host) from the URL and the shell command to execute on that remote system.

	   To pass options to the program that you want to list in GIT_SSH you will need
	   to wrap the program and options into a shell script, then set GIT_SSH to refer
	   to the shell script.

	   Usually it is easier to configure any desired options through your personal
	   .ssh/config file. Please consult your ssh documentation for further details.

write a wapper named ssh-git.sh:

	#!/bin/sh

	if [ -z "$PKEY" ]; then
		# if PKEY is not specified, run ssh using default keyfile
		ssh "$@"
	else
		ssh -i "$PKEY" "$@"
	fi

Then :

	PKEY=~/.ssh/xxx-id_rsa GIT_SSH=/path/to/ssh-git.sh git pull

and `GIT_SSH` can be set to a system environment variable and not need to set `GIT_SSH` every time.

	export GIT_SSH=/path/to/ssh-git.sh
	PKEY=~/.ssh/xxx-id_rsa git pull

Also can see [this](http://stackoverflow.com/a/14493315/1276501), [this](http://superuser.com/a/232375/251495) or [this](http://stackoverflow.com/questions/4565700/specify-private-ssh-key-to-use-when-executing-shell-command-with-or-without-ruby)
