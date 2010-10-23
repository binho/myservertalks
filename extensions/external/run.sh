#!/bin/bash
# Run some command and get output

echo "contact mail: "$1
echo "escope: "$2
echo "command: "$3
echo "params: "$4

CMD=`echo $4 | sed 's/;/ /g'`
echo $CMD
$CMD

exit 0
