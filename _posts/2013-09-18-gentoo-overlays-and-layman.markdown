---
layout: post
title: "Gentoo Overlays and layman"
date: 2013-09-18 22:24
comments: true
categories: Gentoo
---

<!-- more -->

## About Overlays ##

[Gentoo Overlays](http://overlays.gentoo.org/)

### What Are Overlays? ###

> "Overlays" are package trees for Portage. They contain additional ebuilds for Gentoo. They are maintained by Gentoo developers and projects but distributed separately from the main Portage tree.

From [Gentoo Overlays: Users' Guide](http://www.gentoo.org/proj/en/overlays/userguide.xml)


### Why call it Overlays? ###

> Within Gentoo Linux, users already have one "main" package repository, called the Portage tree. This main repository contains all the software packages (called ebuilds) maintained by Gentoo developers. But users can add additional repositories to the tree that are "layed over" the main tree - hence the name, overlays.

From [Gentoo Wiki: Overlay](http://wiki.gentoo.org/wiki/Overlay)

## Use layman ##

	# Install layman
	emerge -av layman
	#(for layman 1.3 and later)
	# Init config
	echo PORTDIR_OVERLAY=\"\" > /var/lib/layman/make.conf
	echo "source /var/lib/layman/make.conf" >> /etc/portage/make.conf
	# List remote overlays
	layman -L
	# Add a overlay
	layman -a <overlay-name>
	# Update the specified overlay
	layman -s <overlay-name>

## gpo.zugaina.org ##

[http://gpo.zugaina.org/](http://gpo.zugaina.org/) is a website to **Search Portages & Overlays**.

Example:

I want to install [git-flow](https://github.com/nvie/gitflow), there is no ebuilds in the offical portage.

So I search it in this website. and find the page [http://gpo.zugaina.org/dev-vcs/gitflow](http://gpo.zugaina.org/dev-vcs/gitflow) is what I need.

There are found items in the page, from different overlay, but the ebuild file is the same, so any one is ok.

The `Overlay` on the right is the overlay name, I choose the overlay `flora`, and add it:

	layman -a flora
	layman -s flora

Now I `emerge -s gitflow` and can install it.

## References ##
* [Gentoo Overlays: Users' Guide](http://www.gentoo.org/proj/en/overlays/userguide.xml)
* [Gentoo Wiki:Overlay](http://wiki.gentoo.org/wiki/Overlay)
* [Diverting from the Official Tree](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=3&chap=5)
* [Using and creating Gentoo Linux repositories using Layman](http://astrofloyd.wordpress.com/2012/12/16/using-and-creating-gentoo-linux-repositories-using-layman/)
* [Gentoo Notes 03 - Programs](http://delta4d.github.io/blog/2013/04/01/gentoo-notes-03/) (zh)
