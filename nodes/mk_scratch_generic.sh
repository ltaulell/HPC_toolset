#!/bin/bash
# $Id: mk_scratch_generic.sh 3842 2022-11-19 09:50:25Z ltaulell $

#
# over complicated "make md scratch" that fits them all (hopefully)
#

HOST=$(hostname -s)
SCRIPTNAME=$(basename "${0}")

usage () {
    printf "    create a local RAID0 scratch disk \\n"
    printf "Usage: \\n"
    printf "    %s <number> <type>\\n" "${SCRIPTNAME}"
    printf "    number: number of disks, min 2, max 8\\n"
    printf "    type: disk or ssd\\n"
    # $1 est ici le paramètre passée à la fonction
    if [[ $1 != "" ]]
    then
        echo -e "$1"
    fi
}

if [[ "${#}" -eq 0 || "${#}" -gt 2 ]]  # equal [[ -z "${1}" ]]
then
    usage "please provide a number of disks and a type"
    exit 1
elif [[ ! "${1}" =~ ^[[:digit:]]+$ ]]  # NOT a digit [0..9]
then
    usage "please provide a NUMBER (integer) of disks as first arg"
    exit 1
elif [[ ! "${2}" =~ ^(disk|ssd)$ ]]  # NOT disk nor ssd
then
    usage "please provide a valid type as second arg"
    exit 1
else
    # case switch suivant nb de disk en arg $1
    # DISK=$(echo "sd"{a..b to f})
    case "${1}" in
        1 )
        usage "cannot do raid scratch with one disk."
        exit 1
        ;;

        2 )
        DISKS=$(echo "sd"{a..b})
        ;;

        3 )
        DISKS=$(echo "sd"{a..c})
        ;;

        4 )
        DISKS=$(echo "sd"{a..d})
        ;;

        5 )
        DISKS=$(echo "sd"{a..e})
        ;;

        6 )
        DISKS=$(echo "sd"{a..f})
        ;;

        8 )
        DISKS=$(echo "sd"{a..h})
        ;;

        * )
        usage "can only do from [2-6,8] disks (2 to 6, or 8)."
        exit 1
        ;;

    esac

fi

# shellcheck disable=SC2206
MDD=($DISKS)  # transforme en array
NBDISKS=${#MDD[@]}  # taille du array, retrouve $1
LOOPMDD=$(for i in "${MDD[@]}" ; do echo -n "/dev/${i}1 "; done)

# vérif
echo "${NBDISKS}: ${LOOPMDD}"

# stop/erase existing raid
for i in {0..127}
do
    if [[ -e "/dev/md${i}" ]]
    then
        mdadm --misc --stop "/dev/md${i}"
    fi
done

# réglages individuels
for i in ${DISKS}
do
    dd if=/dev/zero of=/dev/"${i}" bs=512k count=1000
    sleep 2s
    partprobe -s /dev/"${i}"
    sleep 2s
    parted -a optimal /dev/"${i}" mklabel msdos
    #parted -a optimal /dev/"${i}" mklabel gpt
    parted -a optimal /dev/"${i}" mkpart primary ext4 0% 100%
    #sdparm --set=WCE /dev/"${i}"
    parted /dev/"${i}" set 1 raid on
    partprobe -s /dev/"${i}"
done

# création du software raid0
# oui, 50+ lignes pour cette simplification

NB=$(printf "%d " "${NBDISKS}")  # ici, mdadm veut int, pas str
# shellcheck disable=SC2086
mdadm --create /dev/md0 --level 0 --raid-devices=${NB} ${LOOPMDD}

# speedup, please
sysctl -w dev.raid.speed_limit_min=50000
sysctl -w dev.raid.speed_limit_max=500000

sleep 5s

if [[ "${2}" =~ "disk" ]]
then
    mkfs.ext4 -L scratch /dev/md0
    blkid /dev/md0
    sync
    mkdir -p /scratch/disk
    mount -L "scratch" /scratch/disk
    /bin/chmod ugo+rwXt /scratch/disk

elif [[ "${2}" =~ "ssd" ]]
then
    mkfs.ext4 -L ssdscratch /dev/md0
    blkid /dev/md0
    sync
    mkdir -p /scratch/ssd
    mount -L "ssdscratch" /scratch/ssd
    /bin/chmod ugo+rwXt /scratch/ssd
fi

echo "$HOST: please survey md creation with:"
echo "    cat /proc/mdstat"
echo ""
exit 0

## usefull mdadm cmds
# mdadm --readonly /dev/md127
# mdadm --misc --stop /dev/md127 ou mdadm -S /dev/md127
# mdadm --zero-superblock /dev/sd?1
# sfdisk -l /dev/sd?
