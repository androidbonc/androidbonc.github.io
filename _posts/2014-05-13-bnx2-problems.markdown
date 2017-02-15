---
layout: post
title: "bnx2固件缺少的问题"
date: 2014-05-13 17:50
categories: Ops
---

今天去机房重装几台机器，用Gentoo Livecd做的U盘启动，配置ip后，无法启动网卡，提示说文件或目录不存在。

然后 `ethtool -i eth0` 看了下，是bnx2，印象中在这里栽倒过。

啪啪啪，想了半天，然后发现本地还存放这一个bnx2目录，里面有两个模块文件。

然后想起来之前遇到过这个问题，可悲的是没有做笔记，害我又想了半天。

其实最开始忘了看`dmesg`信息，如果看了就会发现里面很明显的报错提示了:

![bnx2-1](https://tankywoo-wb.b0.upaiyun.com/bnx2-1.png!small)

![bnx2-2](https://tankywoo-wb.b0.upaiyun.com/bnx2-2.png!small)

然后根据提示把相应的模块放到指定位置，重启网络，如果还起不来，再继续看还需要哪些模块。

笔记真心重要，栽倒一次没事，同一个位置栽倒两次就说不过去了。
