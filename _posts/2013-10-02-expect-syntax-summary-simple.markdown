---
layout: post
title: "Expect Syntax Summary - Simple"
date: 2013-10-02 12:47
comments: true
categories: Expect
---

<!-- more -->

# Expect #


## shellbang ##

Expect is an extension of shell script.

The shellbang of Expect:

	#!/usr/bin/expect

## timeout ##

The default timeout of Expect is `10s`.

Change timeout to 20s:

	set timeout 20

## define variable ##

	set var value
	# such as:
	set name "Tanky Woo"

## expr expression ##

	set cnt 2
	set sum "[ expr $cnt + $cnt ]"

## if statement ##

	if { $count < 0 } {
		puts "Success Condition1 : $count\n";
	} elseif { $count == 0  } {
		puts "Success Condition2 : $count\n";
	} else {
		puts "False : $count\n";
	}

## for loop ##

Format:

	for { init } { conditions } { incr | decr } {
		...
	}

Example:

	for { set i 1 } { $i < 5 } { incr i 1 } {
		puts "$i";
	}

## while loop ##

	set count 5;
	while { $count > 0 } {
		puts "count : $count\n";
		set count [expr $count-1];
	}

## switch ##

	set cnt 2
	switch -- $cnt \
		1 {
			puts "1"
		} 
		2 {
			puts "2"
		}
		default {
			puts "default";
		}
