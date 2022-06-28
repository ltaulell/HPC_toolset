#!/bin/bash
#
# PSMN: $Id: sge_get_cpu.sh 1511 2016-12-16 09:51:24Z ltaulell $
#

CPU=$(qstat -g c | grep -vi -e "test" | tail -n +3 | awk '{somme+=$3} END {print somme}')
PENDING=$(qstat -s p -u "*" | awk '{somme+=$8} END {print somme}')
AVAIL=$(qstat -g c | grep -vi -e "test" | tail -n +3 | awk '{somme+=$5} END {print somme}')
TOTAL=$(qstat -g c | grep -vi -e "test" | tail -n +3 | awk '{somme+=$6} END {print somme}')

echo "Cores consommés : ${CPU}"
echo "En attente : ${PENDING}"
echo "Disponible : ${AVAIL}"
echo "Total brut : ${TOTAL}"

exit 0
