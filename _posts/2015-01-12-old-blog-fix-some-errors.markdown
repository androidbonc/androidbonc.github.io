---
layout: post
title: "处理下老博客的一些问题"
date: 2015-01-12 22:10
---

[老博客](http://www.wutianqi.com/)是用WordPress搭建了, 写了好几年, 最近两年改用Jekyll了, 以前的文章也懒得导过去, 一直扔在那没管了, 前几天才想起来看看, 发现打不开了.

不过`/wp-admin/`管理页面还可以打开, 和以前一样，登录后只显示了左边的菜单栏, 右边都是空白. 索性一起弄下.

登录下VPS, php-cgi和nginx都是正常, 然后发现根分区满了, 当时偷懒, 只建了一个分区, 全部被mysql, 日志, 备份文件占满了, 都没有及时清理. 删除后恢复了.

但是后台页面依然是空白的, 怀疑是插件或主题的不兼容导致. 于是都rename了插件, 还是不行.

接着rename了主题, 正常情况下应该会使用WordPress的默认主题, 但是没有自动切换.

根据[这个帖子](https://wordpress.org/support/topic/change-theme-manually)提示, 修改了`wp_options`表的`template`, `stylesheet`, `current_theme`都为default主题:

    mysql> select * from wp_options where option_name IN ('template', 'stylesheet', 'current_theme');
    +-----------+---------+---------------+--------------+----------+
    | option_id | blog_id | option_name   | option_value | autoload |
    +-----------+---------+---------------+--------------+----------+
    |   3294487 |       0 | current_theme | nosky        | yes      |
    |        48 |       0 | stylesheet    | nosky        | yes      |
    |        47 |       0 | template      | nosky        | yes      |
    +-----------+---------+---------------+--------------+----------+
    3 rows in set (0.00 sec)

    mysql> update wp_options set option_value = 'default' where option_name in ('template', 'stylesheet', 'current_theme');
    Query OK, 3 rows affected (0.00 sec)
    Rows matched: 3  Changed: 3  Warnings: 0

    mysql> select * from wp_options where option_name IN ('template', 'stylesheet', 'current_theme');
    +-----------+---------+---------------+--------------+----------+
    | option_id | blog_id | option_name   | option_value | autoload |
    +-----------+---------+---------------+--------------+----------+
    |   3294487 |       0 | current_theme | default      | yes      |
    |        48 |       0 | stylesheet    | default      | yes      |
    |        47 |       0 | template      | default      | yes      |
    +-----------+---------+---------------+--------------+----------+

修改完后博客页面又恢复了, 但是后台还是空白. 继续搜索, 发现好多人都有这个问题, 在[这个帖子](http://stackoverflow.com/questions/21614237/what-would-cause-wordpress-admin-screen-to-be-blank-except-for-nav-bar)看到了解决方案:

> This was the offending code, and it was in wp-admin\includes\screen.php on line 706:

>     <?php echo self::$this->_help_sidebar; ?>

> It should be:

>     <?php echo $this->_help_sidebar; ?>


测试OK.

继续扔在那吧, 哪天心情好了, 再把WordPress更新下 :(

