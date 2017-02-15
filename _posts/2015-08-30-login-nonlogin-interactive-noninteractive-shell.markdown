---
layout: post
title: "Login/Non-Login and Interactive/Non-Interactive Shell"
date: 2015-08-30 15:00
---

首先, 看一看`man bash - INVOCATION`一节.

看完其实下面写的基本都可以忽略~~

## Interactive / Non-Interactive Shell ##

交互和非交互shell

交互shell从用户在终端(tty/pts)下读取输入的命令, 执行并返回结果.

非交互shell一般是执行的shell脚本等, 可以在后台执行.

这个一般都比较好区分.

可以通过环境变量`$PS1`来判断, 在non-interactive shell下, 是空值:

    [ -z $PS1  ] && echo 'non-interactive' || echo 'interactive'

也可以通过`$-`来判断, 这个输出的是当前shell的flag(`set`配置的). 参考[set options](http://www.tldp.org/LDP/abs/html/options.html), 其中`i`表示interactive shell.

    [[ $- == *i*   ]] && echo 'interactive' || echo 'not-interactive'

参考:

* [ABS - Interactive and non-interactive shells and scripts](http://www.tldp.org/LDP/abs/html/intandnonint.html)
* [Different shell types: interactive, non-interactive, login](https://www.vanimpe.eu/2014/01/18/different-shell-types-interactive-non-interactive-login/)


## Login / Non-Login Shell ##

login shell 是指用户登录系统时的shell. 比如tty输入帐号密码登录, 或者远程ssh登录, `su -`, 或者`bash -l/--login`新建的子shell.

non-login shell 是在登录系统后新建的shell, 比如X-Window下打开一个terminal, 则不需要再次输入帐号密码, 或者执行shell脚本, 或者执行如bash新建一个子shell.

login shell和non-login shell最明显的区别就是shell进程名有一个连字符(hyphen):

    $ ps -f
    UID            PID  PPID  C STIME TTY          TIME CMD
    tankywoo      2012 31511  0 16:08 pts/76   00:00:00 ps -f
    tankywoo     31511  6085  0 15:31 pts/76   00:00:01 -zsh

    $ bash

    $ ps -f
    UID            PID  PPID  C STIME TTY          TIME CMD
    tankywoo      2019 31511  0 16:08 pts/76   00:00:00 bash
    tankywoo      2025  2019  0 16:08 pts/76   00:00:00 ps -f
    tankywoo     31511  6085  0 15:31 pts/76   00:00:01 -zsh

可以看到, 新建一个子shell bash, 它的ppid是zsh, zsh前面有连字符, bash没有.

关于这里, login shell和non-login shell加载的一些配置文件是不一样的, 不同的shell也不一定.

以bash为例, login shell加载的顺序是:

    /etc/profile
    /etc/profile.d/*.sh (这一步其实是在上面的/etc/profile里source的)
    ~/.bash_profile
    ~/.bash_login
    ~/.profile

后三个是按顺序找到其中一个, 加载后就不再加载后续的.

non-login shell加载顺序是:

    /etc/bash.bashrc
    ~/.bashrc

参考:

* <http://unix.stackexchange.com/a/46856/45725>
* <http://stackoverflow.com/a/18187389/1276501>
* <http://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html>
* [Zsh/Bash startup files loading order (.bashrc, .zshrc etc.)](https://shreevatsa.wordpress.com/2008/03/30/zshbash-startup-files-loading-order-bashrc-zshrc-etc/)


---

这样两两组合, 就有4种类型的shell, 比较常见的就是登录终端的interactive login shell, 以及执行shell脚本时的non-interactive non-login shell


