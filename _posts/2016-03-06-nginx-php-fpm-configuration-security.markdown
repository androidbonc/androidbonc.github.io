---
layout: post
title: "Nginx 和 PHP-FPM 权限安全配置"
date: 2016-03-06 14:30
---

环境:

- 一台Gentoo宿主机
- 两个WordPress博客
- Nginx
- PHP-FPM 5.6
- MySQL

需要做到两个WordPress博客权限上互相安全隔离。


大致步骤:

- 新建两个系统用户: blog1, blog2. shell是nologin.
- MySQL 新建两个用户blog1/blog2, 两个新数据库dbblog1/dbblog2, 分别将用户开放给各自数据库
- WordPress压缩包解压后, 属主全部改为blog1/blog2
- PHP-FPM 使用sock通信; 进程属主是blog1/blog2, sock文件的属主是blog1/blog2, 属组是nginx; 开启chroot
- Nginx进程权限是nginx

---

以下记录步骤, 只针对blog1, blog2和blog1配置完全一样, 改其中个别字段即可:

创建两个系统服务用户:

因为是作为服务用户, 所以shell需要设置为`/sbin/nologin` 禁止登录; 另外, 不需要生成home目录.

	$ useradd -u 1201 -s /sbin/nologin -d /dev/null blog1


MySQL新建用户, 数据库, 配置权限:

数据库级别权限隔离, 且各用户只有自己相关数据库的权限.

	CREATE DATABASE dbblog1;
	CREATE USER 'blog1'@'localhost' IDENTIFIED BY '<password>';
	GRANT ALL ON dbblog1.* TO 'blog1'@'localhost';
	FLUSH PRIVILEGE;


WordPress压缩包解压, 更改文件属主:

属主更改是为了PHP-FPM有权限读写站点文件.

	$ tar zxvf wordpress-4.4.2-zh_CN.tar.gz
	$ mv wordpress blog1
	$ chown -R blog1 blog1
	$ ls -alhd blog1
	drwxr-xr-x 5 blog1 nogroup 4.0K Feb  3 08:13 blog1


PHP-FPM 配置:

首先修改主配置 `/etc/php/fpm-php5.6/php-fpm.conf`:

注释掉 `Pool Definitions` 中的所有配置项, 即去掉默认的 `www` Pool; 开启 `include` 项:

	; Include one or more files. If glob(3) exists, it is used to include a bunch of
	; files from a glob(3) pattern. This directive can be used everywhere in the
	; file.
	; Relative path can also be used. They will be prefixed by:
	;  - the global prefix if it's been set (-p argument)
	;  - /usr/lib64/php5.6 otherwise
	include=/etc/php/fpm-php5.6/etc/fpm.d/*.conf

每个web site一个独立的php-fpm配置(具体解释看默认的配置文件):

	$ cat /etc/php/fpm-php5.6/etc/fpm.d/blog1.conf
	[blog1]
	user = blog1    ; php-fpm子进程的uid
	group = nogroup

	listen = /var/run/php-fpm-blog1.sock
	listen.owner = nginx    ; sock通信文件的属主, 和nginx通信
	listen.group = nginx    ; sock通信文件的属组, 和nginx通信
	listen.mode = 0660

	pm = dynamic
	pm.max_children = 5
	pm.start_servers = 2
	pm.min_spare_servers = 1
	pm.max_spare_servers = 3

	chroot = /var/www/blog1
	chdir = /

配置 `user` 是为了控制权限, 读写站点文件.

配置 `listen.owner/group` 是为了nginx有权限和php-fpm通信.

设置 `chroot` 到站点目录下, 限制最小访问权限. 命令 `pwdx` 可以查看指定进程的当前工作目录.

	$ ps aux | grep php
	root      5646  0.0  0.3 247836  7192 ?        Ss   14:55   0:00 php-fpm: master process (/etc/php/fpm-php5.6/php-fpm.conf)
	blog1     5647  0.0  0.6 247944 13884 ?        S    14:55   0:00 php-fpm: pool blog1
	blog1     5648  0.0  0.6 247812 13192 ?        S    14:55   0:00 php-fpm: pool blog1
	blog2     5649  0.0  1.4 251840 29756 ?        S    14:55   0:00 php-fpm: pool blog2
	blog2     5650  0.0  0.3 247812  6636 ?        S    14:55   0:00 php-fpm: pool blog2
	root     10071  0.0  0.1 112700  2100 pts/4    S+   15:52   0:00 grep --color php

	$ pwdx 5647
	5647: /var/www/blog1


Nginx配置:

	server {
		listen 80;
		server_name blog1.tankywoo.com;

		index index.php;

		access_log /var/log/nginx/blog1_log main;
		error_log /var/log/nginx/blog1_error_log;

		root /var/www/blog1/;

		location ~ .php$ {
			try_files      $uri  =404;
			fastcgi_pass   unix:///var/run/php-fpm-blog1.sock;
			include        fastcgi.conf;
			fastcgi_param  SCRIPT_FILENAME    /$fastcgi_script_name;
		}
	}

注意 `fastcgi_param` 配置. 如果是默认的:

	 fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;

则PHP-FPM(fastcgi)读取index.php, 即/var/www/blog1/inex.php.

而因为PHP-FPM配置了chroot, 所以这个目录是当对于chroot后的目录.

即实际读取/var/www/blog1/var/www/blog1/index.php


---

中间过程中, 遇到几个报错:

php-fpm log:

> php-fpm chroot FastCGI sent in stderr: "Primary script unknown" while reading response header from upstream

找不到php文件, 原因就是fastcgi的`SCRIPT_FILENAME`配置之前没配.

> 数据库连接失败

原因是WordPress默认是通过socket连接数据库, 而此时web site是chroot的, 所以没法找到sock文件.

方法1是把sock文件mount进去:

	$ mkdir -p /var/www/blog1/var/run/mysqld
	$ mount --bind /var/run/mysqld /var/www/blog1/var/run/mysqld

不过此方法不够完美。

方法2就是将WordPress改为通过tcp链接MySQL, wp-config.php 增加:

	define('DB_HOST', '127.0.0.1');

---

参考链接:

* [Nginx and PHP-FPM Configuration and Optimizing Tips and Tricks](http://www.if-not-true-then-false.com/2011/nginx-and-php-fpm-configuration-and-optimizing-tips-and-tricks/)
* [How To Host Multiple Websites Securely With Nginx And Php-fpm On Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-host-multiple-websites-securely-with-nginx-and-php-fpm-on-ubuntu-14-04)
* [Nginx + PHP-FPM with chroot](https://gir.me.uk/nginx-php-fpm-with-chroot/)
* [Apache + PHP-FPM + chroot results “File not found.” error](http://stackoverflow.com/a/16674537/1276501)
