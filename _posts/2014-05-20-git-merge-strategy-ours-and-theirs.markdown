---
layout: post
title: "Git merge strategy - ours and theirs"
date: 2014-05-20 21:45
categories: Git
---

master分支下的文件afile:

	TankyWoo@Mac::git-test/ (master) » cat afile
	str1="test1"
	str2="test2"
	str3="test3"
	str4="test4"

切换到test分支，修改afile为:

	TankyWoo@Mac::git-test/ (test) » cat afile
	str3="test3"
	str3="test3"
	str4="test4"
	str5="test5"

然后再切换回master分支并修改afile为:

	TankyWoo@Mac::git-test/ (master) » more afile
	str1="test1"
	str2="test2"
	str3="test3"
	str4="test4"
	str5="test6"

使用分支合并策略`ours`:

	TankyWoo@Mac::git-test/ (master) » git merge -s ours test
	Merge made by the 'ours' strategy.

	TankyWoo@Mac::git-test/ (master) » more afile
	str1="test1"
	str2="test2"
	str3="test3"
	str4="test4"
	str5="test6"

文件内容并没有修改

只是在合并时新建了一个合并commit:

	*   550406a - (HEAD, master) Merge branch 'test' (35 seconds ago) <Tanky Woo>
	|\
	| * e23c4a0 - (test) update afile (6 minutes ago) <Tanky Woo>
	|/
	* 1769376 - add afile (7 minutes ago) <Tanky Woo>

reset回到合并前，再尝试切换到test分支，使用合并的默认策略`recursive`的选项`theirs`:

	TankyWoo@Mac::git-test/ (test) » git merge -X theirs master
	Auto-merging afile
	Merge made by the 'recursive' strategy.
	 afile | 2 +-
	 1 file changed, 1 insertion(+), 1 deletion(-)

	TankyWoo@Mac::git-test/ (test) » cat afile
	str3="test3"
	str3="test3"
	str4="test4"
	str5="test6"

再切换到master分支，使用并的默认策略`recursive`的选项`theirs`:

	TankyWoo@Mac::git-test/ (master) » git merge -X theirs test
	Auto-merging afile
	Merge made by the 'recursive' strategy.
	 afile | 5 ++---
	 1 file changed, 2 insertions(+), 3 deletions(-)

	TankyWoo@Mac::git-test/ (master) » more afile
	str3="test3"
	str3="test3"
	str4="test4"
	str5="test5"

关于 `git merge -s recursive -X ours` 和 `git merge -s ours`的区别:

再修改master分支下的afile:

	TankyWoo@Mac::git-test/ (master) » more afile
	str1="test1"
	str2="test2"
	str3="test3"
	str4="test4"
	str5="test6"

使用 `-s ours`来合并:

	TankyWoo@Mac::git-test/ (master) » git merge -s ours test
	Merge made by the 'ours' strategy.

	TankyWoo@Mac::git-test/ (master) » more afile
	str1="test1"
	str2="test2"
	str3="test3"
	str4="test4"
	str5="test6"

并没有任何改动，只是简单的把test分支合并过来了:

	*   7e63b02 - (HEAD, master) Merge branch 'test' (28 seconds ago) <Tanky Woo>
	|\
	| * e23c4a0 - (test) update afile (80 minutes ago) <Tanky Woo>
	* | 88cdead - update afile in master (3 minutes ago) <Tanky Woo>
	|/
	* 1769376 - add afile (81 minutes ago) <Tanky Woo>

再尝试 `-X ours`(即 `-s recursive -X ours`):

	TankyWoo@Mac::git-test/ (master) » git merge -X ours test
	Auto-merging afile
	Merge made by the 'recursive' strategy.
	 afile | 3 +--
	 1 file changed, 1 insertion(+), 2 deletions(-)

	TankyWoo@Mac::git-test/ (master) » more afile
	str3="test3"
	str3="test3"
	str4="test4"
	str5="test6"

可以看到作了合并，但是 **冲突** 的地方使用的是自己的。

log看起来都是一样的:

	*   58b7043 - (HEAD, master) Merge branch 'test' (13 seconds ago) <Tanky Woo>
	|\
	| * e23c4a0 - (test) update afile (80 minutes ago) <Tanky Woo>
	* | 88cdead - update afile in master (4 minutes ago) <Tanky Woo>
	|/
	* 1769376 - add afile (81 minutes ago) <Tanky Woo>

如果没有指定策略，单纯的合并则:

	TankyWoo@Mac::git-test/ (master) » git merge --no-ff test
	Auto-merging afile
	CONFLICT (content): Merge conflict in afile
	Automatic merge failed; fix conflicts and then commit the result.

	TankyWoo@Mac::git-test/ (master*) » gst
	# On branch master
	# You have unmerged paths.
	#   (fix conflicts and run "git commit")
	#
	# Unmerged paths:
	#   (use "git add <file>..." to mark resolution)
	#
	#       both modified:      afile
	#
	no changes added to commit (use "git add" and/or "git commit -a")

	TankyWoo@Mac::git-test/ (master*) » git diff afile
	diff --cc afile
	index 98b19b3,ba5ee86..0000000
	--- a/afile
	+++ b/afile
	@@@ -1,5 -1,4 +1,8 @@@
	- str1="test1"
	- str2="test2"
	+ str3="test3"
	  str3="test3"
	  str4="test4"
	++<<<<<<< HEAD
	 +str5="test6"
	++=======
	+ str5="test5"
	++>>>>>>> test

Git merge 策略的总结:

0. 使用 `-s` 指定策略，使用 `-X` 指定策略的选项
1. 默认策略是`recursive`
2. 策略有 `ours`，但是没有`theirs` (Git老版本好像有)
3. 策略`ours`直接 **忽略** 合并分支的任何内容，只做简单的合并，保留分支改动的存在
4. 默认策略`recursive`有选项`ours` 和 `theirs`
5. `-s recursive -X ours` 和 `-s ours` 不同，后者如第3点提到直接忽略内容，但是前者会做合并，遇到冲突时以自己的改动为主
6. `-s recursive -X theirs`的对立面是 `-s recursive -X ours`
