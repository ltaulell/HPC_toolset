#!/bin/bash
# PSMN: $Id: set-cpufreq.sh 3842 2022-11-19 09:50:25Z ltaulell $

set -euo pipefail # strict mode
#set -x # Trace each command

# GOVERNORS="ondemand userspace powersave conservative performance schedutil"
# see https://www.kernel.org/doc/Documentation/cpu-freq/governors.txt
GOVERNORS="powersave ondemand performance"
GOVERNOR=""
HOST=$(hostname -s)
LOG="logger -is -- ${HOST}: "

function usage() {
    printf "\n\tUsage: %s <governor>\n" "$0"
    printf "\n available governors: %s \n" "$GOVERNORS"
}

# filter user entry
if [[ ${#} -eq 1 ]]
then
    for i in ${GOVERNORS}
    do
        if [[ ${i} =~ ${1} ]]
        then
            GOVERNOR="${1}"
        fi
    done
    if [[ ${GOVERNOR} == "" ]]
    then
        usage
        exit 1
    fi
else
    usage
    exit 1
fi

NPROC=$(nproc)

for ((i=0; i<NPROC; i++))
do
    cpufreq-set -c "${i}" -r -g "${GOVERNOR}" 
done

$LOG "cpufreq done, applied ${GOVERNOR}"

#
