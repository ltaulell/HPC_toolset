#!/bin/bash
# PSMN: $Id: get_acct_group.sh 4149 2023-09-20 15:23:43Z ltaulell $

#set -x
if [ "$1" == "" ]
then
    printf "\\n\\tUsage: %s <numeric year> of wanted accounting \\n" "$0"
    exit 0
else
    YEAR="$1"
fi

GRPS=$(sacctmgr -nP list account format=account | uniq | xargs)

echo "${YEAR}: groupe, jobs, heures"
for GRP in $GRPS
do
    # pour chaque mois, cumul de :
    # sreport -n job sizes printjobcount start=$ end=$ account=$ | awk -F" " '{ SUM +=$3+$4+$5+$6+$7} END {print $2" "SUM}'



    UTIME=$(sreport -n cluster AccountUtilizationByUser format=Used -t Hours Start="${YEAR}"-01-01T00:00:00 end="${YEAR}"-12-31T23:59:59 Accounts="${GRP}" | head -1)
    #UTIME=${UTIME%%$'\n'*}
    if [[ "${UTIME}" == "" ]]
    then
        UTIME="0"
    fi
  echo "${GRP}, ${UTIME}"
done

exit 0

# passer en function, return "start, end"
currentdate="$YEAR-01-01"
last=$((YEAR + 1))
loopenddate=$(/bin/date --date "$last-01-01 1 month" +%Y-%m-%d)

until [ "$currentdate" == "$loopenddate" ]
do
  echo $currentdate
  currentdate=$(/bin/date --date "$currentdate 1 month" +%Y-%m-%d)
done

# autre essai
currentdate="$YEAR-01-01"
for i in {1..13}
do
  echo $currentdate
  currentdate=$(/bin/date --date "$currentdate 1 month" +%Y-%m-%d)
done
