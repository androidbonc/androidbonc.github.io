---
layout: post
title: "netsnmp, python-binding, 和打包"
date: 2015-07-12 09:00
---

netsnmp [主页](http://sourceforge.net/projects/net-snmp/)

Ubuntu 12.04 下, 源里的netsnmp版本是5.4.3:

    % apt-get install libsnmp-base libsnmp15 snmp snmpd libsnmp-python

其中 libsnmp-python 是 netsnmp 的 [python bindings](http://net-snmp.sourceforge.net/wiki/index.php/Python_Bindings). 还有其它的netsnmp python api, 如pysnmp等.

安装后, 根据相应的netsnmp版本, 参考文档做好配置, 执行以下测试:

    % snmpwalk -v 2c -c public localhost sysDescr
    sysDescr: Unknown Object Identifier (Sub-id not found: (top) -> sysDescr)

原因是因为找不到相应的mib module, 默认情况下, ubuntu安装好netsnmp后只有一些基本的mib文件(猜测可能和版本有关).

不过已经有了相应的工具, 安装:

    % apt-get install snmp-mibs-downloader

会安装一个mib下载/管理工具, 并且同时会装上相应的mib文件.

这里手工直接把mib文件copy到mib搜索路径也可以, 我就是这么做的. 因为snmp-mibs-downloader会安装太多的mib文件, 很多用不到...

安装了mib文件后, 再次执行测试命令还是找不到oid. 这次的原因是因为:

**默认情况下, ubuntu的配置, 禁止了导入mib module; 在centos[6|7], gentoo下是没有这个配置, 所以没这个问题**

可以:

    % snmpwalk -v 2c -c public localhost SNMPv2-MIB::sysDescr
    SNMPv2-MIB::sysDescr.0 = STRING: Linux ubuntu 3.5.0-23-generic #35~precise1-Ubuntu SMP Fri Jan 25 17:13:26 UTC 2013 x86_64

    # 或者

    % snmpwalk -v 2c -c public -m SNMPv2-MIB localhost sysDescr
    SNMPv2-MIB::sysDescr.0 = STRING: Linux ubuntu 3.5.0-23-generic #35~precise1-Ubuntu SMP Fri Jan 25 17:13:26 UTC 2013 x86_64

最根本的原因, 是因为 `/etc/snmp/snmp.conf` 这个配置文件:

    % more /etc/snmp/snmp.conf
    #
    # As the snmp packages come without MIB files due to license reasons, loading
    # of MIBs is disabled by default. If you added the MIBs you can reenable
    # loaging them by commenting out the following line.
    mibs :

在centos[6|7] 和 gentoo 下默认装好是没有这个配置的.

根据注释的解释, 可以知道, 这个是禁止导入mib module, 所以需要手工指定mib module.

方法1是去掉冒号, 添加相应的mib module.

注意mib module不是mib 文件名, 一般的路径是在:

    /root/.snmp/mibs:/usr/share/mibs/site:/usr/share/snmp/mibs:/usr/share/mibs/iana:/usr/share/mibs/ietf:/usr/share/mibs/netsnmp

不同版本, 可能会有不同, 具体可以参考文档, 也可以通过写一个错误的mib module名:

    % snmpwalk -v 2c -c public -m xxx localhost sysDescr
    MIB search path: /root/.snmp/mibs:/usr/share/mibs/site:/usr/share/snmp/mibs:/usr/share/mibs/iana:/usr/share/mibs/ietf:/usr/share/mibs/netsnmp
    Cannot find module (xxx): At line 0 in (none)
    sysDescr: Unknown Object Identifier (Sub-id not found: (top) -> sysDescr)

如果目录存在且里面有mib文件, 则也会有相应的`.index`索引

mib module名一般就是这里面的mib文件(暂时看到都是.txt文件)去掉后缀的名称.

查看snmp.conf的man手册:

    % man 5 snmp.conf

    mibs MIBLIST
        specifies a list of MIB modules (not files) that should be loaded.  This operates in the same way as the -m option - see snmpcmd(1) for details.  Note that this list can be overridden by the MIBS environment variable, and the -m option.

继续查看snmpcmd的man手册:

    % man 1 snmpcmd

    -m MIBLIST
          Specifies a colon separated list of MIB modules (not files) to load for this application.  This overrides (or augments) the environment variable MIBS, the snmp.conf directive mibs, and the list of MIBs hardcoded into the Net-SNMP library.

          If MIBLIST has a leading '-' or '+' character, then the MIB modules listed are loaded in addition to the default list, coming before or after this list respectively.  Otherwise, the specified MIBs are loaded instead of this default list.

          The special keyword ALL is used to load all MIB modules in the MIB directory search list.  Every file whose name does not begin with "." will be parsed as if it were a MIB file.

根据这个, 可以知道, 如snmp.conf里配置mibs有`+`, `-`, 则是前插入和后追加的方式, 追加到默认的mibs module. 否则如上面默认的一个冒号, 则是清空默认导入的mibs module.

这块听坑爹的, 看了半天文档和strace追踪, 才发现是这里问题.

centos[6|7] 下则比较简单, 直接:

    yum install net-snmp.x86_64 net-snmp-utils.x86_64 net-snmp-libs.x86_64 net-snmp-python.x86_64

则会装上相应的netsnmp实现, 命令, mib库, 和python api.

---

(net-snmp在ubuntu下的名字叫的误导人, 不然也不会去尝试打包了...)

关于netsnmp的deb打包, 包括netsnmp, 和它的python api.

这块只是简单了看了一些博客和文档, 依葫芦画瓢做的, 具体还是得读一遍文档.

使用的是dh-make, debhelper等相关工具:

    % apt-get install build-essential dpkg-dev dh-make debhelper dpkg-sign autotools-dev

另外, netsnmp依赖perl库, 否则报错:

    > /usr/bin/ld: cannot find -lperl

    % sudo apt-get install libperl-dev

下载net-snmp-5.7.3.tar.gz, 解压后, cd 进入目录

    % dh_make -e me@tankywoo.com -f ../net-snmp-5.7.3.tar.gz

    Type of package: single binary, indep binary, multiple binary, library, kernel module, kernel patch?
     [s/i/m/l/k/n] s

    Maintainer name  : root
    Email-Address    : me@tankywoo.com
    Date             : Sun, 12 Jul 2015 09:21:55 +0800
    Package Name     : net-snmp
    Version          : 5.7.3
    License          : blank
    Type of Package  : Single
    Hit <enter> to confirm:
    Currently there is no top level Makefile. This may require additional tuning.
    Done. Please edit the files in the debian/ subdirectory now. You should also
    check that the netsnmp Makefiles install into $DESTDIR and not in / .

会生成一个debian目录, 里面包含了`dpkg-buildpackage`需要的基本配置, 删除一些无用文件:

    % rm -rf *.ex *.EX README.* docs copyright source

编辑剩下的 changelog, compat, control, rules 文件, 除了rules外, 其它几个都比较好弄, 主要是rules:

    wutq ~/debian % more rules
    #!/usr/bin/make -f
    # -*- makefile -*-
    # Sample debian/rules that uses debhelper.
    # This file was originally written by Joey Hess and Craig Small.
    # As a special exception, when this file is copied by dh-make into a
    # dh-make output file, you may use that output file without restriction.
    # This special exception was added by Craig Small in version 0.37 of dh-make.

    # Uncomment this to turn on verbose mode.
    #export DH_VERBOSE=1

    %:
            dh $@

    override_dh_auto_configure:
            ./configure --with-default-snmp-version="2" --with-sys-contact="@@no.where" --with-sys-location="Unknown" --with-logfile="/var/l
    og/snmpd.log" --with-persistent-directory="/var/net-snmp"

    # ignore dh_usrlocal
    override_dh_usrlocal:

`override_dh_auto_configure` 和 `override_dh_usrlocal` 都是我添加的.

因为./configure时, 会有一些提交需要手动配上, 可以直接用参数来配置.

`override_dh_usrlocal`如果没配上, [dh_usrlocal](http://man.he.net/man1/dh_usrlocal)会在清理目录时报错(TODO 这个暂时还没搞懂具体是干啥的):

    ...
    dh_usrlocal: debian/tmp/usr/local/lib/perl/5.14.2/NetSNMP/agent/Support.pm is not a directory
    rmdir: failed to remove `debian/tmp/usr/local/lib/perl/5.14.2/NetSNMP/agent': Directory not empty
    dh_usrlocal: rmdir debian/tmp/usr/local/lib/perl/5.14.2/NetSNMP/agent returned exit code 1
    make: *** [binary] Error 1
    dpkg-buildpackage: error: debian/rules binary gave error exit status 2


    % dh_usrlocal
    ...
    dh_usrlocal: debian/tmp/usr/local/lib/perl/5.14.2/NetSNMP/agent/Support.pm is not a directory
    rmdir: failed to remove `debian/tmp/usr/local/lib/perl/5.14.2/NetSNMP/agent': Directory not empty
    dh_usrlocal: rmdir debian/tmp/usr/local/lib/perl/5.14.2/NetSNMP/agent returned exit code 1

---

TODO:

参考这个[讨论](http://forums.debian.net/viewtopic.php?f=8&t=52928), 怀疑可能需要保留debian/source/format 这个文件.

或者增加:

    export PREFIX=/usr

另外参考这个netsnmp 5.7.3 rules:

https://tracker.debian.org/media/packages/n/net-snmp/rules-5.7.3%2Bdfsg-1

---


在源码目录执行打包命令:

    % dpkg-buildpackage -uc -b

    ...
     dpkg-genchanges -b >../netsnmp_5.7.3-1_amd64.changes
    dpkg-genchanges: binary-only upload - not including any source code
     dpkg-source --after-build net-snmp-5.7.3
    dpkg-buildpackage: binary only upload (no source included)

打包完成后, 会在net-snmp-5.7.3.tar.gz 平级目录生成一个changes和deb文件:

    % ll
    total 9484
    drwxr-xr-x  3 root root    4096 Jul 12 10:11 .
    drwx------  9 root root    4096 Jul 12 10:13 ..
    drwxrwxr-x 20 1274 1274    4096 Jul 12 10:08 net-snmp-5.7.3
    -rw-r--r--  1 root root     656 Jul 12 10:11 net-snmp_5.7.3-1_amd64.changes
    -rw-r--r--  1 root root 3308488 Jul 12 10:11 net-snmp_5.7.3-1_amd64.deb
    -rw-r--r--  1 root root 6382428 Jul 12 09:12 net-snmp-5.7.3.tar.gz

netsnmp的python binding也是类似的, 首先在netsnmp源码下有python目录, 包括setup.py都写好了, 直接把这个目录单独copy出来:

    % cp -r net-snmp-5.7.3/python  python-netsnmp-5.7.3
    % tar czvf python-netsnmp-5.7.3.tar.gz python-netsnmp-5.7.3

然后和上面类似, 在python-netsnmp-5.7.3目录生成debian, rules这里比较简单, 直接:

    % more rules
    #!/usr/bin/make -f
    # -*- makefile -*-
    # Sample debian/rules that uses debhelper.
    # This file was originally written by Joey Hess and Craig Small.
    # As a special exception, when this file is copied by dh-make into a
    # dh-make output file, you may use that output file without restriction.
    # This special exception was added by Craig Small in version 0.37 of dh-make.

    # Uncomment this to turn on verbose mode.
    #export DH_VERBOSE=1

    %:
            dh $@ --with python2

注意在dpkg-buildpackage前, 需要先装上net-snmp, 这个python binding用到了C扩展, 里面的引用了一些net-snmp的头文件:

    dpkg -i net-snmp_5.7.3-1_amd64.deb

然后再做python netsnmp的deb包.

接下来再抽时间了解下rpm的打包.

---

一些可以参考的文档/博客:

* [netsnmp snmpwalk](http://www.net-snmp.org/wiki/index.php/TUT:snmpwalk)
* [netsnmp using local mibs](http://net-snmp.sourceforge.net/tutorial/tutorial-5/commands/mib-options.html)
* [netsnmp faq](http://www.net-snmp.org/docs/FAQ.html)
* [netsnmp using and loading mibs](http://www.net-snmp.org/wiki/index.php/TUT:Using_and_loading_MIBS)
* [Installing net-snmp MIBs on Ubuntu and Debian](https://l3net.wordpress.com/2013/05/12/installing-net-snmp-mibs-on-ubuntu-and-debian/)
* [SNMPv2-MIB](http://www.oidview.com/mibs/0/SNMPv2-MIB.html)
* [Net-Snmp on Ubuntu](http://www.net-snmp.org/wiki/index.php/Net-Snmp_on_Ubuntu)
* [centos 下安装netsnmp](http://thgenius.blog.51cto.com/1042803/917086) 中间折腾时遇到了一些问题, 这个博客上都整理了, 不过现在再弄, 想不出来是哪里导致的这个问题了...
* [How to create a Debian package](http://santi-bassett.blogspot.kr/2014/07/how-to-create-debian-package.html)
* [Why is dh_usrlocal throwing a build error?](http://stackoverflow.com/questions/7459644/why-is-dh-usrlocal-throwing-a-build-error)
* [dpkg-shlibdeps: error: no dependency information found for](http://stackoverflow.com/questions/11238134/dpkg-shlibdeps-error-no-dependency-information-found-for)
* [Deb打包入门](http://blog.csdn.net/michaelwubo/article/details/41942483)
* [debian包维护手册](https://www.debian.org/doc/manuals/maint-guide/index.zh-cn.html)
* [rules文件语法](https://www.debian.org/doc/manuals/maint-guide/dreq.zh-cn.html#rules)
* [为Debian和Ubuntu制作软件包](https://www.ibm.com/developerworks/community/blogs/5144904d-5d75-45ed-9d2b-cf1754ee936a/entry/%25e4%25b8%25badebian%25e5%2592%258cubuntu%25e5%2588%25b6%25e4%25bd%259c%25e8%25bd%25af%25e4%25bb%25b6%25e5%258c%2585_%25e4%25b8%2580?lang=en)
