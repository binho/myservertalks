#!/bin/bash
procname="smbd"
check=`ps aux | grep $procname | grep -v grep | wc -l`
if [ $check -eq 0 ]; then
	echo "WARNING: SAMBA SERVER DOWN"
	exit 0
fi
