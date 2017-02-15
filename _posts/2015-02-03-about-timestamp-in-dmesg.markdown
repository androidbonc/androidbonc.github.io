---
layout: post
title: "关于dmesg的timestamp"
date: 2015-02-03 15:00
---

最近查看dmesg信息, 因为dmesg里给出的是timestamp, 虽然可以通过`date`计算信息时间, 但是比较麻烦, 发现`man dmesg`有相关的参数:

>       -T, --ctime
>              Print human-readable timestamps.
>
>              Be aware that the timestamp could be inaccurate!  The time source used for the logs is not updated after system SUSPEND/RESUME.

可以直接转换为年月日小时分钟秒的可读时间。

接着发现一个问题, 时间有误! 最后几条显示的时间是一个未来的时间, 登录了其它几台, 发现也都是时间不对, 或是未来某个点, 或是之前某个点.

而`/var/log/kern.log`显示的时间则是正确的.

测试, 向 kernel ring buffer 发送一条信息:

    $ echo 'kernel message' > /dev/kmsg

非root用户可以使用([ref](How to add message that will be read with dmesg?)):

    $ echo 'kernel message' | sudo tee /dev/kmsg

也可以使用`printk()`函数来实现, [例子](http://serverfault.com/a/140358/173472).

> The [`/dev/kmsg`](https://www.kernel.org/doc/Documentation/ABI/testing/dev-kmsg) character device node provides userspace access to the kernel's printk buffer.

查看相关日志的时间:

    $ date
    Wed Feb  4 17:04:49 CST 2015

    $ hwclock --show
    Wed 04 Feb 2015 05:04:51 PM CST  -0.594209 seconds

    $ dmesg | tail -1
    [19035481.360508] kernel message

    $ dmesg -T | tail -1
    [Wed Feb  4 20:01:20 2015] kernel message

    $ tail -1 /var/log/kern.log
    2015-02-04T17:04:55.648426+08:00 localhost kernel: [19035481.360508] kernel message

(如果没有显示时间, 确认`/sys/module/printk/parameters/time`的内容是`Y`, 如果是`N`则用`echo`改为`Y`)

可以看到, 系统时间和硬件时间都是正确的, dmesg的timestamp是错误的, 而通过syslog记录到`/var/log/kern.log`中的时间是对的.

注意先前`dmesg -T`的解释, 这个时间戳是不精确的, 如果系统挂起/恢复后, 是不会更新的.

但是, 机器应该都不会做挂起操作, 不清楚这块为何会造成这样. TODO

---

以后尽量还是通过syslog配置的kernel log来查看相关的日志信息, 这样时间是准确的.

---

参考:

* [How to deal with dmesg timestamps](https://blog.sleeplessbeastie.eu/2013/10/31/how-to-deal-with-dmesg-timestamps/)
* [Linux Centos with dmesg timestamp](http://serverfault.com/questions/375273/linux-centos-with-dmesg-timestamp)
