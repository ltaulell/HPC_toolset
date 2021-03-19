# HPC toolset

PSMN HPC tools for everyday sysadmin.

[PSMN](http://www.ens-lyon.fr/PSMN/) is "Pôle Scientifique de Modélisation Numérique", the Computing Center and "MesoCentre" of [École Normale Supérieure de Lyon](http://www.ens-lyon.fr/en/).

## usefull tools

- [ClusterSSH](https://github.com/duncs/clusterssh)

- [ClusterShell](https://github.com/cea-hpc/clustershell) python module, with 
  NodeSet, from CEA

- [execo](http://execo.gforge.inria.fr/doc/latest-stable/) python module, from 
  INRIA, also [execo-g5k-tools](https://github.com/lpouillo/execo-g5k-tools)

- [shellcheck](https://github.com/koalaman/shellcheck) linter for bash scripts

- [milkcheck](https://github.com/cea-hpc/milkcheck) ansible/salt-like from CEA

## PSMN tools

These are small scripts and sets of scripts we use on a regular basis.

### infiniband

#### ask_infiniband.py

build a CSV list, from cluster's nodes, of firmware revisions and PSIDs, when 
upgrade time as come... Ease the choice of firmware images for download and burn.

#### maj_ib_fw.sh

flash infiniband firmware, based on PSID.

#### map_GUID.py

Create a 'GUID hostname' map file, for use with Infiniband topological tools.

See [https://github.com/cuveland/ibtopviz](https://github.com/cuveland/ibtopviz)

#### ibmapviz.py

(Rewrite of ibtopviz, with more options, colors, speeds, to suits Boss needs.)

Create a colored infiniband map (graphviz DOT format). Usefull to spot cabling problems. See dedicated README (README-[en|fr]-ibmapviz.rst).

### SIDUS

We use [SIDUS](http://www.cbp.ens-lyon.fr/doku.php?id=developpement:productions:sidus) as our main boot/managment system for compute nodes.

#### add new hosts

two script used to add batch of hosts to general config(s). First, use `add_newhosts.py`, then `add-newhosts-03-pxelinks.sh`

#### get_ipmitool.py & plot_metrology.py

two scripts to get data from ipmitool, save in CSV file, then plot. Usefull when a node may have problem(s) (T°C, power consumption, memory fault, fans, ...)

#### get_serial.py

get serial number from host(s). For maintenance contracts purposes.

### Filers

Some little scripts used on our servers.

#### du_labs.sh

follow homes space consumption on data servers.

## More to come...
