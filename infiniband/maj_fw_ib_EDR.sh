#!/bin/bash
# PSMN: $Id: maj_fw_ib_EDR.sh 3149 2021-01-09 13:52:54Z ltaulell $

# script to mass-update EDR infiniband card firmware
#
# depending on your config, you may have to change MAC0 replacement
# and/or firmware images (FWIMG)
#

# set's
set -euo pipefail # strict mode
#set -vx # Trace each command

BASEPATH="/applis/PSMN/Staff/Maintenance/Mellanox"
PCI=$(lspci | grep -i ellanox | awk '{ print $1 }')

# shellcheck disable=SC1117
cd ${BASEPATH} || { echo -e "\nE: cannot cd to ${BASEPATH}"; exit 1; }

# install flint 4.15, needed for EDR hardware
# get latest versions https://www.mellanox.com/products/adapter-software/firmware-tools
if ! flint -v | grep -q -e "4.15";
then
    dpkg -i kernel-mft-dkms_4.15.0-104_all.deb
    dpkg -i mft_4.15.0-104_amd64.deb
fi

FLINT="/usr/bin/flint"

PSID=$(${FLINT} -d "${PCI}" q | grep PSID: | awk '{ print $2 }')

# get latest versions https://www.mellanox.com/support/firmware/connectx4ib
case "${PSID}" in
    MT_2190110032 | HP_2190110032 )
        FWIMG="MT27700_EDR/fw-ConnectX4-rel-12_28_2006-MCX456A-ECA_Ax-UEFI-14.21.17-FlexBoot-3.6.102.bin"
    ;;

    # keep as example
    # DEL1100001019 )
    #     FWIMG="MT27500/fw-ConnectX3-rel-2_42_5000-079DJ3-FlexBoot-3.4.752.bin"
    # ;;

    * )
        # shellcheck disable=SC1117
        echo -e "\nE: unrecognized PSID!"
        exit 1
    ;;

esac

echo -e "Processing device: ${PCI}"
${FLINT} -d "${PCI}" --allow_psid_change -i "${FWIMG}" b
