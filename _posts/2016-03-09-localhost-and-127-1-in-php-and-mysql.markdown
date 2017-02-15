---
layout: post
title: "PHP/MySQL中的localhost和127.0.0.1"
date: 2016-03-09 17:00
---

接上一篇 [Nginx 和 PHP-FPM 权限安全配置]({% post_url 2016-03-06-nginx-php-fpm-configuration-security %}) 最后一段关于数据库连接失败的处理。

之前配置WordPress时, 当时想让mysql连接走tcp, google一下就得到答案:

	define('DB_HOST', '127.0.0.1');

但是, 当时没注意看wp-config.php配置, 原先已经有一条配置了:

	define('DB_HOST', 'localhost');

后来在针对Discuz论坛做权限处理时, 因为mysql也是走的unix domain socket, 所以想看看如何改为走tcp, 当时看到是配了localhost, 总想着是不是配一个端口上去就强制走tcp了。

折腾了半天, 还是不行, 直接通过报错定位PHP代码, 最终定位到`mysql_connect()`函数上。

看了文档也没看出哪里有问题, 随手把 `localhost` 改为 `127.0.0.1`, 突然发现行了, 兴奋之余也感觉很莫名其妙。

初以为是PHP对 `localhost` 作了特殊处理, 直接解析为mysql sock路径了。

今天折腾完手头事情再回头看看这个问题。

依然在本地作了一个PHP-FPM chroot的隔离环境, 测试脚本:

	root@gentoo-local /var/www/test % cat index.php
	<meta charset="utf-8">
	<?php
	    define('DB_HOST','localhost');
	    //define('DB_HOST','127.0.0.1');
	    define('DB_USER','root');
	    define('DB_PWD','******');
	
	
	    $connect = mysql_connect(DB_HOST, DB_USER, DB_PWD) or die('数据库连接失败，错误信息：'.mysql_error());
	    echo $connect;
	?>

和昨天的情况一样, 如果是 `localhost`, 则失败; `localhost:3306`也失败; `127.0.0.1` 则OK。

因为知道是哪块的问题, 所以搜索起来离正确的答案也就越来越近。

于是搜到了这篇回答 [Warning: mysql_connect(): [2002] No such file or directory](http://stackoverflow.com/a/8829005/1276501), 里面有一句话:

> The reason is that "localhost" is a special name for the mysql driver making it use the unix socket to connect to mysql instead of the a tcp socket.

这里说是因为mysql对localhost的解析问题。和我之前猜测是PHP解析的不一致。

本地mysql命令行客户端测试, 正常情况下下面两者都OK (`-h localhost` 是默认方式, 可不指定):

	$ mysql -h localhost -u root -p   # OK
	$ mysql -h 127.0.0.1 -u root -p   # OK

因为 localhost 是 `/etc/hosts` 中定义的, 所以临时注释掉这块, 自然localhost就变成无意义的字串了, 再次尝试:

	$ mysql -h localhost -u root -p   # OK
	$ mysql -h 127.0.0.1 -u root -p   # OK

两者依然OK, 所以可以确定原因应该是mysql driver对 db host 的解析问题了。

另外, 通过 `lsof` 也可以看到连接进程的通信:

	# localhost
	mysql 27971 tankywoo  3u  unix 0xffff880078d25540  0t0  371911 type=STREAM

	# 127.0.0.1
	mysql 28249 tankywoo  3u  IPv4 373797       0t0  TCP localhost:50187->localhost:mysql (ESTABLISHED)

按照经验来说, `localhost` 和 `127.0.0.1` 是等价的, 如果主机是非IP地址, 都会尝试去做解析操作。MySQL可能是考虑到unix domain socket效率更高, 所以默认对localhost作了这个处理。

但是这种处理太不明显, 或者说模凌两可, 所以给我的感觉是「坑」的性质更大一些。

后续针对这块又搜了下, 发现遇到这个问题的人真不少, 就比如上面StackOverflow的那个回答, 有接近300的Up vote就能看出来。

:(
