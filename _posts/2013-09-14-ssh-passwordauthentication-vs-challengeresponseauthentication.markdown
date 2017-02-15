---
layout: post
title: "SSH PasswordAuthentication vs ChallengeResponseAuthentication"
date: 2013-09-14 19:07
comments: true
categories: Linux
---

<!-- more -->

In the previous blog [Common Security of VPS](http://tech.wutianqi.com/blog/2013/09/14/common-security-of-vps/), there is a suggestion "SSH limit root login and password authentication.".

If set `PasswordAuthentication no`, we can still login in by password.

The reason is `ChallengeResponseAuthentication yes`.


The difference between `ChallengeResponseAuthentication` and `PasswordAuthentication`:

From [lzzy](http://superuser.com/a/374234):

> PasswordAuthentication controls support for the 'password' authentication scheme defined in RFC-4252 (section 8). ChallengeResponseAuthentication controls support for the 'keyboard-interactive' authentication scheme defined in RFC-4256. The 'keyboard-interactive' authentication scheme could, in theory, ask a user any number of multi-facited questions. In practice it often asks only for the user's password.
> 
> If you want to fully disable password-based authentication, set BOTH PasswordAuthentication and ChallengeResponseAuthentication to 'no'. If you're of the belt-and-suspenders mindset, consider setting UsePAM to 'no' as well.
> 
> Public/Private Key-based authentication (enabled by the PubkeyAuthentication setting) is a separate type of authentication that does not involve sending user passwords to the server, of course.
> 
> Some would argue that using ChallengeResponseAuthentication is more secure than PasswordAuthentication because it is more difficult to automate. They therefore recommend leaving PasswordAuthentication disabled while leaving ChallengeResponseAuthentication enabled. This configuration also encourages (but does not necessarily prevent) use of publickey authentication for any automated system logins. But, since SSH is a network-based protocol, the server has no way to guarantee that responses to ChallengeResponseAuthentication (a.k.a. 'keyboard-interactive') are actually being provided by a user sitting at a keyboard so long as the challenge(s) always and only consists of asking a user for her password.

From [Richard Silverman](http://fixunix.com/ssh/73410-how-does-challengeresponseauthentication-actually-works.html#post239656):

> It doesn't provide "additional security," per se. The term "ChallengeResponseAuthentication" is just an OpenSSH configuration keyword; it refers to the "keyboard-interactive" userauth method in the SSH protocol, defined here:
> 
> [http://www.snailbook.com/docs/keyboard-interactive.txt](http://www.snailbook.com/docs/keyboard-interactive.txt)
> 
> It allows for an arbitrary sequence of server prompts and typed user responses, to accomodate challenge-response protocols such as one-time password schemes (e.g. SecurID, OPIE, etc.).
> 
> In many default Unix configurations, it may be identical in effect to SSH "password" authentication, keyboard-interactive is set to use PAM, and the PAM profile for SSH is set to simply verify the Unix password.

From [robert.lanning at gmail](http://www.gossamer-threads.com/lists/openssh/users/48112#48112):

> "PasswordAuthentication" is a built-in method of using a password. 
> This is where the client gets the password from somewhere and passes it to the server, along with the user name. 
> 
> "ChallengeResponseAuthentication" is a method to tunnel the authentication process. The client opens the tty and gateways it to the server's authentication process/library. This enforces an interactive authentication scheme. 
> 
> Using ChallengeResponseAuthentication is more secure, as it does its best to not allow programmatic entering of the password. You must enter the password via a tty device. 
> 
> With PasswordAuthentication, you can: 
> $ echo $PASSWORD | ssh $HOST "cat /etc/passwd" 
> 
> With ChallengeResponseAuthentication you have to use a chat script 
> or expect. 
> 
> I would suggest forgoing passwords and just using keys. Unless your requirement is to use both. 

So, if we want to disable SSH's password login function, we should:

	PasswordAuthentication no
	ChallengeResponseAuthentication no

There are another good posts:

* [Five Minutes to a More Secure SSH](http://www.unixlore.net/articles/five-minutes-to-more-secure-ssh.html)
* [OpenSSH: requiring keys, but allow passwords from some locations](http://blather.michaelwlucas.com/archives/818)
