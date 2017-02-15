---
layout: post
title: "About Your Contributions Graph in Github"
date: 2013-12-03 10:23
comments: true
categories: Git
---

最近看了自己Github上的 `Your Contributions` 图表, 发现很多 commits 都没有被统计, 怀疑是因为我提交的不是默认分支.

于是搜了下 Github Help, 找到了答案, 另外在 StackOverflow 上看到有人问了这个问题, 我顺便回答了, 复制过来.

[How to view GitHub Contributors Graph for branches other than master?](http://stackoverflow.com/questions/14972170/how-to-view-github-contributors-graph-for-branches-other-than-master/20341593)

The help of Github [Viewing contributions](https://help.github.com/articles/viewing-contributions) :

> Whenever you commit to a project's `default branch` (or the `gh-pages` branch), `open an issue`, or propose a `Pull Request`, we count that as a contribution.

So:

* default branch
* gh-pages branch
* open an issue
* pull request

only these will be counted.

As @[Mikael](http://stackoverflow.com/a/19004274/1276501) 's answer, you can change the `default branch` in repo's settings.

Another help of Github [Which contributions are counted?](https://help.github.com/articles/why-are-my-contributions-not-showing-up-on-my-profile#which-contributions-are-counted), for commit:

> Your commit contributions are only counted when they are created on or merged into the default branch or gh-pages branch of a non-fork repository.

------

I also want github to count all the commits, not specified branch :(
