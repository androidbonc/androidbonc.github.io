---
layout: post
title: "MySQL 存储过程"
date: 2015-04-01 16:00
---

MySQL 存储过程(Stored Procedure) 是通过给定的语法格式编写自定义的数据库API, 包含一系列sql语句的集合, 完成一个复杂的功能. 这个API可以反复使用, 执行效率也很高.

功能上有点像function, 但是和function还是有些区别.

存储过程的参数有三种类型:

* `IN`: 输入参数. 在调用存储过程时指定, 默认未指定类型时则是此类型.
* `OUT`: 输出参数. 在存储过程里可以被改变, 并且可返回.
* `INOUT`: 输入输出参数. IN 和 OUT 结合

(关于IN和OUT的区别, 个人理解IN比较像C/C++中的传值, OUT像引用)

一个基本的格式:

	DELIMITER //
	DROP PROCEDURE IF EXISTS usp_demo;
	CREATE PROCEDURE usp_demo(IN param1 INT,...)
	BEGIN
		-- Do SQL Operation
	END //
	DELIMITER ;

一般会在存储过程开始时将结束符改为其它字符, 在结束时改回原来的.

原因:

> Because we want to pass the stored procedure to the server as a whole rather than letting mysql tool to interpret each statement at a time.  Following the `END` keyword, we use the delimiter `//` to indicate the end of the stored procedure.

(摘自: [Getting Started with MySQL Stored Procedures](http://www.mysqltutorial.org/getting-started-with-mysql-stored-procedures.aspx))

然后定义存储过程, 参数可有可无, 就和编码写函数一样, 定义几个参数, 调用时就写几个参数.

然后以`BEGIN`开始, 以`END`结束. 里面是一系列的SQL语句, 并且还提供了结构控制语句, 比如 `IF`, `WHILE`, `CASE`等等, 可以完成复杂的操作.

另外, 定义存储过程, 以`usp_`前缀是区别系统存储过程和用户自定义存储过程的[最佳实践](http://www.oschina.net/translate/create-and-call-mysql-stored-procedure-database-sql-example-tutorial).

定义存储过程后, 通过`CALL`命令调用:

	CALL <usp_name>;

`DECLARE` 声明局部变量:

	DECLARE var_name,[var_name...] data_type DEFAULT default_value

如:

	DECLARE a, b, c INT DEFAULT 5;

`SET` 对已声明的变量赋值或重新赋值.

`SELECT` 显示变量; `SELECT var into out_var` 将变量值写入OUT参数

如:

	DELIMITER //
	DROP PROCEDURE IF EXISTS usp_demo;
	CREATE PROCEDURE usp_demo(OUT num INT)
	BEGIN
		DECLARE myvar INT;
		SET myvar = (SELECT id FROM users LIMIT 1);
		SELECT myvar into num;
	END //
	DELIMITER ;

	mysql> set @a=1;
	Query OK, 0 rows affected (0.00 sec)

	mysql> call usp_demo(@a);
	Query OK, 1 row affected (0.00 sec)

	mysql> select @a;
	+------+
	| @a   |
	+------+
	| 3938 |
	+------+
	1 row in set (0.00 sec)

简单例子:

	DELIMITER //
	DROP PROCEDURE IF EXISTS usp_demo;
	CREATE PROCEDURE usp_demo(IN num INT)
	BEGIN
		select num;
		set num = 100;
		select num;
	END //
	DELIMITER ;

	mysql> CALL usp_demo(1);
	+------+
	| num  |
	+------+
	|    1 |
	+------+
	1 row in set (0.00 sec)

	+------+
	| num  |
	+------+
	|  100 |
	+------+
	1 row in set (0.00 sec)

	Query OK, 0 rows affected (0.00 sec)

	mysql> select @a;
	+------+
	| @a   |
	+------+
	|  5   |
	+------+
	1 row in set (0.00 sec)

<!-- -->

	mysql> set @a = 5;
	Query OK, 0 rows affected (0.00 sec)

	mysql> CALL usp_demo(@a);
	+------+
	| num  |
	+------+
	|    5 |
	+------+
	1 row in set (0.00 sec)

	+------+
	| num  |
	+------+
	|  100 |
	+------+
	1 row in set (0.00 sec)

	Query OK, 0 rows affected (0.00 sec)

<!-- -->

	DELIMITER //
	DROP PROCEDURE IF EXISTS usp_demo;
	CREATE PROCEDURE usp_demo(OUT num INT)
	BEGIN
		set num = 100;
		select num;
	END //
	DELIMITER ;

	mysql> set @a = 5;
	Query OK, 0 rows affected (0.00 sec)

	mysql> CALL usp_demo(@a);
	+------+
	| num  |
	+------+
	|  100 |
	+------+
	1 row in set (0.00 sec)

	Query OK, 0 rows affected (0.00 sec)

	mysql> select @a;
	+------+
	| @a   |
	+------+
	|  100 |
	+------+
	1 row in set (0.00 sec)

其它命令:

* `SHOW PROCEDURE STATUS` 列出所有存储过程
* `SHOW CREATE PROCEDURE <sp_name>` 查看一个已存在的存储过程的信息


参考:

* [MySQL Stored Procedure](http://www.mysqltutorial.org/mysql-stored-procedure-tutorial.aspx)
* [An Introduction to Stored Procedures in MySQL5](http://code.tutsplus.com/articles/an-introduction-to-stored-procedures-in-mysql-5--net-17843)

---

[事件(Event)](http://dev.mysql.com/doc/refman/5.1/en/events.html), 可以定义一些任务调度.

首先需要开启事件调度的支持:

	SET GLOBAL event_scheduler = 1;

[创建语法](http://dev.mysql.com/doc/refman/5.1/en/create-event.html):

	CREATE EVENT [IF NOT EXISTS] <event_name>
	ON SCHEDULE <schedule>
	DO
	<event_body>;

其它命令:

* `SHOW EVENTS` 列出所有事件
* `SHOW CREATE EVENT <event_name>` 查看一个已存在的事件的信息

参考:

* [Working with MySQL Scheduled Event](http://www.mysqltutorial.org/mysql-triggers/working-mysql-scheduled-event/)

---

一个存储过程配合事件的例子:

使用事件, 每半小时调用存储过程, 存储过程是一个WHILE循环, 一直删除2个小时之前的数据, 每次删除1000条.

	-- 定义存储过程
	DELIMITER //
	DROP PROCEDURE IF EXISTS usp_del_user;
	CREATE PROCEDURE usp_del_user(IN expire_interval INT, IN delete_per_count INT)
	-- expire_interval: the unit is hour
	-- delete_per_count: specify the count do every delete operation
	BEGIN
	    WHILE EXISTS (select 1 from users where ts < DATE_SUB(NOW(), INTERVAL expire_interval HOUR)) DO
	        delete from users order by ts limit delete_per_count;
	    END WHILE;
	END //
	DELIMITER ;

	-- 定义事件, 调用存储过程
	DROP EVENT IF EXISTS del_user;
	CREATE EVENT del_user
	ON SCHEDULE EVERY 30 MINUTE
	DO
	CALL usp_del_user(2, 1000)

---

在本地测试创建存储过程的时候, 遇到这个报错:

> ERROR 1548 (HY000): Cannot load from mysql.proc. The table is probably corrupted

应该是mysql升级后有些表格的信息需要相应升级, 修复:

	sudo mysql_upgrade -uroot -p

---

MySQL 输出时的`\G`

有时使用`SHOW`输出一些信息表格时, 限制于屏幕的宽度, 表格会比较混乱. 加上`\G`后显示效果如:

	mysql> show events\G;
	*************************** 1. row ***************************
					  Db: testsp
					Name: delete_user
				 Definer: root@localhost
			   Time zone: SYSTEM
					Type: RECURRING
			  Execute at: NULL
		  Interval value: 5
		  Interval field: SECOND
				  Starts: 2015-03-26 17:26:27
					Ends: NULL
				  Status: ENABLED
			  Originator: 1
	character_set_client: utf8
	collation_connection: utf8_general_ci
	  Database Collation: utf8_general_ci
	1 row in set (0.00 sec)

这种左右的结构看上去就会比较美观.
