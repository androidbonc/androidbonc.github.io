---
layout: post
title: "Svn list ignored files and to ignore files"
date: 2014-02-14 16:25
comments: true
categories: Svn
---

<!-- more -->

List all property recursively on all files:

	svn proplist -v -R dir/

To ignore all files in the dir:

	svn propset svn:ignore directory

To ignore .jpg picture in the dir:

	svn propset svn:ignore "*.jpg"  dir/

To ignore file list from file:

	svn propset svn:ignore -F ignoring.txt dir/

To edit the ignore feature, this will use default editor to open a file, which list the been ignored files under the dir:

	svn propedit svn:ignore dir/


Reference:

* [How do I ignore files in subversion?](http://stackoverflow.com/questions/86049/how-do-i-ignore-files-in-subversion)
* [How do I list subversion repository's ignore settings](http://stackoverflow.com/questions/4509834/how-do-i-list-subversion-repositorys-ignore-settings)
* [How do I view all ignored patterns set with svn:ignore recursively in an svn repository?](http://stackoverflow.com/questions/1252270/how-do-i-view-all-ignored-patterns-set-with-svnignore-recursively-in-an-svn-rep)
* [Command Line svn:ignore a file](http://blog.bogojoker.com/2008/07/command-line-svnignore-a-file/)
