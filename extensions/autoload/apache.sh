#!/bin/bash
# MyServerTalks! v1.2
# description: Autoload module to check if process its running 
# author: Cleber Santos
# url: myservertalks.com / binho.net
# Setup:
#
# Add the lines to your modules.ini file:
#
#       [autocheck_apache]
#       type = autoload
#       call = apache.sh
#       escope = user, super
#       status = enabled

procname="httpd"
check=`ps aux | grep $procname | grep -v grep | wc -l`
if [ $check -eq 0 ]; then
	echo "WARNING: APACHE SERVER DOWN"
fi
