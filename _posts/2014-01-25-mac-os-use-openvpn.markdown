---
layout: post
title: "Mac OS Use Openvpn"
date: 2014-01-25 17:58
comments: true
categories: Mac
---

<!-- more -->

Mac 下使用 `Openvpn`。

1. `brew install openvpn`
2. 安装完会提示看 `brew info tuntap`, 按照上面的操作安装 TunTap Extensions。
3. 加载 TunTap Extension。`sudo kextload /Library/Extensions/tun.kext` (*)
4. `cd /usr/local/etc/openvpn`, 然后把配置放到这里。
5. 运行。 `sudo openvpn --config /usr/local/etc/openvpn/xxx.ovpn`

注意用sudo权限运行openvpn。
