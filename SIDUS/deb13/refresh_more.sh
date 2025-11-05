#!/bin/bash
# PSMN: $Id: refresh_more.sh 4890 2025-10-07 12:24:26Z ltaulell $
#
# mount -o remount /
echo 3 > /proc/sys/vm/drop_caches
sync
systemctl restart ssh.service
systemctl restart munge.service
systemctl restart unscd.service
systemctl restart nslcd.service
systemctl restart autofs.service
#systemctl restart slurmd.service
