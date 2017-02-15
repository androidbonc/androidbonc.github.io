---
layout: post
title: "关于最近写的小玩具tfcs"
date: 2015-10-24 10:00
---

说是最近写的, 其实就是最近几天晚上抽了点时间写的, 没有什么技术含量, 也没有什么工作量...

平时的工作中, 会时不时搜到一些不错的代码片段(code snippet). 也没有保存代码片段的习惯, 就是偶尔给保存在Gist上.

最近看到两个不错的片段, 寻思着该收集一下了. 以目前我所了解的来看, Gist应该是最好用的.

但是Gist只有一个贴代码的地方, 和一个简单的描述栏.

> 我想的是:
> 
> * 可以做一些category/tag, 方便分类
> * 可以让我有一个更详细的说明的地方, 支持标记语言, 如md/rst
> * 以后我可以很方便的迁移到其它地方使用, 或者导出

于是我又翻看了自己曾经在知乎的一篇回答[哪些程序或服务可以方便地保存常用代码片段？](http://www.zhihu.com/question/21003319/answer/16931276).

网上关于这个的讨论不多, 大部分还是推荐Gist, 我的这篇回答应该是包括了圈里比较常用的几个web code snippet网站.

但是这些功能上都大同小异, 都是在一些细节上有不同的特色, 无法满足我的需求.

至于MacOs App, 网上倒是可以搜出十来个, 很多人也推荐的是[Dash](https://kapeli.com/dash)自带的code snippet功能, 和Gist相比多了一个Tag功能.

而Vim的插件, 我印象中也是有这类插件的, 可以配置快捷键快速调出snippet, 不过配置有点麻烦

既然没有合适的, 我就选择了自己写一个, 取名叫tfcs, 没有什么其它意义, 就是几个单词的缩写, 原谅我自恋了一把(TankyWoo Flask Code Snippet)...

关于这个tfcs, 项目主页[tankywoo/tfcs](https://github.com/tankywoo/tfcs), 目前是:

使用markdown作为静态输入源. 对这类文本标记语言, 尤其markdown, 我几乎达到一个狂热的地步了, 见我之前写的[Simiki](http://simiki.org/)就知道了...

依然使用了yaml front matter作为每一篇code snippet的meta信息.

    ---
    title: 'xxx'
    description: 'xxx'
    tag: xxx1,xxx2
    date: 2015-10-23 00:00
    id: xxx
    ---

    ...
    ...

当然, 这个id是暂时需要手动需生成的, 作为url部分, 我自己是使用的8位随机ascii/digit字符串, 以个人使用来说, 应该是足够了.

code snippet存放在一个单独的目录下, 有一个大的分类(category), 如:

    .
    ├── cpp
    │   └── xxx3.md
    ├── nodejs
    │   └── xxx4.md
    ├── python
    │   └── xxx1.md
    └── ruby
        └── xxx2.md

然后tag是在meta信息里配置的.

暂时使用os.path.walk遍历snippets目录, re分割meta和body. 试了几十篇的情况, 效率上应该是足够了.

关于它和wiki以及blog的区别, 这里简单说下我的理解:

* tfcs以snippet为主，几十上百字的简单的说明, 外加一个或多个snippet, 可以认为是一个微型blog.
* blog以记录生成、问题解决方案、研究的某一块笔记为主, 是一个更复杂的笔记
* wiki是在某一类形成一定规模时, 尤其blog上的, 可以逐步汇总到wiki上了

关于tfcs和以上web code snippet的对比缺点:

* 首次需要配置, 部署, 需要有自己的服务器
* 展示稍微麻烦, 比如我现在是更新后把文档传到我的vps指定目录上
* 没有fork/star功能, Gist的这个功能比较方便, 因为它自身就是一个snippets体系, 可以随时把别人的收藏了

后续考虑的:

* 数据源转换下存在sqlite里. 模式就是编辑md, 脚本转换写入sqlite, flask是直接和sqlite交互.
* 支持点击代码复制到clipboard
* category/tag分支检索
* ...

最后, 这个是折腾着玩写的, 后续基本不会怎么变动, 也没有考虑太多, 就像README里写的, be used with caution, 慎用...

demo传送门: [code.tankywoo.com](http://code.tankywoo.com)
