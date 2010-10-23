#!/bin/sh -e

# MyServerTalks! v1.2
# description: Show procs ordered by CPU usage
# author: Cleber Santos
# url: myservertalks.com / binho.net

# Setup:
#
# Add the lines to your modules.ini file:
#
# 	[cpu-high-procs]
# 	type = external
# 	call = cpu-high-procs.sh
# 	escope = super
# 	status = enabled

ps -e -o pcpu,cpu,nice,state,cputime,args --sort pcpu | sed '/^ 0.0 /d'
