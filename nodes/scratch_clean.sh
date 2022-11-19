#!/bin/bash
# $Id: scratch_clean.sh 3847 2022-11-19 10:16:26Z ltaulell $

#
# find and erase files/directories older than 120 days
#

# set's
#set -euo pipefail # strict mode, beware with "-e + pipefail", exit on first error
#set -x # Trace each command

HOST=$(hostname -s)
LOG="logger -is -- ${HOST}: "
SCRATCHDIR="/scratch"  # must not be empty

case "${HOST}" in
# only on /scratch/[disk,ssd,local]
    c8220node* )
    # ssd
    HOSTNUM=${HOST/c8220node/}
    if [[ "${HOSTNUM}" -ge "41" && "${HOSTNUM}" -le "56" ]]
    then
        $LOG "cleaning /scratch/ssd"
        SCRATCHDIR="/scratch/ssd"
    elif [[ "${HOSTNUM}" -ge "169" && "${HOSTNUM}" -le "176" ]]
    then
        $LOG "cleaning /scratch/ssd"
        SCRATCHDIR="/scratch/ssd"
    fi
    ;;

    c6420node* )
    # disk

    # The simpliest way to strip leading '0', like
    # 'sed "s/^ 0//g"' or "new=${old##+(0)}" is to add 0:
    # HOSTNUM=$(expr "${HOST/c6420node/}" + 0)
    # or to convert to decimal : new=$((10#${old}))
    HOSTNUM=$((10#"${HOST/c6420node/}"))
    if [[ "$HOSTNUM" -ge "49" && "$HOSTNUM" -le "60" ]]
    then
        $LOG "cleaning /scratch/disk"
        SCRATCHDIR="/scratch/disk"
    fi
    ;;

    r740gpu* )
    # local

    # strip leading '0'
    HOSTNUM=$((10#"${HOST/r740gpu/}"))
    if [[ "$HOSTNUM" -ge "6" && "$HOSTNUM" -le "9" ]]
    then
        $LOG "cleaning /scratch/local"
        SCRATCHDIR="/scratch/local"
    fi
    ;;

    r740bigmem201 )
    # disk
        $LOG "cleaning /scratch/disk"
        SCRATCHDIR="/scratch/disk"
    ;;

    * )
        $LOG "no local scratch, exiting..."
        exit 0
    ;;
esac

# cleanup files older than 120 days, except in ${SCRATCHDIR}/programs/ (lch special)
find "${SCRATCHDIR}/" -not -path "${SCRATCHDIR}/lost+found" -not -path "${SCRATCHDIR}/programs/*" -type f -iname '*' -ctime +120 -exec rm -f {} \;

# cleanup empty directories as well
find "${SCRATCHDIR}/" -not -path "${SCRATCHDIR}/lost+found" -not -path "${SCRATCHDIR}/programs/*" -empty -type d -delete

# proper unix rights on /lost+found/, bad lch scripts
chmod -R go-rwxst "${SCRATCHDIR}/lost+found/"
