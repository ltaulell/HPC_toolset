#!/bin/bash
#
#PSMN: $Id: du_labs.sh 3008 2020-10-13 14:24:00Z ltaulell $

# run only on data servers, not on client nodes

# quick & dirty
# du -sh /users/chimie/* > chimie.usage.20170515.txt
# this script + cron:
# mn h d w m user command
#0 23 * * * root /root/tools/du_labs.sh /users/chimie > /dev/null 2>&1

## TODO
# add email address as param

## DEBUG
set -euo pipefail # strict mode
#set -x # Trace each command

SCRIPTNAME=$(basename "$0")

function F_Usage {
    printf "\\n  %s \\n\\n" "$1"
    printf "%s: volume to scan (/users/<lab> for example) \\n\\n" "${SCRIPTNAME}"
    printf "Usage: %s <volume>\\n\\n" "${SCRIPTNAME}"
}

if [[ ${#} -eq 0 ]] # equal
then
    F_Usage "Too few argument"
    exit 1
elif [[ ${#} -ne 1 ]]
then
    F_Usage "Too much arguments"
    exit 1
fi

VOLUME=$1
LABO=$(basename "${VOLUME}")
DATE=$(date +%Y%m%d%H%M)
HOST=$(hostname)
DUDIR="/root/usage"
DUFILE="${DUDIR}/${LABO}.usage.${DATE}.txt"
TMPFILE=$(mktemp /tmp/"${SCRIPTNAME}".XXXXXXXX) || { echo "cannot create ${TMPFILE}"; exit 1; }
MAILRECIPIENT="example@example.org"

if [[ ! -d "${DUDIR}" ]]
then
    mkdir -p "${DUDIR}"
fi

du -sh "${VOLUME}"/* > "${DUFILE}"

date >>  "${DUFILE}"

# do NOT modify $DUFILE as it is diff-able
#cat ${DUFILE} | sort -r -h > ${TMPFILE}

# to send both ${DUFILE} and ${TMPFILE}, cat both...
# FIXME: UUOC

/bin/cat "${DUFILE}" | /usr/bin/mailx -a "From: ${HOST} <${MAILRECIPIENT}>" -s "${HOST}: ${SCRIPTNAME}" "${MAILRECIPIENT}" --

rm -f "${TMPFILE}"

exit 0

