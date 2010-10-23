#!/bin/sh -e

# MyServerTalks! v1.2
# description: Apache handler 
# author: Cleber Santos
# url: myservertalks.com / binho.net

# Setup:
#
# Add the lines to your modules.ini file:
#
#       [apache]
#       type = external
#       call = apache.sh
#       escope = super
#       status = enabled

# apachectl script path
APACHECTL=/etc/init.d/apache2

case $4 in
	start)
		exec $APACHECTL start;
	;;
	stop)
		exec $APACHECTL stop;
	;;
	restart)
		exec $APACHECTL stop;
		sleep 10
		exec $APACHECTL start;
	;;
	*)
		echo "Usage: apache {start|stop|restart}"
	;;
esac
