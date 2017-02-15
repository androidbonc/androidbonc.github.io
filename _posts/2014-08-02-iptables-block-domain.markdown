---
layout: post
title: "Iptables drop domain dns request packet"
date: 2014-08-02 16:00
---

<!-- more -->

Iptables使用[string](http://ipset.netfilter.org/iptables-extensions.man.html) match的`--string`选项是无法直接匹配dns查询中的域名进行操作的。

使用tcpdump查看dns packet:

	15:36:24.918455 IP 100.224.236.84.50546 > ns1.xxx.com.domain: 58178% [1au] A? www.abc.com. (42)
			0x0000:  4500 0046 01c6 0000 3511 7edd 7ce0 ec54  E..F....5.~.|..T
			0x0010:  0aac 9123 c572 0035 0032 e13d e342 0010  ...#.r.5.2.=.B..
			0x0020:  0001 0000 0000 0001 0377 7777 0361 6263  .........www.abc
			0x0030:  0363 6f6d 0000 0100 0100 0100 0029 1000  .com.........)..
			0x0040:  0000 8000 0000                           ......

可以看到, 域名 www.abc.com 的dns查询包，并不是常规的对这个域名做hex处理，其中并不包含点字符(dot character).

	 3 w  w w  3 a  b c  3 c  o m
	0377 7777 0361 6263 0363 6f6d

dns包中，不包含点字符，而是对点字符进行分割，每部分的开始处加入这一段的字符长度。

所以`www`, `abc`, `com`前面分别是数字3.

把这个域名的dns包给drop掉:

	iptables -t raw -I dns_filter -m string --icase --hex-string "|03|www|03|abc|03|com" --algo bm -j DROP

或者:

	iptables -t raw -I dns_filter -m string --icase --hex-string "|037777770361626303636f6d|" --algo bm -j DROP

可以看到规则:

	Chain dns_filter (1 references)
	 pkts bytes target     prot opt in     out     source               destination
		0     0 DROP       all  --  *      *       0.0.0.0/0            0.0.0.0/0           STRING match "|037777770361626303636f6d|" ALGO name bm TO 65535 ICASE

具体也可以看看StackOverflow上的[这篇问答](http://stackoverflow.com/a/17184231/1276501), 以及[这篇文章](http://linux.topology.org/iptables_dns_flood.html)

    [!] --hex-string pattern
          Matches the given pattern in hex notation.

    Examples:

          # The string pattern can be used for simple text characters.
          iptables -A INPUT -p tcp --dport 80 -m string --algo bm --string 'GET /index.html' -j LOG

          # The hex string pattern can be used for non-printable characters, like |0D 0A| or |0D0A|.
          iptables -p udp --dport 53 -m string --algo bm --from 40 --to 57 --hex-string '|03|www|09|netfilter|03|org|00|'


这里 `|` 来标记不可打印的字符，之外的文件都认为是普通ASCII字符.

> The --hex-string parameter parses the provided string looking for hex values delimited by pairs of vertical bars. Anything outside of the vertical bars is interpreted as ASCII text.


另外，这里`--algo`指定匹配字符串的算法

>        --algo {bm|kmp}
>              Select the pattern matching strategy. (bm = Boyer-Moore, kmp = Knuth-Pratt-Morris)

有两个选择，bm算法和kmp算法，kmp算是一个众所周知的字符串匹配算法了，而bm是另一个更高效、精妙的算法。

详细可以看看:

* [字符串匹配的Boyer-Moore算法](http://www.ruanyifeng.com/blog/2013/05/boyer-moore_string_search_algorithm.html)
* [Boyer-Moore算法学习](http://blog.csdn.net/sealyao/article/details/4568167)
