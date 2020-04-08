#!/usr/bin/env python3
# coding: utf-8

##
## $Id: add_newhosts.py 2857 2020-04-08 15:17:11Z ltaulell $
##

"""
Ajout d'un host ou d'un groupe de host au PSMN, en 4 étapes :

1 : ajout au fichier /etc/hosts (all servers & nodes)
2 : ajout au fichier /etc/dhcpd.conf @ psmn-pxe
3 : création des liens PXE (dans /tftpboot/pxelinux.cfg @ psmn-pxe)
4 : ajout des hostnames dans le fichier /etc/postfix/machines @ psmn-postfix-out

Ce script prépare un output pour 3 des 4 étapes, qu'il n'y aura qu'a
copier/coller aux endroits concernés.

Usage: $0 -[nfs|gb|ib] basename extension([lin|node|gpu]) network first last

"""

import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ajout d'un host (ou d'un groupe de host)")
    parser.add_argument("-d", action="store_true", help="Active le debug")
    parser.add_argument("-gb", action="store_true", help="Ajoute un réseau privé gigabit (10.80.<network>.<host>)")
    parser.add_argument("-ib", action="store_true", help="Ajoute un réseau privé InfiniBand (10.50.<network>.<host>)")
    parser.add_argument("basename", type=str, help="nom de base")
    parser.add_argument("extension", type=str, help="extension ([lin|node|gpu])")
    parser.add_argument("network", type=int, help="sous-réseau de classe C dans le 172.16")
    parser.add_argument("premier", type=str, help="premier de la liste (filler)")
    parser.add_argument("dernier", type=str, help="dernier de la liste")
    args = parser.parse_args()

    filler = len(str(args.premier))
    premier = int(args.premier)
    dernier = int(args.dernier)

    if args.d:
        print("gb :", args.gb)
        print("ib :", args.ib)
        print("net :", args.network)
        #print(args.basename, args.extension, '{num:03d}'.format(num=args.premier), '{num:03d}'.format(num=args.dernier))  # pour mémoire
        print(args.basename, args.extension, str(premier).zfill(filler), str(dernier).zfill(filler))

    print("\n*** Etape 1, /etc/hosts :")
    print("### ", args.basename, args.extension, str(premier).zfill(filler), "-", str(dernier).zfill(filler))

    for i in range(premier, (dernier + 1)):
        host = args.basename + args.extension + str(i).zfill(filler)
        print("172.16." + str(args.network) + "." + str(i) + "\t" + host + "\t" + host + ".psmn.ens-lyon.fr")
        if args.gb:
            print("10.20." + str(args.network) + "." + str(i) + "\t" + host + "-gb")
        if args.ib:
            print("10.50." + str(args.network) + "." + str(i) + "\t" + host + "-ib")
        print("10.80." + str(args.network) + "." + str(i) + "\t" + host + "-mngt")

    print("\n*** Etape 2, /etc/dhcpd.conf :")
    print("### ", args.basename, args.extension, str(premier).zfill(filler), "-", str(dernier).zfill(filler))

    for i in range(premier, (dernier + 1)):
        host = args.basename + args.extension + str(i).zfill(filler)
        print("  host", host, "{")
        print("    fixed-address 172.16." + str(args.network) + "." + str(i) + ";")
        print("    hardware ethernet ;")
        print("  }")

    print("\n*** Etape 3, /etc/postfix/machines :")
    for i in range(premier, (dernier + 1)):
        host = args.basename + args.extension + str(i).zfill(filler)
        print(host + ".psmn.ens-lyon.fr")
        print(host)


    print("\n*** Etape 4, pxelinks group\n")
    liste = []
    for i in range(premier, (dernier + 1)):
        host = args.basename + args.extension + str(i).zfill(filler)
        liste.append(host)
    print("cd nodes ; for i in " + ' '.join(liste) + "; do ln -s " + args.basename + args.extension + ".cfg $i ; done")

    print("\n*** Etape 5, utiliser ~/Code/tools4psmn/tools/add-newhosts-03-pxelinks.sh $HOME/Code/tools4psmn/etc-files/dhcpd.conf " + str(args.basename) + "\n")

    print("\n*** Etape 6, svn commit\n")
    
    print("\n*** Etape 7, ~/Code/tools4psmn/tools/add-newhosts-05-update.sh\n")
