---
layout: post
title: "Double Quotes around Variable in Bash"
date: 2013-10-09 20:56
comments: true
categories: Linux
---

<!-- more -->

Example:

	x="-e h\ti"
	echo ${x}
	echo '------'
	echo "${x}"

Output:

	h       i
	------
	-e h\ti

The first echo statement equals to:

	echo -e h\ti

The second equals to:

	echo "-e h\ti"

From [Why Use Double Quotes around Variables in Bash?](http://www.solomonson.com/content/why-use-double-quotes-around-variables-bash)

Another example:

```bash
	files="foo bar baz"

	for file in ${files}
	do
		echo "${file}""<eol>"
	done
```

Output:

	foo<eol>
	bar<eol>
	baz<eol>

If I use double quotes around `${files}`, such as:

```bash
	files="foo bar baz"

	for file in "${files}"
	do
		echo "${file}""<eol>"
	done
```

The output:

	foo bar baz<eol>

Supplement, another for loop example:

```bash
	files=("foo" "bar" "baz")

	for file in "${files[@]}"
	do
		echo "${file}""<eol>"
	done
```
