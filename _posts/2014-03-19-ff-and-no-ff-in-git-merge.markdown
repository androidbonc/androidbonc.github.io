---
layout: post
title: "ff and no-ff in git merge"
date: 2014-04-19 22:00
comments: true
categories: Git
---

<!-- more -->

关于Git Merge时的`--ff` 和 `--no-ff` 参数，ff代表的意思是`fast forward`，即直接快速前进。

`man git-merge`的解释:

	--ff
	   When the merge resolves as a fast-forward, only update the branch pointer, without creating a merge commit. This is the default behavior.

	--no-ff
	   Create a merge commit even when the merge resolves as a fast-forward. This is the default behaviour when merging an annotated (and possibly signed)
	   tag.

fast forward 和 no fast forward 的合并图:

![git branch merge](https://tankywoo-wb.b0.upaiyun.com/git-branch-merge.png)

<sup>(图片来至 [A successful Git branching model](http://nvie.com/posts/a-successful-git-branching-model/))</sup>

fast forward 快速前进的合并方式适用于分支B从分支A从checkout出来后，分支A没有commit，这样分支B被合并到分支A时，可以快速前进，这个也是git默认的合并方式。

如果分支B被checkout出来后，分支A也有修改，那么就没法快速前进合并，会额外建立一个merge commit，对分支A和分支B做一个合并操作。

使用 no fast forward 的好处就是时分支的结构性没有做改动，保持分支的结构，把分支B的多次开发最后做一个merge commit 合并到分支A上。

网上有一些探讨的帖子和文章，建议把`--no-ff`作为默认的方式，比如上面提到的 [A successful Git branching model](http://nvie.com/posts/a-successful-git-branching-model/)。

另外，StackOverflow上也有几篇很详细的讲解:

* [What is the difference between 'git merge' and 'git merge --no-ff'?](http://stackoverflow.com/questions/9069061/what-is-the-difference-between-git-merge-and-git-merge-no-ff)
* [Git fast forward VS no fast forward merge](http://stackoverflow.com/questions/6701292/git-fast-forward-vs-no-fast-forward-merge)
* [Why does git fast-forward merges by default?](http://stackoverflow.com/questions/2850369/why-does-git-fast-forward-merges-by-default)
* [When to use the '--no-ff' merge option in Git](http://stackoverflow.com/questions/18126297/when-to-use-the-no-ff-merge-option-in-git)
* [Fast-Forward Git Merge](http://ariya.ofilabs.com/2013/09/fast-forward-git-merge.html)

首先checkout一个分支，叫ff, 并切换过去:

	TankyWoo@Mac::test-git/ (master) » git co -b ff master
	Switched to a new branch 'ff'

新建一个文件c，做一个commit，再随便修改下，并又做一个commit。

接着切换回master分支，做 fast forward 合并:

	TankyWoo@Mac::test-git/ (ff) » git co master
	Switched to branch 'master'
	TankyWoo@Mac::test-git/ (master) » git merge ff
	Updating 2f1e828..8bffa7b
	Fast-forward
	 c | 1 +
	 1 file changed, 1 insertion(+)
	 create mode 100644 c

查看log:

	* 8bffa7b - (HEAD, ff) update c (10 seconds ago) <Tanky Woo>
	* 525481f - add c (18 seconds ago) <Tanky Woo>
	* 2f1e828 - (origin/test, origin/master, origin/HEAD, master) update test-git-submodule (2 days ago) <Tanky Woo>

如果做 no fast forward 合并:

	TankyWoo@Mac::test-git/ (master) » git merge -no-ff ff

查看log:

	*   a368dcc - (HEAD, master) Merge branch 'ff' (4 seconds ago) <Tanky Woo>
	|\
	| * 8bffa7b - (ff) update c (3 minutes ago) <Tanky Woo>
	| * 525481f - add c (3 minutes ago) <Tanky Woo>
	|/
	* 2f1e828 - (origin/test, origin/master, origin/HEAD) update test-git-submodule (2 days ago) <Tanky Woo>

再尝试做一个正常情况下不可 fast forward 的，先在ff分支里做两次commit，然后checkout回master分支，也做一个commit。

ff分支的log:

	* 693ad65 - (HEAD, ff) update c (12 seconds ago) <Tanky Woo>
	* a9ce393 - add c (24 seconds ago) <Tanky Woo>
	* 2f1e828 - (origin/test, origin/master, origin/HEAD, master) update test-git-submodule (2 days ago) <Tanky Woo>

master分支的log:

	* 503393f - (HEAD, master) add d (1 second ago) <Tanky Woo>
	* 2f1e828 - (origin/test, origin/master, origin/HEAD) update test-git-submodule (2 days ago) <Tanky Woo>

可以看到commit id为2f1e828 的提交是master和ff的公共原点，也就是ff是在这个commit上从master分支checkout出去的。

如果直接做`-ff-only`，可以看到报错提示:

	TankyWoo@Mac::test-git/ (master) » git merge --ff-only ff
	fatal: Not possible to fast-forward, aborting.

这个时候，要么做一次`--no-ff`提交合并，要么就[`rebase`](http://stackoverflow.com/questions/13106179/fatal-not-possible-to-fast-forward-aborting)，如:

	TankyWoo@Mac::test-git/ (master) » git rebase master

做完rebase后的log:

	* 3b2a4d9 - (HEAD, master) add d (77 seconds ago) <Tanky Woo>
	* 693ad65 - (ff) update c (15 minutes ago) <Tanky Woo>
	* a9ce393 - add c (15 minutes ago) <Tanky Woo>
	* 2f1e828 - (origin/test, origin/master, origin/HEAD) update test-git-submodule (2 days ago) <Tanky Woo>

