---
layout: post
title: "Simiki基于Github Pages配合Travis CI做持续集成"
date: 2016-02-19 21:00
---

P.S. 2016年第一篇博客, 15年就没写总结和计划来安慰自己了~~

回归正题

关于这个方案，最早看过是关于Jekyll的，那时没想太多，扫一眼就忽略了。

后来 [@zvving](https://github.com/zvving) 年前在 [issue上提交了simiki的解决方案](https://github.com/tankywoo/simiki/issues/23#issuecomment-179675088)，也提出了一些问题。于是我最近两天实践了一次，也hack了一些坑。

具体的步骤可以参考以下:

* [@zvving Simiki + Travis-ci + Github-Pages 搭建自动部署的个人 Wiki](http://www.jianshu.com/p/d56008e6c2e1)
* [@xuanwo 使用Travis CI自动部署Hexo](https://xuanwo.org/2015/02/07/Travis-CI-Hexo-Autodeploy/)
* [用 Travis CI 自動部署網站到 GitHub](https://zespia.tw/blog/2015/01/21/continuous-deployment-to-github-with-travis/)
* issue上讨论的内容

*这里不讲一步步该如何做，主要对其中的一些步骤和问题，给出讲解说明以及解决方案。*


除了[Simiki](http://simiki.org/)本身，还需要的额外服务:

* [Github Pages](https://pages.github.com/)  这个之前已经写过文档 [Simiki Docs - Deploy](http://simiki.org/zh-docs/deploy.html)
* [Travis CI](https://travis-ci.org/)  做持续集成，配合Github，Simiki项目开发一直在用

大致的流程就是:

* 推送源分支到Github
* Travis CI收到推送，执行相应的build服务
* Travis CI生成相应的output，反推回到Github的gh-pages分支

首先在Travis CI上开启对自己项目的持续集成。

因为这个涉及到推送回Github的写权限问题，所以生成一对单独的公私钥，专门给这个提供使用(这里我私钥就没有加密码了，因为travis会进一步加密):

	ssh-keygen -C "wiki@tankywoo.com" -t rsa -b 2048 -f ~/.ssh/wiki

将公钥内容贴到Github上项目的 「Settings -> Deploy keys -> Add deploy key」

其次安装「travis」的本地工具，登录:

	gem install travis
	travis login --auto

会生成一个token文件存放在`~/.travis/config.yml` (部分字符串用`*`代替):

	$ cat ~/.travis/config.yml
	---
	last_check:
	  etag: W/"**********"
	  version: 1.8.2
	  at: 1455634393
	checked_completion: true
	completion_version: 1.8.2
	endpoints:
	  https://api.travis-ci.org/:
		access_token: *******

进入相应的Github项目目录，加密私钥：

	$ travis encrypt-file ~/.ssh/wiki --add
	encrypting /Users/TankyWoo/.ssh/wiki for tankywoo/wiki.tankywoo.com
	storing result as wiki.enc
	storing secure env variables for decryption

	Make sure to add wiki.enc to the git repository.
	Make sure not to add /Users/TankyWoo/.ssh/wiki to the git repository.
	Commit all changes to your .travis.yml.

这个操作主要做了几件事情:

1. 加密ssh私钥, 生成一个wiki.enc。这个文件需要放到项目里，上面的输出已经提示了，千万别把原始的私钥放进去了~~
2. 相应的解密k/v值以环境变量方式存在Travis CI上, 见Travis CI上项目的「More options -> Settings -> Environment Variables」
3. 将解密命令自动写入到本地项目的`.travis.yml`里 (注意每个人的环境变量名不一样, 不需要去复制我的, travis加密时会自动写入)

		before_install:
		- openssl aes-256-cbc -K $encrypted_f9a8a4d68f34_key -iv $encrypted_f9a8a4d68f34_iv
		  -in wiki.enc -out ~\/.ssh/wiki -d

然后本地项目新增文件`ssh_config`:

	Host github.com
		User git
		StrictHostKeyChecking no
		IdentityFile ~/.ssh/id_rsa
		IdentitiesOnly yes

这里需要指定用户是git, 走的「ssh/git」协议, 而不是「http/https」协议。

到这里，我先把配置ok的完整「.travis.yml」贴出来:

	language: python
	python:
	  - '2.7'
	install:
	  - pip install fabric
	  - pip install ghp-import
	  - pip install simiki
	branches:
	  only:
		- master
		- gh-pages
	before_install:
	  - openssl aes-256-cbc -K $encrypted_f9a8a4d68f34_key -iv $encrypted_f9a8a4d68f34_iv
		-in wiki.enc -out ~/.ssh/id_rsa -d
	  - chmod 600 ~/.ssh/id_rsa  # ssh私钥权限
	  - cp ssh_config ~/.ssh/config  # 配置ssh client
	  - git config --global user.name "Tanky Woo"  # 推送回gh-pages需要的基本配置
	  - git config --global user.email wtq1990@gmail.com
	  - git remote set-url origin git@github.com:tankywoo/wiki.tankywoo.com.git  # hack 1
	  - git fetch origin gh-pages:refs/remotes/origin/gh-pages  # hack 2
	  - git branch gh-pages origin/gh-pages
	script:
	  - simiki g
	  - fab deploy

这里面有两处hack的地方(注释处):

hack 1, 因为Travis CI克隆是用的「http/https」协议(需要输入username/password)，所以我在push gh-pages时没法使用公私钥认证，于是克隆下来后我就改了origin的地址为「ssh/git」。

hack 2, 作了一个单独拉出`gh-pages`分支的操作。

看Travis CI的build log, 克隆项目指定了`--depth`，这个会只拉出当前分支:

	git clone --depth=50 --branch=master https://github.com/tankywoo/wiki.tankywoo.com.git tankywoo/wiki.tankywoo.com

其实最简单的就是配置选项，再加上`--no-single-branch`选项就可以了；但是，Travis CI对于克隆命令，除了可以配置`depth`外，不支持其它选项，所以我只能作了这个hack，单独拉出gh-pages分支，否则会报错:

	$ fab deploy
	[localhost] local: which ghp-import > /dev/null 2>&1; echo $?
	[localhost] local: ghp-import -p -m "Update output documentation" -r origin -b gh-pages output
	Warning: Permanently added the RSA host key for IP address '192.30.252.131' to the list of known hosts.
	To git@github.com:tankywoo/wiki.tankywoo.com.git
	 ! [rejected]        gh-pages -> gh-pages (fetch first)
	error: failed to push some refs to 'git@github.com:tankywoo/wiki.tankywoo.com.git'
	hint: Updates were rejected because the remote contains work that you do
	hint: not have locally. This is usually caused by another repository pushing
	hint: to the same ref. You may want to first integrate the remote changes
	hint: (e.g., 'git pull ...') before pushing again.
	hint: See the 'Note about fast-forwards' in 'git push --help' for details.
	Traceback (most recent call last):
	  File "/home/travis/virtualenv/python2.7.9/bin/ghp-import", line 198, in <module>
		main()
	  File "/home/travis/virtualenv/python2.7.9/bin/ghp-import", line 194, in main
		sp.check_call(['git', 'push', opts.remote, opts.branch])
	  File "/opt/python/2.7.9/lib/python2.7/subprocess.py", line 540, in check_call
		raise CalledProcessError(retcode, cmd)
	subprocess.CalledProcessError: Command '['git', 'push', 'origin', 'gh-pages']' returned non-zero exit status 1
	Fatal error: local() encountered an error (return code 1) while executing 'ghp-import -p -m "Update output documentation" -r origin -b gh-pages output'
	Aborting.

因为克隆时origin没有带上gh-pages分支，所以这样相当于新建了gh-pages分支，并会覆盖远端的，这时需要加上`-f/--force`强制push，但是这样显然也并不是一个好的方案。

另外，在配置ssh client配置时，也可以不用这个「ssh-config」配置文件，改用`ssh_agent`(这玩意相当于win下常用的PuTTY工具集的Pageant，我的[dotfiles](https://github.com/tankywoo/dotfiles/blob/master/.zshrc)里也有这个的配置，有兴趣的可以看看):

	before_install:
	  - openssl aes-256-cbc -K $encrypted_f9a8a4d68f34_key -iv $encrypted_f9a8a4d68f34_iv
		-in wiki.enc -out ~/.ssh/id_rsa -d
	  - chmod 600 ~/.ssh/id_rsa
	  - eval $(ssh-agent)  # 这两行使用ssh-agent
	  - ssh-add ~/.ssh/id_rsa
	  - git config --global user.name "Tanky Woo"
	  - ...

当然，网上很多方案把这两种都加进去了，也无所谓~~~

这个说白了就是一点点的测试，我前后也测试了20次，才测试OK。

后续，我会再基于此篇基础上，整理一份文档放到 [simiki.org](http://simiki.org) 上。

最后感谢 [@zvving](https://github.com/zvving) 和 [@Xuanwo](https://github.com/Xuanwo) 对这个方案的贡献.
