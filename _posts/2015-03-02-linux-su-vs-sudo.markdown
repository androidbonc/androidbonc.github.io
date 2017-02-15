---
layout: post
title: "Linux sudo and su"
date: 2015-03-02 16:00
---

> su - change user ID or become superuser

格式:

    su [options] [username]

`su` 用来切换用户, 后接需要切换的用户名, 不指定用户时默认切换为root

	tankywoo@gentoo-local::~/ » whoami
	tankywoo
	tankywoo@gentoo-local::~/ » pwd
	/home/tankywoo
	tankywoo@gentoo-local::~/ » su
	Password:
	root@gentoo-local::tankywoo/ » whoami
	root
	root@gentoo-local::tankywoo/ » pwd
	/home/tankywoo
	root@gentoo-local::tankywoo/ »

> The current environment is passed to the new shell. The value of $PATH is reset to /bin:/usr/bin for normal users, or /sbin:/bin:/usr/sbin:/usr/bin for the superuser.

su 不接参数, 切换后会停留在之前的路径, `$PATH`环境变量会改为上面提到的.

`-, -l, --login`这个参数是经常用到的(在`sudo su -`中):

> Provide an environment similar to what the user would expect had the user logged in directly.

> When - is used, it must be specified as the last su option. The other forms (-l and --login) do not have this restriction.

使用 `su - [username]` 登录时会使用被登录用户的环境变量.

---

> sudo, sudoedit — execute a command as another user

`sudo` 是用来以某个用户的身份执行命令

管理哪些用户可以使用sudo, 以及用户可执行的命令等, 是在 `/etc/sudoers`中配置的, 比如:

	tankywoo ALL=(ALL) NOPASSWD:ALL

表示 tankywoo 用户可以不需要输入(自己的)密码来执行所有命令

语法:

	users  hosts = (run-as) commands

users 可以在主机 hosts 上以run-as用户身份执行commands

来至[gentoo sudo-guide](https://www.gentoo.org/doc/zh_cn/sudo-guide.xml)的例子:

	# 配置允许swift可以像apache或gorg用户那样执行kill命令
	swift   ALL = (apache, gorg) KILL

	# 当前为swift用户, 执行如下命令:
	sudo -u apache pkill apache

注意这里编辑/etc/sudoers使用`visudo`命令, 而不要直接用vi编辑, 因为如果语法有误, visudo是会在保存时做检查报错的; 曾经直接用vi编辑保存导致无法使用sudo.

sudo最常用的例子就是:

	sudo su
	sudo su -

如果不加sudo, su切换用户时要输入的是被切换用户的密码, 如果使用了sudo, 则切换时使用的是当前用户自己的密码. 加不加`-`的区别在上面提到了.

常用例子, 以某个用户身份执行命令:

	sudo -u [username] [run command]

如:

	# 以newuser身份查看newuser家目录
	tankywoo@gentoo-local::~/ » sudo -u newuser ls ~newuser
	a_file_under_newuser

常用例子, 切换用户:

	sudo -u [username] -i
	sudo -u [username] [shell path]
	sudo -u [username] -s

参数`-i`:

> The -i (simulate initial login) option runs the shell specified by the password database entry of the
> target user as a login shell.  This means that login-specific resource files such as .profile or .login
> will be read by the shell.

类似与上面`su -`一样, 都是使用被切换用户自己的环境变量.

暂时的感觉就是:

	`su - [username]` = `sudo -u [username] -i`

参数`-s` 使用当前环境变量`$SHELL`作为被切换用户的SHELL, 也可以后接指定SHELL, 如:

	$ sudo -u tankywoo /bin/bash

---

总结:

* sudo 是(通过/etc/sudoers配置)让用户在某些方面拥有superuser的权限, 只需要输入自己的密码即可(也可以配置为NOPASSWD)
* su 是切换用户, 需要输入被切换用户的密码
* 两者可以配合使用, 更牛逼

---

关于 login shell 和 non-login shell

ref to [stackexchange](http://unix.stackexchange.com/a/46856/45725):

> A login shell is the first process that executes under your user ID when you log in for an interactive session. The login process tells the shell to behave as a login shell with a convention: passing argument 0, which is normally the name of the shell executable, with a - character prepended 

ref to `man bash - INVOCATION`:

> A login shell is one whose first character of argument zero is a -, or one started with the --login option.

> An interactive shell is one started without non-option arguments and without the -c option whose  standard  input and  error  are both connected to terminals (as determined by isatty(3)), or one started with the -i option.  PS1 is set and $- includes i if bash is interactive, allowing a shell script or a startup file to test this state.

如果当前是login shell, 则通过:

	echo $0

会输出如`-[shell name]`, 以一个横线开始, 或者使用`--login`选项; 否则是non-login shell.

如 `su -`, `bash --login`

---

相关:

* login-shell / non-login shell
* [su VS sudo su VS sudo -u -i](http://johnkpaul.tumblr.com/post/19841381351/su-vs-sudo-su-vs-sudo-u-i) 非常详细的一篇文章(包括讨论)
* [What is the functional difference between sudo su and sudo -i?](http://askubuntu.com/questions/331062/what-is-the-functional-difference-between-sudo-su-and-sudo-i)
* [Difference between Login Shell and Non-Login Shell?](http://unix.stackexchange.com/questions/38175/difference-between-login-shell-and-non-login-shell)
* [differences between login shell and interactive shell](http://stackoverflow.com/questions/18186929/differences-between-login-shell-and-interactive-shell)
* [Difference between Login shell and Non login shell](http://howtolamp.com/articles/difference-between-login-and-non-login-shell/)
