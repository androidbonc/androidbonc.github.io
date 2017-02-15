---
layout: post
title: "List all symbolic links in current directory"
date: 2013-10-09 10:35
comments: true
categories: Linux
---

```bash
	ls -l `find . -maxdepth 1 -type 1 -print`
```

<!-- more -->

Example:

	$ tankywoo::~/ » ls -l `find . -maxdepth 1 -type l -print`
	lrwxrwxrwx 1 tankywoo tankywoo 35 Sep 27 23:47 ./.gitconfig -> /home/tankywoo/.dotfiles/.gitconfig
	lrwxrwxrwx 1 tankywoo tankywoo 34 Sep 26 22:07 ./.screenrc -> /home/tankywoo/.dotfiles/.screenrc
	lrwxrwxrwx 1 tankywoo tankywoo 35 Aug 15 22:33 ./.tmux.conf -> /home/tankywoo/.dotfiles/.tmux.conf
	lrwxrwxrwx 1 tankywoo tankywoo 32 Sep 26 23:59 ./tmux.sh -> /home/tankywoo/.dotfiles/tmux.sh
	lrwxrwxrwx 1 tankywoo tankywoo 31 Aug 15 22:33 ./.vimrc -> /home/tankywoo/.dotfiles/.vimrc
	lrwxrwxrwx 1 tankywoo tankywoo 31 Aug 15 22:33 ./.zshrc -> /home/tankywoo/.dotfiles/.zshrc

Supplement(2013-10-10):

Above command has a little problem. If there is no symlinks in the specified directory, the command equals to `ls -l`, so it will display current directory without filter!

So make sure there are symlinks under the specified directory.

The other way is use `symlinks` command, fisrt install it.

```bash
	symlinks -v .
```

## More ##

* [Display only files and folders that are symbolic links in tcsh or bash](http://stackoverflow.com/questions/1412423/display-only-files-and-folders-that-are-symbolic-links-in-tcsh-or-bash)
* [List all symbolic links in current directory](http://www.commandlinefu.com/commands/view/4138/list-all-symbolic-links-in-current-directory)
