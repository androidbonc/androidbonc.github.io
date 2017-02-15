---
layout: post
title: "Tmux protocol version mismatch"
date: 2014-08-11 16:00
---

Tmux 升级后，运行任何 tmux命令都报以下信息:

    $ tmux ls
    protocol version mismatch (client 8, server 7)

这是因为新版本的client/server是 v8, 而老的server是v7

最暴力的办法就是 `pkill -9 tmux`

当然，真正原因还是因为运行着老的server在

想要恢复老的Session, 可以先找到运行老tmux server的pid(可能有多个):

    $ pgrep tmux
    4234

然后恢复会话:

    $ /proc/4234/exe attach

`/proc/<tmux pid>/exe` 其实就是 `/usr/bin/tmux` 的软链接:

    $ ll /proc/4234/exe
    /proc/4234/exe -> /usr/bin/tmux

参考:

* [protocol version mismatch (client 8, server 6) when trying to upgrade](http://unix.stackexchange.com/questions/122238/protocol-version-mismatch-client-8-server-6-when-trying-to-upgrade)
* [Google Group](https://plus.google.com/110139418387705691470/posts/BebrBSXMkBp)
