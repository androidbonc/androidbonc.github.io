---
layout: post
title: "Find with Xargs Problem"
date: 2014-10-27 10:00
---

最近发现一个定期清理目录的脚本失效了:

    find $mypath -name *.gz -mtime +10 | xargs -r rm -f

报错:

    rm: unrecognized option '--filter'
    Try `rm --help' for more information.
    rm: unrecognized option '--filter'
    Try `rm --help' for more information.

直接执行管道前面的find命令, 发现目录中有这么一个文件不知道是啥时候引入的(猜测是某次测试把命令当文件名写了):

    $mypath/.rsync-partial --filter *.201409*.gz

这个文件名带有空格(space).

`man xargs`有一段:

> Because Unix filenames can contain blanks and newlines, this default behaviour is often problematic; filenames containing blanks and/or newlines are incorrectly  processed by xargs.  In these situations it is better to use the -0 option, which prevents such problems.   When using this option you will need to ensure that the program which produces the input for xargs also uses a null character as a separator.  If that program is GNU find for example, the -print0 option does this for you.

因为find的输出中这个文件名有空格, 所以xargs执行会有问题, xargs有一个选项`-0/--null`用于处理这种情况:

>  --null/-0  
>     Input items are terminated by a null character instead of by whitespace, and the quotes and backslash are not special (every character is taken literally).  Disables the end of file string, which is treated like  any  other  argument.  Useful when input items might contain white space, quote marks, or backslashes.  The GNU find -print0 option produces input suitable for this mode.

xargs会以`null character`来处理input，而不是默认的`whitespace`空白符.

一般find和xargs配合的比较多, 所以find也有相应配合的一个选项`-print0`, 将输入项以`null chacter`作为行尾:

> -print0  
> True;  print  the full file name on the standard output, followed by a null character (instead of the newline character that -print uses).  This allows file names that contain newlines or other types of white space to be correctly interpreted by programs that process the find output.  This option corresponds to the -0 option of xargs.

改为这样就可以了:

    find $mypath -name *.gz -mtime +10 -print0 | xargs -0 -r rm -f


本地测试，目录下两个文件filea.log和fileb.log, 分析两者的EOL:

    $ find . -name 'file*.log'  | hexdump -C
    00000000  2e 2f 66 69 6c 65 61 2e  6c 6f 67 0a 2e 2f 66 69  |./filea.log../fi|
    00000010  6c 65 62 2e 6c 6f 67 0a                           |leb.log.|
    00000018

    $ find . -name 'file*.log' -print0 | hexdump -C
    00000000  2e 2f 66 69 6c 65 61 2e  6c 6f 67 00 2e 2f 66 69  |./filea.log../fi|
    00000010  6c 65 62 2e 6c 6f 67 00                           |leb.log.|
    00000018

可以看到前者默认是`-print`, EOL是`0a` (`\n`), 后者是`-print0`, EOL是`00` (`\0`)

参考:

* `man xargs`
* `man find`
