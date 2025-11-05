#!/bin/bash
# PSMN: $Id: refresh.sh 4890 2025-10-07 12:24:26Z ltaulell $
#
# mount -o remount /
echo 3 > /proc/sys/vm/drop_caches
sync
