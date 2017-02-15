---
layout: post
title: "Ubuntu get local ipmi configuration"
date: 2013-09-12 15:40
comments: true
categories: Ops
---

<!-- more -->

This way is [clanzx](http://blog.clanzx.net/) told me.

```bash
#cd /sys/class/dmi/id
find /lib/modules/`uname -r`/ -name "ipmi*"
modprobe ipmi_si
modprebe ipmi_devintf
```

and then install `ipmitool` tool.


	$ ipmitool lan print

	Set in Progress         : Set Complete
	Auth Type Support       : NONE MD2 MD5 PASSWORD 
	Auth Type Enable        : Callback : MD2 MD5 
							: User     : MD2 MD5 
							: Operator : MD2 MD5 
							: Admin    : PASSWORD 
							: OEM      : 
	IP Address Source       : Static Address
	IP Address              : X.X.X.X
	Subnet Mask             : X.X.X.X
	MAC Address             : X:X:X:X:X:X
	SNMP Community String   : public
	IP Header               : TTL=0x40 Flags=0x40 Precedence=0x00 TOS=0x10
	Default Gateway IP      : X.X.X.X
	Default Gateway MAC     : X:X:X:X:X:X
	Backup Gateway IP       : X.X.X.X
	Backup Gateway MAC      : X:X:X:X:X:X
	802.1q VLAN ID          : Disabled
	802.1q VLAN Priority    : 0
	RMCP+ Cipher Suites     : 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14
	Cipher Suite Priv Max   : aaaaaaaaaaaaaaa
							:     X=Cipher Suite Unused
							:     c=CALLBACK
							:     u=USER
							:     o=OPERATOR
							:     a=ADMIN
							:     O=OEM
