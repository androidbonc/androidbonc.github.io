---
layout: post
title: "Gentoo Dependency Graph Slot Conflicts"
date: 2014-08-26 16:00
---

Gentoo安装`pylint`时遇到一个`slot conflict`:

	tankywoo@gentoo-local::~/ » sudo emerge -av pylint

	These are the packages that would be merged, in order:

	Calculating dependencies... done!
	[ebuild     U  ] dev-python/setuptools-2.2 [0.6.30-r1] PYTHON_TARGETS="python2_7 python3_3%* (-pypy) -python3_2* (-python3_4) 
														(-python2_5%) (-python2_6%) (-python3_1%)" 769 kB
	[ebuild  N     ] dev-python/logilab-common-0.61.0  USE="-doc {-test}" PYTHON_TARGETS="python2_7 python3_3 (-pypy) -python3_2 (-python3_4)" 195 kB
	[ebuild  N     ] dev-python/astng-0.21.1  USE="{-test}" 98 kB
	[ebuild  N     ] dev-python/pylint-0.23.0  USE="-examples" 196 kB

	Total: 4 packages (1 upgrade, 3 new), Size of downloads: 1,256 kB

	!!! Multiple package instances within a single package slot have been pulled
	!!! into the dependency graph, resulting in a slot conflict:

	dev-python/setuptools:0

	  (**dev-python/setuptools-2.2::gentoo**, ebuild scheduled for merge) pulled in by
		dev-python/setuptools[python_targets_python2_7(-)?,python_targets_python3_2(-)?,python_targets_python3_3(-)?,python_targets_python3_4(-)?,
							python_targets_pypy(-)?,-python_single_target_python2_7(-),python_single_target_python3_2(-),
							-python_single_target_python3_3(-),-python_single_target_python3_4(-),python_single_target_pypy(-)] 
							required by (**dev-python/logilab-common-0.61.0::gentoo**, ebuild scheduled for merge)

	  (**dev-python/setuptools-0.6.30-r1::gentoo**, installed) pulled in by
		dev-python/setuptools[python_targets_python2_7(-)?,python_targets_python3_2(-)?,python_targets_python3_3(-)?,
							-python_single_target_python2_7(-),-python_single_target_python3_2(-),-python_single_target_python3_3(-)] 
							required by (**dev-python/pip-1.3.1::gentoo**, installed)
		dev-python/setuptools[python_targets_python2_7(-)?,python_targets_python3_2(-)?,python_targets_python3_3(-)?,python_targets_pypy(-)?,
							-python_single_target_python2_7(-),-python_single_target_python3_2(-),-python_single_target_python3_3(-),-python_single_target_pypy(-)] 
							required by (**dev-python/pygments-1.5-r1::gentoo**, installed)

	It may be possible to solve this problem by using package.mask to
	prevent one of those packages from being selected. However, it is also
	possible that conflicting dependencies exist such that they are
	impossible to satisfy simultaneously.  If such a conflict exists in
	the dependencies of two different packages, then those packages can
	not be installed simultaneously. You may want to try a larger value of
	the --backtrack option, such as --backtrack=30, in order to see if
	that will solve this conflict automatically.

根据提示，本地的`pip-1.3.1`和`pygments-1.5-r1`依赖老版本的`setuptools-0.6.30-r1`，而`pylint`依赖新版本的`setuptools-2.2`，所以就造成了`slot conflict`。

参考[Gentoo Wiki](http://wiki.gentoo.org/wiki/Troubleshooting#Dependency_Graph_Slot_Conflicts) 对这里的说明，其实只需要手动指定新版本`setuptools-2.2`升级时，同时执行依赖老版本的`pip`和`pygments`(**不用指定版本号**)，这样就会将`pip`和`pygments`也升级到合适的高版本中.

	tankywoo@gentoo-local::~/ » sudo emerge -avu '=dev-python/setuptools-2.2' dev-python/pip dev-python/pygments

	These are the packages that would be merged, in order:

	Calculating dependencies... done!
	[ebuild     U  ] dev-python/setuptools-2.2 [0.6.30-r1] PYTHON_TARGETS="python2_7 python3_3%* (-pypy) -python3_2* (-python3_4) (-python2_5%) (-python2_6%) (-python3_1%)" 769 kB
	[ebuild     U  ] dev-python/pip-1.4.1 [1.3.1] USE="zsh-completion" PYTHON_TARGETS="python2_7 python3_3* (-pypy) -python3_2* (-python2_6%)" 435 kB
	[ebuild     U  ] dev-python/pygments-1.6 [1.5-r1] USE="-doc {-test}" PYTHON_TARGETS="python2_7 python3_3* (-pypy) -python3_2* (-pypy1_9%) (-pypy2_0%) (-python2_5%) (-python2_6%) (-python3_1%)" 1,390 kB

	Total: 3 packages (3 upgrades), Size of downloads: 2,593 kB

	Would you like to merge these packages? [Yes/No]

升级好`setuptools`后再安装`pylint`就可以了.
