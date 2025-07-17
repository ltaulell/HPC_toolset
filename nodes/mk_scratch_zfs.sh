#!/bin/bash
# $Id: mk_scratch_zfs.sh 4722 2024-12-11 15:38:51Z ltaulell $

#
# make zfs scratch
#

echo "NOT READY!"
exit 1

# HOST=$(hostname -s)
SCRIPTNAME=$(basename "${0}")
SCRATCHDIR="/scratch/local"
SCRATCHNAME="scratch"
MAXDISKS=8  # don't go over 24, it won't work (zfs raidz1 and script)

usage () {
    printf "    create a local RAID0/RAIDZ scratch disk \\n"
    printf "Usage: \\n"
    printf "    %s <number> <type>\\n" "${SCRIPTNAME}"
    printf "    number: number of disks, min 2, max %s\\n" "${MAXDISKS}"
    printf "    type: disk or ssd\\n"
    # $1 est ici le paramètre passée à la fonction
    if [[ $1 != "" ]]
    then
        echo -e "$1"
    fi
}

if [[ "${#}" -eq 0 || "${#}" -gt 2 ]]  # equal [[ -z "${1}" ]]
then
    usage "please provide a number of disks and a disk type"
    exit 1
elif [[ ! "${1}" =~ ^[[:digit:]]+$ ]]  # NOT a digit [0..9]
then
    usage "please provide a NUMBER (integer) of disks as first arg"
    exit 1
elif [[ "${1}" -lt 2 || "${1}" -gt "${MAXDISKS}" ]]  # 2 > x >= MAXDISKS
then
    usage "number of disks must be between 2 and ${MAXDISKS}"
    exit 1
elif [[ ! "${2}" =~ ^(disk|ssd)$ ]]  # NOT disk nor ssd
then
    usage "please provide a valid disk type as second arg [disk|ssd]"
    exit 1
else
    # build disks list
    DISKS=""
    for ((i=0; i<"${1}"; i++));
    do
        # convert number to ascii position
        nombre=$(( i + 97 ))
        # convert ascii position to actual character string
        letter=$(printf '%b' "$(printf '\\x%x' ${nombre})")
        # append to the disks list
        DISKS="${DISKS} sd${letter}"
    done
fi

# shellcheck disable=SC2206
MDD=($DISKS)  # transforme en array
NBDISKS=${#MDD[@]}  # taille du array, retrouve $1

# vérif user inputs
echo "disks: ${NBDISKS}, ${MDD[*]}"


# shellcheck disable=SC2010
mapfile -t BYPATH < <(ls /dev/disk/by-path/* | grep -v part | grep -v -e "\.0$")

# find disks from /dev/disk/by-path/? -> /dev/sd?
# readlink -f or realpath
PATHMDD=""
for i in "${BYPATH[@]}"
do
    # echo "${i}"
    REALPATH=$(realpath "${i}")
    for j in "${MDD[@]}"
    do
        # echo "${j}"
        if [[ ${REALPATH} =~ ${j} ]]
        then
            echo "adding: ${i}"
            PATHMDD="${PATHMDD} ${i}"
        fi
    done
done

# echo "${PATHMDD}"

# zpool/zfs create -f, name as $SCRATCHNAME
# mountpoint to $SCRATCHDIR
if [[ "${NBDISKS}" -eq 2 ]]
then
    # if 2, raid0 (stripe)
    CMD="zpool create -f -m ${SCRATCHDIR} ${SCRATCHNAME} stripe ${PATHMDD}"
elif [[ "${NBDISKS}" -gt 2 || "${NBDISKS}" -le ${MAXDISKS} ]]
then
    # else (2 < x <= ${MAXDISKS}), raidz1
    CMD="zpool create -f -m ${SCRATCHDIR} ${SCRATCHNAME} raidz1 ${PATHMDD}"
fi

echo "${CMD}"

read -rp "Do you want to proceed? (yes/no) " yn

case $yn in
    [yY] | yes)
        echo "OK, proceeding"
    ;;
    [nN] | no )
        echo "exiting."
        exit 0
    ;;
    * )
        echo "invalid answer, exiting."
        exit 1
    ;;
esac

echo "executing: ${CMD}"
${CMD}

# set zfs defaults
zfs set compression=on ${SCRATCHNAME}
zfs set snapdev=hidden ${SCRATCHNAME}
zfs set snapdir=hidden ${SCRATCHNAME}
zfs set xattr=sa ${SCRATCHNAME}
zfs set atime=off ${SCRATCHNAME}
zfs set relatime=off ${SCRATCHNAME}

# set unix owner:group defaults
echo "/bin/chmod ugo+rwXt ${SCRATCHDIR}"
/bin/chmod ugo+rwXt "${SCRATCHDIR}"
echo "mkdir -p ${SCRATCHDIR}/lost+found"
mkdir -p "${SCRATCHDIR}/lost+found"
echo "chown root:root ${SCRATCHDIR}/lost+found"
chown root:root "${SCRATCHDIR}/lost+found"
echo "chmod go-rwXst ${SCRATCHDIR}/lost+found"
chmod go-rwXst "${SCRATCHDIR}/lost+found"
echo "ls -ltr ${SCRATCHDIR}"
ls -ltr "${SCRATCHDIR}"
echo "all done."
