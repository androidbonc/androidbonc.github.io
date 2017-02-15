---
layout: post
title: "一次io wait导致负载升高的分析"
date: 2014-04-14 17:22
comments: true
categories: Linux
published: false
---

一台测低配试机器上，发现负载达到将近20，导致操作也比较延迟。正常情况下这台机器连0.3都没超过。

首先用`top`看了是不是有机器占用CPU比较高，然后发现CPU的`us%` 和 `sy%` 等很低，但是 `wa%` 很高，达到接近 50%

	wa -- iowait
	  Amount of time the CPU has been waiting for I/O to complete.


在 [StackOverflow](http://stackoverflow.com/a/12126674/1276501) 上看到一个方法:

	while true; do date; ps auxf | awk '{if($8=="D") print $0;}'; sleep 1; done

这个就是检查哪些进程的stat是 `D`，`man ps` 中的 `PROCESS STATE CODES` 部分对各个状态的解释:

	PROCESS STATE CODES
	Here are the different values that the s, stat and state output specifiers (header "STAT" or "S") will display to describe the state of a process:
	D    uninterruptible sleep (usually IO)
	R    running or runnable (on run queue)
	S    interruptible sleep (waiting for an event to complete)
	T    stopped, either by a job control signal or because it is being traced.
	W    paging (not valid since the 2.6.xx kernel)
	X    dead (should never be seen)
	Z    defunct ("zombie") process, terminated but not reaped by its parent.


另外还有一些io的分析工具: `iotop`, `iostat`, `vmstat`，稍后也整理到 wiki 上。

参考链接:

* [How to find out which process is consuming “wait CPU” (i.e. I/O blocked)](http://stackoverflow.com/questions/666783/how-to-find-out-which-process-is-consuming-wait-cpu-i-e-i-o-blocked)
* [How can I tell what processes are causing high loads if they are not high-cpu usage?](http://serverfault.com/questions/56094/how-can-i-tell-what-processes-are-causing-high-loads-if-they-are-not-high-cpu-us)
* [Diagnosing high CPU waiting](http://serverfault.com/questions/396443/diagnosing-high-cpu-waiting)
* [Tracking Down High IO Wait in Linux](http://ostatic.com/blog/tracking-down-high-io-wait-in-linux)
* [Linux Wait IO Problem](http://www.chileoffshore.com/en/interesting-articles/126-linux-wait-io-problem)
* [http://www.chileoffshore.com/en/interesting-articles/126-linux-wait-io-problem](http://bencane.com/2012/08/06/troubleshooting-high-io-wait-in-linux/) *


dstat --aio --io --disk --tcp --top-io-adv --top-bio-adv
or 
atop -dl
