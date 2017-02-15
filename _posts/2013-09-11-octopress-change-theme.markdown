---
layout: post
title: "Octopress change theme"
date: 2013-09-11 21:17
comments: true
categories: Octopress
---

<!-- more -->

Google `octopress themes`, I found two websites list many beautiful themes.

* [Octopress Themes](http://opthemes.com/)
* [Top 10+ Octopress Themes](http://www.evolument.com/blog/2013/03/02/top-10-plus-octopress-themes/)


I choose a theme named [DarkStripes](https://github.com/amelandri/darkstripes).


The installation is very easy, use this theme as a example(from its README):

	$ cd octopress
	$ git clone git://github.com/amelandri/darkstripes.git .themes/darkstripes
	$ rake install['darkstripes']
	$ rake generate

**NOTE** : When I installed this theme, it overrited my `about.html` in `source/_includes/custom/asides/about.html` .

The offical docs also provide a 3rd party themes list:

* [3rd Party Octopress Themes](https://github.com/imathis/octopress/wiki/3rd-Party-Octopress-Themes)
