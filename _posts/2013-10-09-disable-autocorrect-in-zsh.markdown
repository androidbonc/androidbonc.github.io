---
layout: post
title: "Disable AutoCorrect in Zsh"
date: 2013-10-09 11:29
comments: true
categories: Zsh
---

The `auto-correct` feature of zsh is sometimes helpful, but most time will annoy me.

Such as:

	$ tankywoo::octopress/ (source*) » ls
	_deploy  Gemfile  plugins  public  ...
	$ tankywoo::octopress/ (source*) » rake deploy 
	zsh: correct 'deploy' to '_deploy' [nyae]? 

<!-- more -->

To disable this feature, there are some ways.

## Disable autocorrect on specific command ##

	alias rake='nocorrect rake'

`nocorrect` is a precommand modifier that prevents a spell check on any following words.

## Disable autocorrect entirely ##

For newer versions of zsh:

	unsetopt correct

For older version of zsh:

	unsetopt correct-all

## Use oh-my-zsh ##

The newer version of oh-my-zsh can control this feature:

	# Uncomment following line if you want to disable autosetting terminal title.       
	# DISABLE_AUTO_TITLE="true"

default is enable, uncomment it and disable autocorrect feature.


## References ##

* [Github- oh-my-zsh issues](https://github.com/robbyrussell/oh-my-zsh/issues/534)
* [Disabling Autocorrect in Zsh](https://coderwall.com/p/jaoypq)
* [How to partially disable the zsh's autocorrect](http://superuser.com/questions/439209/how-to-partially-disable-the-zshs-autocorrect)
* [How to partially disable the zsh's autocorrect](http://earthwithsun.com/questions/439209/how-to-partially-disable-the-zshs-autocorrect)
