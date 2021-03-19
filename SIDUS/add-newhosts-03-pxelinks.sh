#!/bin/bash
# PSMN: $Id: add-newhosts-03-pxelinks.sh 2857 2020-04-08 15:17:11Z ltaulell $
#

set -euo pipefail # strict mode
#set -x # Trace each command
#echo $*

if [[ $* == "" ]]
# no args
then
  printf "\n\tUsage: $0 dhcpfile basename\n"

else
  dhcpfile=$1
  basename=$2

  printf "\n\tUsage: $0 dhcpfile basename\n"

  printf "\n### ${basename}\n"

  grep -v "^#" ${dhcpfile} | tr "\n" ";" | sed -e "s/host/\n/g" | grep ${basename} | awk '{ print $1" "$7 }' | tr [A-Z] [a-z] | awk -F';' '{ print  $1 }' | tr ':' '-' | awk '{ print "ln -sf nodes/"$1" 01-"$2 }'

fi


