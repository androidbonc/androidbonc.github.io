---
layout: post
title: ".gitignore file ignore itself"
date: 2013-11-29 13:31
comments: true
categories: Git
---

<!-- more -->

`.gitignore` 文件忽略他本身?

这确实是一个奇葩的需求, `.gitignore` 作为一个repo的一部分, 本身就应该是存在的, 如果什么都不想忽略, 那么就没必要建一个文件了.

当然, 还是有方法解决这个问题的, 首先如果把 .gitignore 加到 .gitignore 文件中, 是不起作用的.

不过可以加到 `.git/info/exclude` 这个文件中, 具体解释:

> The .gitignore file should be in your repository, so it should indeed be added and committed in, as "git status" suggests. It has to be a part of the repository tree, so that changes to it can be merged and so on.
> 
> So, add it to your repository, it should not be gitignored.
> 
> If you really want you can add .gitignore to the .gitignore file if you don't want it to be committed. However, in that case it's probably better to add the ignores to .git/info/exclude, a special checkout-local file that works just like .gitignore but does not show up in "git status" since it's in the .git folder.
> 
> See also [https://help.github.com/articles/ignoring-files](https://help.github.com/articles/ignoring-files)

参考: [How do I tell Git to ignore “.gitignore”?](http://stackoverflow.com/questions/767147/how-do-i-tell-git-to-ignore-gitignore)
