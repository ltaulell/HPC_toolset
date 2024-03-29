#!/bin/bash
# PSMN: $Id: maj_fw_ib_FDR.sh 3386 2021-09-28 06:57:59Z ltaulell $

# script to mass-update infiniband card firmware
#
# depending on your config, you may have to change MAC0 replacement
# and/or firmware images (FWIMG)
#

# set's
set -euo pipefail # strict mode
#set -vx # Trace each command

BASEPATH="/applis/PSMN/Staff/Maintenance/Mellanox"
PCI=$(lspci | grep -i ella | awk '{ print $1 }')
FLINT="${BASEPATH}/mstflint-3.7.0/flint/mstflint"
GUID=$("${FLINT}" -d "${PCI}" query | grep GUIDs: | awk '{ print $2 }')

# shellcheck disable=SC1117
cd ${BASEPATH} || { echo -e "\nE: cannot cd to ${BASEPATH}"; exit 1; }

# GUID contain '0300', 'ffff' or 'e0000'
if [[ "${GUID}" =~ "0300" ]]
then
    # shellcheck disable=SC2001
    MAC0=$(echo "${GUID}" | sed -e "s/0300//g")

elif [[ "${GUID}" =~ "ffff" ]]
then
    # shellcheck disable=SC2001
    MAC0=$(echo "${GUID}" | sed -e "s/ffff//g")

elif [[ "${GUID}" =~ "e0000" ]]
then
    # shellcheck disable=SC2001
    MAC0=$(echo "${GUID}" | sed -e "s/e0000/e/g")

else
    # shellcheck disable=SC1117
    echo -e "\nE: GUID mismatch!"
    exit 1
fi

MAC=$(printf '%X' $((0x$MAC0+0x1)))

PSID=$(${FLINT} -d "${PCI}" q | grep PSID: | awk '{ print $2 }')

case "${PSID}" in
    MT_1090120019 | HP_0280210019 | ORC1090120019 )
        FWIMG="MT27500/fw-ConnectX3-rel-2_42_5000-MCX354A-FCB_A2-A5-FlexBoot-3.4.752.bin"
    ;;

    MT_1100120019 )
        FWIMG="MT27500/fw-ConnectX3-rel-2_42_5000-MCX353A-FCB_A2-A5-FlexBoot-3.4.752.bin"
    ;;

    ISL1090110018 )
        # shellcheck disable=SC1117
        echo -e "\nW: FDR10 card !"
        FWIMG="MT27500/fw-ConnectX3-rel-2_42_5000-MCX354A-QCB_Ax-FlexBoot-3.4.752.bin"
    ;;

    DEL1100001019 )
        FWIMG="MT27500/fw-ConnectX3-rel-2_42_5000-079DJ3-FlexBoot-3.4.752.bin"
    ;;

    DEL0A30000019 )
        FWIMG="MT27500/fw-ConnectX3-rel-2_42_5000-0T483W-FlexBoot-3.4.752.bin"
    ;;

    HP_1370110017 )
        FWIMG="MT27500/fw-ConnectX3Pro-rel-2_42_5000-MCX314A-BCC_Ax-FlexBoot-3.4.752.bin"
    ;;

    * )
        # shellcheck disable=SC1117
        echo -e "\nE: unrecognized PSID!"
        exit 1
    ;;

esac

echo -e "Processing device: ${PCI}"
${FLINT} -d "${PCI}" --allow_psid_change --guid "${GUID}" --mac "${MAC}" -i "${FWIMG}" b
