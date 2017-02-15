---
layout: post
title: "Kill process by process name or script name"
date: 2013-11-18 15:04
comments: true
categories: Linux
---

Kill all processes match the process name or script name:

```bash
ps aux | grep [search string] | awk '{print $2}' | xargs kill -9
```

or use `pkill`:

```bash
pkill -9 -f [search string]
```

From [Linux: How to Kill all instances of a script/program by using a string search](http://heatware.net/linux-unix/linux-how-to-kill-all-instances-of-a-scriptprogram-by-using-a-string-search/)

> -f, --full
> The pattern is normally only matched against the process name.  When -f is set, the full command line is used.
