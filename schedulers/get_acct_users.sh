#!/bin/bash
# PSMN: $Id: get_acct_users.sh 3911 2023-02-07 12:36:13Z ltaulell $

if [ "$1" == "" ]
then
    printf "\\n\\tUsage: %s <numeric year> of wanted accounting \\n" "$0"
    exit 1
else  # FIXME test numeric only '=~ [0-9]{4}'?
    YEAR="$1"
fi

LOGINS=$(sacctmgr -n show user format=User%30 | xargs)

echo "${YEAR}: login, heures"
for LOGIN in $LOGINS
do
    UTIME=$(sreport -n cluster AccountUtilizationByUser format=Used -t Hours Start="${YEAR}"-01-01T00:00:00 end="${YEAR}"-12-31T23:59:59 user="${LOGIN}")
    if [[ "${UTIME}" == "" ]]
    then
        UTIME="0"
    fi
    echo "${LOGIN}, ${UTIME}"
done
