#!/bin/bash
# PSMN: $Id: get_top10_lab_year.sh 4317 2024-02-12 13:44:16Z ltaulell $

#set -x
if [[ $# -ne "2" ]];
then
    printf "\\nDisplay top 10 users, by lab, sorted\\n"
    printf "\\n\\tUsage: %s <lab> <numeric year> \\n" "$0"
    exit 0
else
    LAB="$1"
    YEAR="$2"
fi

echo "for ${YEAR}: login, hours"

sreport -n cluster AccountUtilizationByUser -t Hours Start="${YEAR}"-01-01 End="${YEAR}"-12-31 format=Login,Used Accounts="${LAB}" | sort -nk2 -r | head -n 10

