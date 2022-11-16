
sinfo, squeue
-h -> no header
-o "%C" -> nb of cores == threads !!
-o "%Z" -> nb of threads / core
-o "%t" -> état short
-o "%T" -> état long
-o "%P" -> partition (with *)
-o "%R" -> partition (without *)

squeue
-p partition -> only this partition


squeue -h -o "%t %C" (état, cores=threads)

squeue -h -o "%T" (état)

for i in $(sinfo -h -o "%R");
do
    echo -n "slurm_cpus_run.${i}.value " ;
    squeue -h -p ${i} -o "%t %C" | awk 'BEGIN {s=0} /R/ {s+=($2/2)} END {printf "%g\n", s}' ;
done

actives users ?

-O UserName,StateCompact
-u $USER 
-t r

 
