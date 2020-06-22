# HPC toolset

PSMN HPC tools for everyday sysadmin

## usefull tools

- [ClusterSSH](https://github.com/duncs/clusterssh)

- [ClusterShell](https://github.com/cea-hpc/clustershell) python module, with 
  NodeSet, from CEA

- [execo](http://execo.gforge.inria.fr/doc/latest-stable/) python module, from 
  INRIA, also [execo-g5k-tools](https://github.com/lpouillo/execo-g5k-tools)

- [shellcheck](https://github.com/koalaman/shellcheck) linter for bash scripts

- [milkcheck](https://github.com/cea-hpc/milkcheck) ansible/salt-like from CEA

## other tools

### ask_infiniband.py

build a CSV list, from cluster's nodes, of firmware revisions and PSIDs, when 
upgrade time as come... Ease the choice of firmware images for download and burn.

### map_GUID.py

Create a 'GUID hostname' map file, for use with Infiniband topological tools.

See [https://github.com/cuveland/ibtopviz](https://github.com/cuveland/ibtopviz)

### ibmapviz.py

(Rewrite of ibtopviz, with more options, colors, speeds, to suits Boss needs.)

Create a colored infiniband map (graphviz DOT format). Usefull to spot cabling problems. See dedicated README.

### add_newhosts

two script used to add batch of hosts to general config(s).

### get_ipmitool.py & plot_metrology.py

two scripts to get data from ipmitool, save in CSV file, then plot. Usefull when a node may have problem(s) (T°C, power consumption, memory fault, fans, ...)

## More to come...
