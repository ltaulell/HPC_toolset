#!/bin/bash
#
# $Id: post-install.sh 3594 2022-02-04 11:06:59Z ltaulell $
# SPDX-License-Identifier: BSD-2-Clause
#

set -euo pipefail # strict mode
#set -vx # Trace each command

function usage() {
    printf "\n\tUsage: %s <node9|node11>\n" "$0"
}

if [[ ${#} -eq 1 ]]
then
    if [[ ${1} == "node9" ]] || [[ ${1} == "node11" ]]
    then
        NODE="${1}"
    else
        usage
        exit 1
    fi
else
    usage
    exit 1
fi

export SIDUS="/data/hosts/${NODE}"
sidus() { DEBIAN_FRONTEND=noninteractive chroot "${SIDUS}" "$@"; }
export ARCH=amd64

umount -l /data/hosts/"${NODE}"/dev/pts
umount -l /data/hosts/"${NODE}"/sys
umount -l /data/hosts/"${NODE}"/proc
findmnt
