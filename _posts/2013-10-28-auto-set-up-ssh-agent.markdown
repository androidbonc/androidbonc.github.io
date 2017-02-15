---
layout: post
title: "Auto Set Up ssh-agent"
date: 2013-10-28 15:33
comments: true
categories: Linux
---

<!-- more -->

Add auto set up ssh-agent in my [.zshrc](https://github.com/tankywoo/dotfiles/blob/master/.zshrc)

```bash
# Set up ssh-agent
SSH_ENV="$HOME/.ssh/environment"

function start_agent {
	echo "Initializing new SSH agent..."
	/usr/bin/ssh-agent | sed 's/^echo/#echo/' > "${SSH_ENV}"
	echo succeeded
	chmod 600 "${SSH_ENV}"
	. "${SSH_ENV}" > /dev/null
	/usr/bin/ssh-add;
}

# Source SSH settings, if applicable
if [ -f "${SSH_ENV}" ]; then
	. "${SSH_ENV}" > /dev/null
	#ps ${SSH_AGENT_PID} doesn't work under cywgin
	ps -ef | grep ${SSH_AGENT_PID} | grep ssh-agent$ > /dev/null || {
		start_agent;
	}
else
	start_agent;
fi
```

From :

* [Gist - .bashrc_ssh](https://gist.github.com/bluegraybox/1998129)
* [Set up SSH for Git - Step 5](https://confluence.atlassian.com/display/BITBUCKET/Set+up+SSH+for+Git)
