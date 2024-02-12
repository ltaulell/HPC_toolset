#!/bin/bash
#
# $Id: get_slurm_global_usage_cli.sh 4314 2024-02-12 10:42:00Z ltaulell $
#

declare -a VALUE

for partition in $(sinfo -h -o "%R")
# by partitions
do

    RUNNING=$(squeue -h -p "${partition}" -o "%t %C" -t R | awk 'BEGIN {somme=0} /R/ {somme+=($2)} END {print somme}')
    TOTAL=$(sinfo -h -p "${partition}" -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($4)} END {print somme}')
    UNAVAIL=$(sinfo -h -p "${partition}" -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($3)} END {print somme}')
    # there could be a "divided by zero" error
    if [[ $((TOTAL-UNAVAIL)) == 0 ]]
    then
        PERCENT=0
    else
        DIVISOR=$((TOTAL-UNAVAIL))
        PERCENT=$(((RUNNING * 100) / DIVISOR))
    fi
    VALUE[${partition}]="${PERCENT}"
    #echo "${partition}: ${VALUE[$i]}%"
    #printf "%s:\t %.1f%%\n" "${partition}" "${VALUE[$i]}"
    # proper aligment (fill with spaces minus lenght of word)
    printf "%s:" "${partition}"; printf " %0.s" $(seq 1 $((15-${#partition}))); printf "%d%%\n" "${VALUE[$i]}"
done

# global
RUNNING=$(squeue -h -o "%t %C" -t R | awk 'BEGIN {somme=0} /R/ {somme+=($2)} END {print somme}')
TOTAL=$(sinfo -h -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($4)} END {print somme}')
UNAVAIL=$(sinfo -h -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($3)} END {print somme}')
PERCENT=$(((RUNNING * 100) / (TOTAL-UNAVAIL)))
GRATE="${PERCENT}"
str="global"
#echo "${str}: ${GRATE}%"
#printf "%s:\t%d%%\n" "${str}" "${GRATE}"
printf "%s:" "${str}"; printf " %0.s" $(seq 1 $((15-${#str}))); printf "%d%%\n" "${GRATE}"

