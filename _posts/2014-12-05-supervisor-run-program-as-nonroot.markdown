---
layout: post
title: "Supervisor Run Program as Non-root"
date: 2014-12-05 11:00
---

需求:

一个Tornado程序，使用进程管理工具开两个端口运行.

以用户bob运行，相关的Python库有都通过`pip install --user`装在`/home/bob/.local/`家目录下.

之前使用daemontools控制, 在`/etc/service/`下得建立两个目录, 分别在run脚本写入:

	#!/bin/sh
	exec sudo -u bob -i python /path/to/prog.py --port=6001

和

	#!/bin/sh
	exec sudo -u bob -i python /path/to/prog.py --port=6002

效果:

	$ ps aux | grep captch[a]
	root      8420  0.0  0.0  37112  1556 ?        S    13:43   0:00 sudo -u bob -i python /path/to/prog.py --port=6001
	bob       8421  0.1  0.0  83884 14604 ?        S    13:43   0:00 python /path/to/prog.py --port=6001
	root      8487  0.0  0.0  37112  1548 ?        S    13:43   0:00 sudo -u bob -i python /path/to/prog.py --port=6002
	bob       8488  0.3  0.0  83884 14600 ?        S    13:43   0:00 python /path/to/prog.py --port=6002

如果开多个端口的话，需要建立相应个数的目录，不是很方便，且此方式是通过SHELL建一个子进程运行Python脚本

涉及到Tornado服务的管理，推荐还是用Supervisor.

以前使用supervisor时，`program section`都是使用默认用户, 也就是root用户，这样带来了权限上的风险，所以这里也需要配置为 bob 用户来执行.

	[program:myprog6002]
	command=sudo -u bob -i python /path/to/prog.py --port=6002
	redirect_stderr=true
	stdout_logfile=/home/bob/myprog.log # 这里要注意bob拥有写日志权限
	autostart=true
	autorestart=true
	numproces=1

另外一个改下端口为6001就行，不贴了.

但是这样基本就和用daemontools控制差不多了，不过使用参数选项的方式控制重启、日志等，还是比daemontools方便的.

因为program section 还有一个[`user`配置](http://supervisord.org/configuration.html):

> If supervisord is run as the root user, switch users to this UNIX user account before doing any meaningful processing. This value has no effect if supervisord is not run as root.

在supervisord以root用户运行的情况下，会setuid到这个指定用户来运行程序, 即:

	[program:myprog6002]
	command=python /path/to/prog.py --port=6002
	user=bob
	redirect_stderr=true
	stdout_logfile=/home/bob/myprog.log
	autostart=true
	autorestart=true
	numproces=1

但是使用status查看状态发现报错:

	supervisor> status
	myprog6002                      BACKOFF   Exited too quickly (process log may have details)

查看配置时的日志, 发现找不到相应的Python库，因为这些库是以bob用户使用`pip install --user`装在当前用户的家目录下.

即相当于在root用户下执行`python /path/to/prog.py --port=6002`

接着查到[Supervisor Doc - Subprocess Environment](http://supervisord.org/subprocess.html#subprocess-environment):

> No shell is executed by supervisord when it runs a subprocess, so environment variables such as `USER`, `PATH`, `HOME`, `SHELL`, `LOGNAME`, etc. are not changed from their defaults or otherwise reassigned. **This is particularly important to note when you are running a program from a supervisord run as root with a `user=` stanza in the configuration**.
> Unlike cron, supervisord does not attempt to divine and override “fundamental” environment variables like USER, PATH, HOME, and LOGNAME when it performs a setuid to the user defined within the `user=` program config option. If you need to set environment variables for a particular program that might otherwise be set by a shell invocation for a particular user, you must do it explicitly within the `environment=` program config option. An example of setting these enviroment variables is as below.

	[program:apache2]
	command=/home/chrism/bin/httpd -c "ErrorLog /dev/stdout" -DFOREGROUND
	user=chrism
	environment=HOME="/home/chrism",USER="chrism"

额外开一个program, 运行脚本，输出 `os.environ` 的信息，主要片段:

	'LOGNAME': 'root', 'USER': 'root', 'HOME': '/root', 'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games', 'PWD': '/root', 'SHELL': '/bin/bash'

这里的 `$USER`, `$HOME` 都还是 root.

输出`sys.path`也可以看到`PYTHONPATH`并没有`/home/bob/.local`的搜索路径

如果在SHELL终端操作:

	export HOME=/home/bob
	python /path/to/prog.py --port=6002

则是OK的.

当然，也可以设置`PYTHONPATH`来解决, 不过后者对路径的依赖性太强了, 建议设置`$HOME`

所以这里需要加上`environment`选项:

	[program:myprog6002]
	command=python /path/to/prog.py --port=6002
	user=bob
	environment=HOME="/home/bob",USER="bob"
	redirect_stderr=true
	stdout_logfile=/home/bob/myprog.log
	autostart=true
	autorestart=true
	numproces=1

更新:

	supervisor> update
	myprog6002: stopped
	myprog6002: updated process group

	supervisor> status
	myprog6002                      RUNNING   pid 12178, uptime 0:00:04

效果:

	/etc/service# ps aux | grep captch[a]
	bob      20779  1.0  0.0  83888 14620 ?        S    15:00   0:00 python /path/to/prog.py --port=6001
	bob      20780  1.0  0.0  83888 14612 ?        S    15:00   0:00 python /path/to/prog.py --port=6002

最后感谢下这两篇帖子让我注意到environment这个选项的配置:

* [Incorrect user for supervisor'd celeryd](http://stackoverflow.com/questions/9034709/incorrect-user-for-supervisord-celeryd)
* [How can I have Supervisor running my programs as another user?](http://serverfault.com/questions/529658/how-can-i-have-supervisor-running-my-programs-as-another-user)

DONE...
