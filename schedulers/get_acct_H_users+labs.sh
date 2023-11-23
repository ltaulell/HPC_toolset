#!/bin/bash
# PSMN: $Id: get_acct_H_users+labs.sh 4245 2023-11-23 10:07:46Z ltaulell $

if [ "$1" == "" ]
then
    printf "\\n\\tUsage: %s <numeric year> of wanted accounting \\n" "$0"
    exit 1
else  # FIXME test numeric only '=~ [0-9]{4}'?
    YEAR="$1"
fi

LOGINS=$(sacctmgr -n show user format=User%30 | xargs)

shopt -s lastpipe  # for read to assign to UTIME array

echo "${YEAR}: login, heures"
for LOGIN in $LOGINS
do
    UTIME=()  # naïve array
    # UTIME=$(sreport -n cluster AccountUtilizationByUser format=Account,Used -t Hours Start="${YEAR}"-01-01T00:00:00 end="${YEAR}"-12-31T23:59:59 user="${LOGIN}")
    # insert output into array with read
    sreport -n cluster AccountUtilizationByUser format=Account,Used -t Hours Start="${YEAR}"-01-01T00:00:00 end="${YEAR}"-12-31T23:59:59 user="${LOGIN}" | IFS=" " read -r -a UTIME
    if [[ "${UTIME[1]}" == "" ]]
    then
        UTIME[1]="0"
        if [[ "${UTIME[0]}" == "" ]]
        then
            # get lab, and squeeze whitespaces from output
            UTIME[0]=$(sacctmgr -n show Association format=Account user="${LOGIN}" | tr -s '[:blank:]')
        fi
    fi
    echo "${LOGIN}, ${UTIME[0]}, ${UTIME[1]}"
done
