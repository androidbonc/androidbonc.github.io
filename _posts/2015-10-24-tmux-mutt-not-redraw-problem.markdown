---
layout: post
title: "Tmux下Mutt没有重绘终端窗口的问题"
date: 2015-10-24 18:00
---

现象: 使用mutt查看邮件, 连续查看下一封, 或者按q回退到邮件列表, 屏幕上字符会混乱, 也就是比如看到下一封邮件, 但是有些地方还是上一封的内容字符, 并没有完全重绘(redraw)窗口.

这个问题困扰了很长一段时间, 多次搜索无果, 找不到切入点.

这两天又试了下, 发现在tmux下运行mutt会有这个问题, 否则是正常的. Google "tmux mutt not flush" 搜出这篇回答: [Tmux + mutt not redrawing](http://superuser.com/questions/844058/tmux-mutt-not-redrawing)

试了下, 果然是这个原因.

查看`man tmux`关于default-terminal的设置:

>   Set the default terminal for new windows created in this session - the default value of the TERM environment variable.  For tmux to work correctly, this must be set to `screen' or a derivative of it.

这个是设置新建窗口的`TERM`环境变量, 默认是`screen`. 另外这里还强调了必须设置screen或它的衍生. 而我设置的是`xterm-256color`. 于是改为:

	set -g default-terminal "screen-256color"

另外, tmux设置`TERM`是在加载~/.zshrc之前, 所以如果在~/.zsh中设置了`TERM`, 还要做一定的定制:

	if [ -z "$TMUX" ] && [[ "$TERM" =~ "xterm" ]]; then
		if [ -e /usr/share/terminfo/*/xterm-256color ]; then
			echo "1"
			export TERM='xterm-256color'
		else
			echo "2"
			export TERM='xterm-color'
		fi
	elif [ -n "$TMUX" ]; then
		if [ -e /usr/share/terminfo/*/screen-256color ]; then
			echo "3"
			export TERM='screen-256color'
		else
			echo "4"
			export TERM='screen'
		fi
	fi

这里有两个地方说明下:

* `$TMUX` 环境变量, 在使用tmux后, 这个变量是一个路径值
* `-e /usr/share/terminfo/*/xterm-256color`, 在linux下, `*`这个其实是terminal type的首字母, 但是mac os下不是这样, 我原先设置的是`-e /usr/share/terminfo/x/xterm-256color`, 在mac下不工作.

如果shell配置中没有设置`TERM`, 则只需要配置tmux.conf即可.

问题解决, mutt查看邮件的闹心问题总算没了

---

(
TL;DR

并且没有完全弄清楚, 可能会有理解错误的地方
)

tty, pty, pts: (`man 4 xxx`查看手册)

`tty`, [Tele TYpewriter](https://en.wikipedia.org/wiki/Teleprinter) 是一个终端设备, 是硬件设备(如[VT100](https://en.wikipedia.org/wiki/VT100) 或由 内核仿真(如`Ctrl+Alt+F1~F6`, 虚拟控制台).

> * A tty is a native terminal device, the backend is either hardware or kernel emulated.
> * The TTY is a terminal that doesn't require X or any program to exist, aka a Real Terminal. So you can use that terminal even when X fails to load. (kernel stuff)

`pty, pts`, [pseudoterminal](https://en.wikipedia.org/wiki/Pseudoterminal), 伪终端. 是由普通程序仿真出来, 如screen, ssh等. pty分为ptmx(master)和pts(slave).

> * A pty (pseudo terminal device) is a terminal device which is emulated by an other program (example: xterm, screen, or ssh are such programs).
> * In practice, pseudo-terminals are used for implementing terminal emulators such as xterm
> * A PTS is a a Pseudo Terminal that needs a program to exist. You can launch several PTS in the same TTY. Both behaviors almost the same. (user stuff)

Linux/Mac 下按 `w` 可以看到登录情况以及terminal name:

	# 这台机器是部署在虚拟机上
	# tty1 是我直接在虚拟机终端输入帐号密码登录进去
	# pts/0 是通过ssh登录上去
	tankywoo ~ % w
	 18:13:38 up 13 days,  6:08,  2 users,  load average: 0.02, 0.04, 0.05
	USER     TTY        LOGIN@   IDLE   JCPU   PCPU WHAT
	tankywoo tty1      17:59   14:05   0.36s  0.34s -zsh
	tankywoo pts/0     17:41    0.00s  0.57s  0.00s w


参考:

* [What is the difference between a TTY terminal and a PTS graphical terminal in Linux?](https://www.quora.com/What-is-the-difference-between-a-TTY-terminal-and-a-PTS-graphical-terminal-in-Linux)
* [Difference between pts and tty](http://unix.stackexchange.com/questions/21280/difference-between-pts-and-tty)

terminal, console, terminal emulator, terminal multiplexer

[terminal emulator](https://en.wikipedia.org/wiki/Terminal_emulator), 终端仿真器.

> * is a program that emulates a video terminal within some other display architecture.
> * provides a standardised character based interface for text mode applications, it emulates the behavior of real or idealised hardware.

如基于X Window的[xterm](https://en.wikipedia.org/wiki/Xterm), KDE默认的terminal [konsole](https://en.wikipedia.org/wiki/Konsole), Mac下比自带更好用的[iTerm2](https://en.wikipedia.org/wiki/ITerm2), Win下的 [PuTTY](https://en.wikipedia.org/wiki/PuTTY)和[XShell](https://en.wikipedia.org/wiki/Xshell).

这是一份完整的列表[List of terminal emulators](https://en.wikipedia.org/wiki/List_of_terminal_emulators)

[terminal multiplexer](https://en.wikipedia.org/wiki/Terminal_multiplexer), 终端复用器.

> is a software application that can be used to multiplex several virtual consoles, allowing a user to access multiple separate terminal sessions inside a single terminal window or remote terminal session.

如系统自带的[screen](https://en.wikipedia.org/wiki/GNU_Screen), Ubuntu下有名的[Byobu](https://en.wikipedia.org/wiki/Byobu_(software)), 以及[tmux](https://en.wikipedia.org/wiki/Tmux)

关于`console`和`terminal`, 其实在日常的技术交流中, 这两个基本是等价的. 所以这里这里要是深究其区别, 并追溯历史原因, 是一件很蛋疼的事情.

> * A **terminal** refers to a wrapper program which runs a shell. Decades ago, this was a physical device consisting of little more than a monitor and keyboard. As unix/linux systems added better multiprocessing and windowing systems, this terminal concept was abstracted into software. Now you have programs such as Gnome Terminal which launches a window in a Gnome windowing environment which will run a shell into which you can enter commands.
> * The **console** is a special sort of terminal. Historically, the console was a single keyboard and monitor plugged into a dedicated serial console port on a computer used for direct communication at a low level with the operating system. Modern linux systems provide virtual consoles. These are accessed through key combinations (e.g. `Alt+F1` or `Ctrl+Alt+F1`; the function key numbers different consoles) which are handled at low levels of the linux operating system -- this means that there is no special service which needs to be installed and configured to run. Interacting with the console is also done using a shell program.


参考:

* [What is the difference between a Console, Shell, Terminal, Terminal emulator, Terminal multiplexer, and a Window manager?](http://unix.stackexchange.com/questions/33881/what-is-the-difference-between-a-console-shell-terminal-terminal-emulator-te)
* [What is the difference between shell, console, and terminal?](http://superuser.com/a/144668/251495) 比较认可这篇的解释
* [What is the difference between Terminal, Console, Shell, and Command Line?](http://askubuntu.com/questions/506510/what-is-the-difference-between-terminal-console-shell-and-command-line) 这个帖子的一些回答都值得看看
* [What is the exact difference between a 'terminal', a 'shell', a 'tty' and a 'console'?](http://unix.stackexchange.com/questions/4126/what-is-the-exact-difference-between-a-terminal-a-shell-a-tty-and-a-con)
* [console vs terminal](http://linuxmantra.com/2010/04/console-vs-terminal.html)

结合上面的这些说下自己的理解:

> * tty和pty其实都可以总称tty(terminal).
> * console是一个特殊的terminal.
> * terminal一般用于指terminal emulator
> * 直接显示器连服务器看到的是console

其实, 这块还是不纠结, 就当作一回事比较好, 基于历史原因, 曾经的terminal, console现在都software/virtual化了.

查了几个小时, 越看越晕.

关于`$TERM`环境变量, 定义terminal type (`man 7 term`):

> * The  environment  variable TERM should normally contain the type name of the terminal, console or display-device type you are using.  This  information  is  critical for all screen-oriented programs, including your editor and mailer.
> * associates the terminal you are using with a list of characteristics given in the terminfo(M) database. The characteristics tell the system how to interpret your terminal's keys and how to display data on your terminal screen.
> * The $TERM variable is for use by applications to take advantage of capabilities of that terminal.
> * For example, if a program want's to display colored text, it must first find out if the terminal you're using supports colored text, and then if it does, how to do colored text.
> * The way this works is that the system keeps a library of known terminals and their capabilities. On most systems this is in /usr/share/terminfo (there's also termcap, but it's legacy not used much any more).

`toe` 可以查看支持的terminal type

`/usr/share/terminfo/` 是一个数据库, 存放是支持的terminal功能

`infocmp <term type 1> <term type 2>` 用于对比两个term的不同

参考:

* [Which terminal type am I using?](http://unix.stackexchange.com/questions/93376/which-terminal-type-am-i-using) 解释的比较详细
* [What's the difference between various $TERM variables?](http://unix.stackexchange.com/questions/43945/whats-the-difference-between-various-term-variables)
* [Terminal emacs colors only work with TERM=xterm-256color](http://stackoverflow.com/questions/7617458/terminal-emacs-colors-only-work-with-term-xterm-256color)

个人理解, terminal emulator 和 terminal type的关系, 有点类似Linux发行版和系统内核的关系. 比如guake和gnome-terminal这两个terminal emulator都是GNOME终端, terminal type可以是gnome一系的.

常规的万金油设置一般就是`screen-*`或者`xterm-*`


其它:

iTerm 在 Profiles -> Terminal -> Report Terminal Type 里可以设置终端仿真器的类型.

这个可以被shell配置(.basrc/.zshrc/...)中配置的`$TERM`环境变量覆盖.

* [How does a Linux terminal work?](http://unix.stackexchange.com/questions/79334/how-does-a-linux-terminal-work)
* [Text-Terminal-HOWTO](http://oss.sgi.com/LDP/HOWTO/Text-Terminal-HOWTO-9.html)
* [How are “xterm” and “screen” related?](http://unix.stackexchange.com/questions/140139/how-are-xterm-and-screen-related)
* [系统变量TERM不知是用来干什么的？它的值有vt100，vt220等，这些值代表什么意思？](http://www.cnblogs.com/dkblog/archive/2009/07/16/1980729.html)
