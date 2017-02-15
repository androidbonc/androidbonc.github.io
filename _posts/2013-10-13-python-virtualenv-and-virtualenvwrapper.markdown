---
layout: post
title: "Python virtualenv and virtualenvwrapper"
date: 2013-10-13 17:36
comments: true
categories: Python
---

* virtualenv - Python virtual environment creator
* virtualenvwrapper - extension to virtualenv for managing multiple virtual Python environments

<!-- more -->

Install:

	pip install virtualenv
	pip install virtualenvwrapper

In LinuxMint, I use `apt-get` to install virtualenvwrapper, but some files seem lost, maybe another package need to be installed also.


## Use virtualenv ##

	$ tankywoo@linuxmint::/tmp/ » virtualenv myenv
	New python executable in myenv/bin/python
	Installing distribute.....................................done.
	Installing pip................done.
	
	$ tankywoo@linuxmint::/tmp/ » which python
	/usr/bin/python
	
	$ tankywoo@linuxmint::/tmp/ » source myenv/bin/activate
	
	$ (myenv)tankywoo@linuxmint::/tmp/ » which python
	/tmp/myenv/bin/python

	$ (myenv)tankywoo@linuxmint::/tmp/ » deactivate 

	$ tankywoo@linuxmint::/tmp/ » which python
	/usr/bin/python

Optional Argument:

--no-site-packages : Don't give access to the global site-packages dir to the virtual environment (default)

This is the default argument.

## Use virtualenvwrapper ##

	$ tankywoo@linuxmint::~/ » export WORKON_HOME=~/Envs
	$ tankywoo@linuxmint::~/ » mkdir -p $WORKON_HOME
	$ tankywoo@linuxmint::~/ » source /usr/local/bin/virtualenvwrapper.sh

	$ tankywoo@linuxmint::~/ » mkvirtualenv env1
	New python executable in env1/bin/python
	Installing distribute.....................................done.
	Installing pip................done.

	$ (env1)tankywoo@linuxmint::~/ » which python
	/home/tankywoo/Envs/env1/bin/python

	$ (env1)tankywoo@linuxmint::~/ » ls $WORKON_HOME
	get_env_details  postmkproject     preactivate      prermproject
	initialize       postmkvirtualenv  predeactivate    prermvirtualenv
	postactivate     postrmproject     premkproject
	postdeactivate   postrmvirtualenv  premkvirtualenv


	# This will create env2, and change to it.
	$ (env1)tankywoo@linuxmint::~/ » mkvirtualenv env2
	New python executable in env2/bin/python
	Installing distribute.....................................done.
	Installing pip................done.

	$ (env2)tankywoo@linuxmint::~/ » which python
	/home/tankywoo/Envs/env2/bin/python

	# This will change to env1
	$ (env2)tankywoo@linuxmint::~/ » workon env1
	$ (env1)tankywoo@linuxmint::~/ » 

	# List exist virtual-env
	$ (env1)tankywoo@linuxmint::~/ » lsvirtualenv
	env1
	====

	env2
	====

	# Another way to list exist virtual-env
	# The same as lsvirtualenv -b
	$ (env1)tankywoo@linuxmint::~/ » workon
	env1
	env2

	# This will remove the specified virtual-env
	(env1)tankywoo@linuxmint::~/ » rmvirtualenv env2 
	Removing env2...

	# Exit virtual-env
	$ (env1)tankywoo@linuxmint::~/ » deactivate
	$ tankywoo@linuxmint::~/ »

Use `mkvirtualenv -h` will find that it has a little options and most use `virtualenv`'s options.

Reference: [virtualenvwrapper doc](http://virtualenvwrapper.readthedocs.org/en/latest/)

## pip with virtualenv and virtualenvwrapper #

### Using pip with virtualenv ###

pip is most nutritious when used with virtualenv. One of the reasons pip doesn't install "multi-version" eggs is that virtualenv removes much of the need for it. Because pip is installed by virtualenv, just use path/to/my/environment/bin/pip to install things into that specific environment.

To tell pip to only run if there is a virtualenv currently activated, and to bail if not, use:

	export PIP_REQUIRE_VIRTUALENV=true

To tell pip to automatically use the currently active virtualenv:

	export PIP_RESPECT_VIRTUALENV=true

### Using pip with virtualenvwrapper ###

If you are using virtualenvwrapper, you might want pip to automatically create its virtualenvs in your `$WORKON_HOME`.

You can tell pip to do so by defining `PIP_VIRTUALENV_BASE` in your environment and setting it to the same value as that of `$WORKON_HOME`.

Do so by adding the line:

	export PIP_VIRTUALENV_BASE=$WORKON_HOME

in your .bashrc under the line starting with `export WORKON_HOME`.

From: [pip 1.0.2 doc](https://pypi.python.org/pypi/pip/1.0.2)

