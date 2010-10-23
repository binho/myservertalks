#!/bin/bash
procname="netbeans"
check=`ps aux | grep $procname | grep -v grep | wc -l`
if [ $check -eq 0 ]; then
	echo "WARNING: PROCESSO PARADO"
fi
