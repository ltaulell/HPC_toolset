#!/bin/bash
#
# $Id: get_slurm_global.sh 4740 2025-01-09 13:12:51Z ltaulell $
#

# compilation de get_slurm_partition_usage_cli.sh et get_slurm_cpu.sh

declare -a VALUE

printf "By partition (%%):\n" # %16s

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
    #printf "%13s:" "${partition}"; printf " %0.s" $(seq 1 $((15-${#partition}))); printf "%d%%\n" "${VALUE[$i]}"
    printf "%16s: %6d%%\n" "${partition}" "${VALUE[$i]}"
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
#printf "%13s:" "${str}"; printf " %0.s" $(seq 1 $((15-${#str}))); printf "%d%%\n" "${GRATE}"
printf "%16s: %6d%%\n" "${str}" "${GRATE}"

printf "\n%16s:\n" "By core usage"

RUNNING=$(squeue -h -o "%t %C" | awk 'BEGIN {somme=0} /R/ {somme+=($2)} END {print somme}')
PENDING=$(squeue -h -o "%t %C" | awk 'BEGIN {somme=0} /PD/ {somme+=$2} END {print somme}')
# TOTAL=$(sinfo -h -e -o '%8X %8Y %5D' | awk 'BEGIN {somme=0} {somme+=($1 * $2 * $3)} END {print somme}')
TOTAL=$(sinfo -h -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($4)} END {print somme}')
AVAIL=$(sinfo -h -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($2)} END {print somme}')
UNAVAIL=$(sinfo -h -e -o '%C' | awk -F'/' 'BEGIN {somme=0} {somme+=($3)} END {print somme}')
NODES=$(sinfo -h --exact --format="%.5D")

PERCENT=$(((RUNNING * 100) / (TOTAL-UNAVAIL)))

printf "%16s: %6d\n" "Running Cores" ${RUNNING}
printf "%16s: %6d\n" "Pending Cores" ${PENDING}
printf "%16s: %6d\n" "Available" ${AVAIL}
printf "%16s: %6d\n" "Unavailable" ${UNAVAIL}
printf "%16s: %6d\n" "Overall Total" ${TOTAL}
printf "\n"
# %% -> literal '%' symbol
printf "%16s: %6d%%\n" "Overall Use" ${PERCENT}
printf "%16s: %6d\n" "Total nodes" ${NODES}

echo ""
sinfo -R

exit 0
