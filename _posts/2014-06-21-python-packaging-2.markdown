---
layout: post
title: "Python Packaging (2)"
date: 2014-06-21 15:30
categories: Python
---

<!-- more -->

上一篇 [Python Packaging]({{ site.baseurl }}{% post_url 2013-12-04-python-packaging %})

关于`python setup.py`的一些记录。

	(package)TankyWoo@Mac::simiki/ (dev*) » python setup.py --help
	Common commands: (see '--help-commands' for more)

	  setup.py build      will build the package underneath 'build/'
	  setup.py install    will install the package

	Global options:
	  --verbose (-v)      run verbosely (default)
	  --quiet (-q)        run quietly (turns verbosity off)
	  --dry-run (-n)      don't actually do anything
	  --help (-h)         show detailed help message
	...

使用`--help`可以看到列出两个常用的子命令`build`和`install`，并提示了更多的命令使用`python setup.py --help-commands`查看。其它显示的都是一些参数选项。

使用`python setup.py <cmd> --help` 还可以看到相应子命令的参数选项。


	(package)TankyWoo@Mac::simiki/ (dev*) » python setup.py --help-commands
	Standard commands:
	  build             build everything needed to install
	  build_py          "build" pure Python modules (copy to build directory)
	  build_ext         build C/C++ extensions (compile/link to build directory)
	  build_clib        build C/C++ libraries used by Python extensions
	  build_scripts     "build" scripts (copy and fixup #! line)
	  clean             clean up temporary files from 'build' command
	  install           install everything from build directory
	  install_lib       install all Python modules (extensions and pure Python)
	  install_headers   install C/C++ header files
	  install_scripts   install scripts (Python or otherwise)
	  install_data      install data files
	  sdist             create a source distribution (tarball, zip file, etc.)
	  register          register the distribution with the Python package index
	  bdist             create a built (binary) distribution
	  bdist_dumb        create a "dumb" built distribution
	  bdist_rpm         create an RPM distribution
	  bdist_wininst     create an executable installer for MS Windows
	  upload            upload binary package to PyPI
	  check             perform some checks on the package

	Extra commands:
	  rotate            delete older distributions, keeping N newest files
	  develop           install package in 'development mode'
	  setopt            set an option in setup.cfg or another config file
	  saveopts          save supplied options to setup.cfg or other config file
	  egg_info          create a distribution's .egg-info directory
	  upload_docs       Upload documentation to PyPI
	  alias             define a shortcut to invoke one or more commands
	  easy_install      Find/get/install Python packages
	  bdist_egg         create an "egg" distribution
	  install_egg_info  Install an .egg-info directory for the package
	  test              run unit tests after in-place build

	usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
	   or: setup.py --help [cmd1 cmd2 ...]
	   or: setup.py --help-commands
	   or: setup.py cmd --help

本地测试的`setup.py`是基于`setuptools`的[simiki](https://github.com/tankywoo/simiki).

这些命令在执行时，都会显示详细的信息，可以看到具体都执行了哪些操作和命令，有些命令会携带一起执行其它命令。

### `python setup.py alias`

设置一些别名，默认写入当前项目的`setup.cfg`里，如执行:

	python setup.py alias release sdist bdist_egg register upload

查看setup.cfg:

	[aliases]
	release = sdist bdist_egg register upload

也可以手动直接写文件

### `python setup.py build`

会建立`build`目录和`<PACKAGE_NAME>.egg_info` 目录，其中build目录结构是`build/lib/<PACKAGE_NAME>`

### `python setup.py clean`

会清理上面build的生成的临时文件

### `python setup.py egg_info`

生成`simiki.egg-info`目录，包含了这个包的一些在setup.py/cfg中的配置信息

这个会在`sdist`, `bdist_egg` 等多个命令中都会使用到，具体可以看执行的输出日志。

### `python setup.py sdist`

默认是对Python包进行压缩打包，生成`.tar.gz`文件，可以被`pip`直接使用。

查看执行日志可以看到是执行了`sdist`和`egg_info`命令。

生成`dist`和`simiki.egg-info`目录，`dist`下就是对Python包进行打包后的tar包`simiki-1.0.3.tar.gz`

解压后里面包含了simiki包、simiki.egg-info、setup.py、setup.cfg和MANIFEST.in包含的文件等。

此命令后面还可以接一些参数，主要就是`--formats`指定打包格式，默认就是`tar.gz`

	Options for 'sdist' command:
	  --formats         formats for source distribution (comma-separated list)
	  --keep-temp (-k)  keep the distribution tree around after creating archive
						file(s)
	  --dist-dir (-d)   directory to put the source distribution archive(s) in
						[default: dist]
	  --help-formats    list available distribution formats

	(package)TankyWoo@Mac::simiki/ (dev) » python setup.py sdist --help-formats
	List of available source distribution formats:
	  --formats=bztar  bzip2'ed tar-file
	  --formats=gztar  gzip'ed tar-file
	  --formats=tar    uncompressed tar file
	  --formats=zip    ZIP file
	  --formats=ztar   compressed tar file

### `python setup.py bdist_egg`

同`sdist`类似，生成同样的目录，只不过dist目录下是一个egg文件，比如这里是: simiki-1.0.3-py2.7.egg

`easy_install`可以使用egg文件快速安装包，就像pip使用tar.gz一样。

egg文件本质上就是一个zip包:

	(package)TankyWoo@Mac::simiki/ (dev*) » file dist/simiki-1.0.3-py2.7.egg
	dist/simiki-1.0.3-py2.7.egg: Zip archive data, at least v2.0 to extract

使用`unzip -l`可以预览里面的文件列表，和dist的tar包内容基本一样:

	(package)TankyWoo@Mac::simiki/ (dev*) » unzip -l dist/simiki-1.0.3-py2.7.egg
	Archive:  dist/simiki-1.0.3-py2.7.egg
	  Length     Date   Time    Name
	 --------    ----   ----    ----
			1  06-21-14 21:55   EGG-INFO/dependency_links.txt
		   44  06-21-14 21:55   EGG-INFO/entry_points.txt
			1  06-21-14 21:55   EGG-INFO/not-zip-safe
		  676  06-21-14 21:55   EGG-INFO/PKG-INFO
		   70  06-21-14 21:55   EGG-INFO/requires.txt
		  701  06-21-14 21:55   EGG-INFO/SOURCES.txt
			7  06-21-14 21:55   EGG-INFO/top_level.txt
		   69  06-21-14 13:55   simiki/__init__.py
		  171  06-21-14 21:55   simiki/__init__.pyc
		 7277  06-21-14 13:55   simiki/cli.py
		 8430  06-21-14 21:55   simiki/cli.pyc
		 2244  06-21-14 15:28   simiki/configs.py
		 2486  06-21-14 21:55   simiki/configs.pyc
		 8863  06-21-14 15:28   simiki/generators.py
		 ......
	 --------                   -------
		83963                   33 files


所以一般打包时同时使用`sdist`和`bdist_egg`支持`pip`和`easy_install`两个。

egg更详细介绍见[What is a Python egg?](http://stackoverflow.com/questions/2051192/what-is-a-python-egg)

### `python setup.py install`

通过输出日志看到，执行install时会先执行`bdist_egg`生成egg文件

然后通过这个egg文件在Python系统路径下安装和执行一些其它操作，最后安装依赖的包。

### `python setup.py bdist`

这个暂时还有点不是很明白 TODO

	(package)TankyWoo@Mac::simiki/ (dev*) » tree -L 2 build dist simiki.egg-info
	build
	├── bdist.macosx-10.9-intel
	└── lib
		└── simiki
	dist
	└── simiki-1.0.3.macosx-10.9-intel.tar.gz
	simiki.egg-info

`dist/Users/TankyWoo`是`dist/simiki-1.0.3.macosx-10.9-intel.tar.gz`解压后，针对我用了virtualenvwrapper，是直接放到`./Users/TankyWoo/.virtualenvs/package/`下，所以它这个打包应该是指定了绝对路径打包的。

在[distutils](https://docs.python.org/2/distutils/builtdist.html)文档中看到了一段解释:

> the Distutils builds my module distribution (the Distutils itself in this case), does a “fake” installation (also in the build directory), and creates the default type of built distribution for my platform. The default format for built distributions is a “dumb” tar file on Unix, and a simple executable installer on Windows. (That tar file is considered “dumb” because it has to be unpacked in a specific location to work.)

> Thus, the above command on a Unix system creates Distutils-1.0.plat.tar.gz; unpacking this tarball from the right place installs the Distutils just as though you had downloaded the source distribution and run python setup.py install. (The “right place” is either the root of the filesystem or Python’s prefix directory, depending on the options given to the `bdist_dumb` command; the default is to make dumb distributions relative to prefix.)

> Obviously, for pure Python distributions, this isn’t any simpler than just running python setup.py install—but for non-pure distributions, which include extensions that would need to be compiled, it can mean the difference between someone being able to use your extensions or not. And creating “smart” built distributions, such as an RPM package or an executable installer for Windows, is far more convenient for users even if your distribution doesn’t include any extensions.

感觉这个和打包的平台和环境关系很深，比如我这里它解压后的路径，必须要和我一样才行。

应该就如上面所说: does a "fake" installation.

### `python setup.py register`

将软件包注册到[PyPI](https://pypi.python.org/pypi)，主要是通过`<PACKAGE_NAME>.egg-info`目录里的信息。所以在执行register时会同时执行`egg_info`命令。

当执行时，默认情况下，如果本地没有`~/.pypirc`文件，则会讯问是否登录已有PyPI账户或注册一个，如果登录或注册后，会讯问是否将帐号密码保存到本地的`~/.pypirc`文件中，保存后，下次提交或注册其它包就会从这个文件读取账户信息并使用。

另外，如果upload的软件包信息（比如description, classifier）等需要更新，只需要本地更新后运行`egg_info`生成xxx.egg-info文件，确认里面的`PKG-INFO`文件内容是对的，就可以执行register命令更新。

### `python setup.py develop`

这个功能超赞！我以前不知道这个命令，然后是手动把此目录作了软链接到`python2.7/site-packages/`下。

看执行日志可以看到实际是在上面的目录中生成了一个`simiki.egg-link`文件，记录了项目实际的目录。

### `python setup.py upload`

将相关的项目二进制包上传到PyPI提供下载。

来至[setuptools](https://pythonhosted.org/setuptools/setuptools.html)的说明:

> It’s usually a good idea to include the register command at the start of the command line, so that any registration problems can be found and fixed before building and uploading the distributions, e.g.:

	setup.py register sdist bdist_egg upload

所以可以设置为如上面alias命令的配置。

## 参考 ##

* [setuptools](https://pythonhosted.org/setuptools/index.html)
* [distutils](https://docs.python.org/2/distutils/index.html)

