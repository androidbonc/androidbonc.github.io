---
layout: post
title: "Git Change Commit Message with Remote Repo"
date: 2013-10-10 14:30
comments: true
categories: Git
---

To change the commit message also with repo pushed message:

1. `git rebase -i <hash-of-commit-preceding-the-incorrect-one>`
2. In the editor that opens, change `pick` to `reword` on the line for the incorrect commit.
3. Save the file and close the editor.
4. The editor will open again with the incorrect commit message. Fix it.
5. Save the file and close the editor.
6. git `push --force` to update GitHub.

<!-- more -->

Refer: [Accidently pushed commit: change git commit message](http://stackoverflow.com/a/5032614/1276501)

As one answer in [How do I push amended commit to the remote git repo?](http://stackoverflow.com/questions/253055/how-do-i-push-amended-commit-to-the-remote-git-repo) says:

> I actually once pushed with --force to git.git repository and got scolded by Linus BIG TIME. It will create a lot of problems for other people. A simple answer is "don't do it".

Notice: **rebase** has risk!!! It's better to use for own repo.

PS: To change local commit message, just `git amend`.
