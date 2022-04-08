#!/bin/bash
#
# $Id: pre-install.sh 3595 2022-02-04 14:14:39Z ltaulell $
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

sidus mount -t proc none /proc
sidus mount -t sysfs sys /sys
mount --bind /dev/pts "${SIDUS}"/dev/pts
findmnt

echo "ready to install -> sidus apt-get install <package>"
echo ""
echo "finalyze with post-install.sh ${NODE}"

