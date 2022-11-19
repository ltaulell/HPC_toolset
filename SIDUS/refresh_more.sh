#!/bin/bash
# PSMN: $Id: refresh_more.sh 3796 2022-10-28 06:48:22Z ltaulell $
#
mount -o remount /
systemctl restart slurmd.service
systemctl restart munge.service
systemctl restart unscd.service
systemctl restart nslcd.service
systemctl restart autofs.service

