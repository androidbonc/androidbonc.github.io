---
layout: post
title: "ESXi5.1 remove /sdk service and can't login"
date: 2014-01-20 13:32
comments: true
categories: ESXi
---

<!-- more -->

因为帮忙解决一个问题, 本地测试把 "/sdk" 服务删除后找解决方法。

	vim-cmd proxysvc/remove_service "/sdk" httpsWithRedirect

执行后, 问题就出来了。

无法执行:

	~ # vim-cmd proxysvc/service_list
	Failed to login: Invalid response code: 400 Bad Request

执行`esxcli network` 也有问题:

	~ # esxcli network ip connection list
	Connect to localhost failed: Connection failure

然后通过 vcenter 也登录不了。

按照[文档](http://pubs.vmware.com/vsphere-51/index.jsp?topic=%2Fcom.vmware.vsphere.security.doc%2FGUID-0EF83EA7-277C-400B-B697-04BDC9173EA3.html) 的意思:

> Changes are effective immediately and persist across reboots.

这个是临时生效的命令, reboot 后应该就恢复了。但是我重启了几次, 都不行。(我估计是版本问题, 因为让帮忙解决这个问题的朋友, 他是ESXi5.5, 重启后恢复了。)

找了半天文档, 也跑到 vmware 社区去[提问](https://communities.vmware.com/thread/468479)了, 还是没找到方法。

后来在一个文档([Change Security Settings for a Web Proxy Service](http://pubs.vmware.com/vsphere-51/index.jsp?topic=%2Fcom.vmware.vsphere.security.doc%2FGUID-F70B032F-8C68-4FCC-9E80-E83D0A88B14F.html))里终于找到了方法:

* vi /etc/vmware/rhttpproxy/endpoints.conf
* 增加这行: `/sdk local 8307 redirect allow`
* 然后重启 `rhttpproxy` 服务: `/etc/init.d/rhttpproxy restart`

就可以恢复/sdk了。


