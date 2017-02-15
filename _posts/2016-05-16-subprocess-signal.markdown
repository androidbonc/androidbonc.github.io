---
layout: post
title: "子进程信号问题"
date: 2016-05-16 15:00
---

## 场景 ##

(适当修改了，方便简单模拟)

daemontools管理一个服务serviceA, run脚本:

```sh
#!/bin/bash

exec /opt/srv/mysrv.sh
```

/opt/srv/mysrv.sh脚本：

```sh
#!/bin/bash

# other statements...

ping tankywoo.com >> /tmp/srv.log
```

这里`ping`命令用来模拟一直在前台运行的程序。

使用`svc -d`停止当前服务，发送的是`TERM`信号。([参考](https://cr.yp.to/daemontools/svc.html))

因为run脚本用到`exec`，mysrv.sh脚本停止了，但是ping命令的父进程变为1(init)，然后继续执行。


## 解决 ##

根本原因是信号没有传递到子进程中。

参考这几个帖子：

* [Identifying received signal name in bash shell script](http://stackoverflow.com/questions/9256644/identifying-received-signal-name-in-bash-shell-script)
* [Forward SIGTERM to child in Bash](http://unix.stackexchange.com/questions/146756/forward-sigterm-to-child-in-bash#146770)
* [Linux信号处理机制](http://hutaow.com/blog/2013/10/19/linux-signal/)

使用`trap`命令来指定在接收到信号后做相应的动作。 ([可以看看这篇](http://man.linuxde.net/trap))

```sh
#!/bin/bash

# other statements...

_term() {
    echo "[`date`] Caught SIGTERM in mysrv.sh!" >> /tmp/srv.log
}

trap _term TERM

ping tankywoo.com >> /tmp/srv.log
```

在`kill -TERM <pid_of_run>`时，子shell并不会收到TERM信号。

换个更简单的例子，run脚本：

```sh
#!/bin/bash

ping tankywoo.com >> /tmp/srv.log
```

直接执行run脚本，ping命令是当前shell的一个子shell，如果发送TERM信号，则ping变为父进程是1的进程了。

所以需要加上`exec`，这也是为何第一个场景里需要`exec /opt/srv/mysrv.sh`

所以这里的最简单的解决办法就是在/opt/srv/mysrv.sh中也使用exec：

```sh
#!/bin/bash

# other statements...

exec ping tankywoo.com >> /tmp/srv.log
```

另外，[How to propagate SIGTERM to a child process in a Bash script](http://veithen.github.io/2014/11/16/sigterm-propagation.html)这篇文章总结的很好。使用的是`trap`加`wait`的用法。 (*建议好好读一读*)

/opt/srv/mysrv.sh改为：

```sh
#!/bin/bash

# other statements...

trap 'kill -TERM $PID' TERM INT

ping tankywoo.com >> /tmp/srv.log &   # 注意这行，将ping命令改为后台执行

PID=$!   # 获取上一个放入后台执行的pid
wait $PID  # 等待指定pid的后台进程运行完毕
trap - TERM INT  # 恢复TERM和INT信号的默认行为
wait $PID
EXIT_STATUS=$?

# other statements...
```

至于为何要两次wait，我还没弄太明白。
