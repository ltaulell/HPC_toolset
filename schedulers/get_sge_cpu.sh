#!/bin/bash
#
# PSMN: $Id: get_sge_cpu.sh 3695 2022-07-05 12:59:26Z ltaulell $
#

RUNNING=$(qstat -g c | grep -vi -e "test" | tail -n +3 | awk '{somme+=$3} END {print somme}')
PENDING=$(qstat -s p -u "*" | awk '{somme+=$8} END {print somme}')
AVAIL=$(qstat -g c | grep -vi -e "test" | tail -n +3 | awk '{somme+=$5} END {print somme}')
UNAVAIL=$(qstat -g c | grep -vi -e "test" | tail -n +3 | awk '{somme+=$8} END {print somme}')
TOTAL=$(qstat -g c | grep -vi -e "test" | tail -n +3 | awk '{somme+=$6} END {print somme}')

PERCENT=$(((RUNNING * 100) / (TOTAL-UNAVAIL)))

echo "Running Cores: ${RUNNING}"
echo "Pending Cores: ${PENDING}"
echo "Available    : ${AVAIL}"
echo "Unavailable  : ${UNAVAIL}"
echo "Overall Total: ${TOTAL}"
echo ""
echo "Overall Use  : ${PERCENT}%"


exit 0
