---
layout: post
title: "cpufrequtils"
date: 2014-05-26 14:52
categories: Linux
---

<!-- more -->

安装[cpufrequtils](https://www.kernel.org/pub/linux/utils/kernel/cpufreq/)，安装完成时会看到对cpu频率做调整:

	root@ubuntu:~# apt-get install cpufrequtils
	...
	Setting up cpufrequtils (007-2) ...
	 * Loading cpufreq kernel modules...                                   [ OK ]
	 * CPUFreq Utilities: Setting ondemand CPUFreq governor...
	 * CPU0...
	 * CPU1...
	 * CPU2...
	 * CPU3...
	 * CPU4...
	 * CPU5...
	 * CPU6...
	 * CPU7...                                                             [ OK ]
	Processing triggers for libc-bin ...
	ldconfig deferred processing now taking place

主要有以下一些文件:

	root@ubuntu:~# dpkg -L cpufrequtils
	/etc/init.d/loadcpufreq
	/etc/init.d/cpufrequtils
	/usr/share/doc/cpufrequtils/examples/cpufrequtils.loadcpufreq.sample
	/usr/share/doc/cpufrequtils/examples/cpufrequtils.sample
	/usr/bin/cpufreq-info
	/usr/bin/cpufreq-set
	/usr/bin/cpufreq-aperf

三个工具:

### cpufreq-info ###

用于查看cpu的相关信息。

比如查看第0个cpu的信息:

	cpufrequtils 007: cpufreq-info (C) Dominik Brodowski 2004-2009
	Report errors and bugs to cpufreq@vger.kernel.org, please.
	analyzing CPU 0:
	  driver: acpi-cpufreq
	  CPUs which run at the same hardware frequency: 0
	  CPUs which need to have their frequency coordinated by software: 0
	  maximum transition latency: 10.0 us.
	  hardware limits: 1.60 GHz - 3.30 GHz
	  available frequency steps: 3.30 GHz, 3.30 GHz, 3.20 GHz, 3.10 GHz, 2.90 GHz, 2.80 GHz, 2.70 GHz, 2.60 GHz, 2.40 GHz, 2.30 GHz, 2.20 GHz, 2.10 GHz, 2.00 GHz, 1.80 GHz, 1.70 GHz, 1.60 GHz
	  available cpufreq governors: powersave, userspace, conservative, ondemand, performance
	  current policy: frequency should be within 1.60 GHz and 3.30 GHz.
					  The governor "ondemand" may decide which speed to use
					  within this range.
	  current CPU frequency is 1.60 GHz (asserted by call to hardware).
	  cpufreq stats: 3.30 GHz:0.37%, 3.30 GHz:0.00%, 3.20 GHz:0.00%, 3.10 GHz:0.00%, 2.90 GHz:0.00%, 2.80 GHz:0.00%, 2.70 GHz:0.00%, 2.60 GHz:0.00%, 2.40 GHz:0.00%, 2.30 GHz:0.00%, 2.20 GHz:0.00%, 2.10 GHz:0.00%, 2.00 GHz:0.00%, 1.80 GHz:0.00%, 1.70 GHz:0.00%, 1.60 GHz:99.62%  (963)

* `dirver`: 实用的cpufreq内核驱动
* `hardware limits`: 设定的cpu频率范围
* `available frequency steps`: 可选的cpu频率
* `available cpufreq governors`: 可选的cpu频率调速器:
	* `powersave` : 节能调速器，CPU以最低频运行
	* `userspace` : 用户空间调速器。以用户设置的cpu频率运行
	* `conservative` : 保守调速器。动根据需求进行升/降频。
	* `ondemand` : 随需应变调速器。默认的方式，自动根据需求进行升/降频。
	* `performance` : 性能调速器，CPU以最大频率运行
* `current CPU frequency`: 当前的CPU频率
* `cpufreq stats`: 统计cpu在每个频率下的工作时间

关于 `conservative` 和 `ondemand` 这两个governors区别，[这里](http://blog.csdn.net/linweig/article/details/5972312)有一段说明:

> ondemand governor 的最初实现是在可选的频率范围内调低至下一个可用频率。这种降频策略的主导思想是尽量减小对系统性能的负面影响，从而不会使得系统性能在短时间内迅速降低以影响用户体验。但是在 ondemand governor 的这种最初实现版本在社区发布后，大量用户的使用结果表明这种担心实际上是多余的， ondemand governor在降频时对于目标频率的选择完全可以更加激进。因此最新的 ondemand governor 在降频时会在所有可选频率中一次性选择出可以保证 CPU 工作在 80% 以上负荷的频率，当然如果没有任何一个可选频率满足要求的话则会选择 CPU 支持的最低运行频率。大量用户的测试结果表明这种新的算法可以在不影响系统性能的前提下做到更高效的节能。在算法改进后， ondemand governor 的名字并没有改变，而 ondemand governor 最初的实现也保存了下来，并且由于其算法的保守性而得名 conservative 。

> Ondemand降频更加激进，conservative降频比较缓慢保守，事实使用ondemand的效果也是比较好的。


### cpufreq-set ###

修改CPU的频率配置

	root@ubuntu:~# cpufreq-set -h
	cpufrequtils 007: cpufreq-set (C) Dominik Brodowski 2004-2009
	Report errors and bugs to cpufreq@vger.kernel.org, please.
	Usage: cpufreq-set [options]
	Options:
	  -c CPU, --cpu CPU        number of CPU where cpufreq settings shall be modified
	  -d FREQ, --min FREQ      new minimum CPU frequency the governor may select
	  -u FREQ, --max FREQ      new maximum CPU frequency the governor may select
	  -g GOV, --governor GOV   new cpufreq governor
	  -f FREQ, --freq FREQ     specific frequency to be set. Requires userspace
							   governor to be available and loaded
	  -r, --related            Switches all hardware-related CPUs
	  -h, --help               Prints out this screen

其中 `-c`指定第几个cpu(cpu从0开始)，没指定则为cpu0；`-d`和`u`指定在**非`userspace`**调速器的最小和最大频率；`-g` 修改调速器类型；`-f`指定cpu频率，只有在调速器是`userspace`时才能使用；`-r` TODO

把governor改为userspace，并调整频率是3.0GHz:

	root@ubuntu:~# cpufreq-set -c 0 -g userspace
	root@ubuntu:~# cpufreq-set -c 0 -f 3.0GHz

然后查看当前频率是3.1GHz:

	root@ubuntu:~# cpufreq-info -c 0 -f -m
	3.10 GHz

因为在 `available frequency steps` 里并没有 3.0GHz，所以会自动使用偏上的3.1GHz

### cpufreq-aperf ###

需要加载`cpuid`和`msr`两个内核模块:

	root@ubuntu:~# cpufreq-aperf -c 0
	CPU     Average freq(KHz)       Time in C0      Time in Cx      C0 percentage
	Could not read cpuid, is the cpuid driver loaded or compiled into the kernel?

	root@ubuntu:~# modprobe cpuid

	root@ubuntu:~# cpufreq-aperf -c 0
	CPU     Average freq(KHz)       Time in C0      Time in Cx      C0 percentage
	Could not read MSRs, is the msr driver loaded or compiled into the kernel?

	root@ubuntu:~# modprobe msr

统计信息:

	root@ubuntu:~# cpufreq-aperf -c 0
	CPU     Average freq(KHz)       Time in C0      Time in Cx      C0 percentage
	000     1782540                 00 sec 001 ms   00 sec 998 ms   00


关于CPU动态变频技术(CPU Dynamic Frequency Scaling)，要将`CONFIG_CPU_FREQ`设置为y。另外要使用governors(调速器)，也需要将相应的调速器内核参数设置为y或m:

	CONFIG_CPU_FREQ_GOV_PERFORMANCE=y
	CONFIG_CPU_FREQ_GOV_POWERSAVE=m
	CONFIG_CPU_FREQ_GOV_USERSPACE=m
	CONFIG_CPU_FREQ_GOV_ONDEMAND=y
	CONFIG_CPU_FREQ_GOV_CONSERVATIVE=m

有几篇文章讲得不错:

* [减少 Linux 电耗，第 1 部分: CPUfreq 子系统](http://www.ibm.com/developerworks/cn/linux/l-cpufreq-1/)
* [Linux的cpufreq（动态变频）技术](http://blog.csdn.net/linweig/article/details/5972312)
* [How to make use of Dynamic Frequency Scaling](http://www.thinkwiki.org/wiki/How_to_make_use_of_Dynamic_Frequency_Scaling)

关于配置:

通过init.d下的脚本可以看到需要两个配置文件:

* `/etc/default/loadcpufreq` : 加载cpufreq驱动模块，自动会加载`acpi-cpufreq`
* `/etc/default/cpufrequtils` 对cpufrequtils进行配置

具体可参考[CPU frequency scaling](https://wiki.archlinux.org/index.php/CPU_frequency_scaling#CPU_frequency_driver) 和 [Cpufrequtils](http://wiki.debianforum.de/Cpufrequtils)(德文)

Sample都在 `/usr/share/doc/cpufrequtils/examples/` 目录下。

另外Intel的机器可以查看`/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor`获取当前的调速器。

	root@ubuntu:/tmp# cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
	performance

**TODO** : AMD的调速方式?
