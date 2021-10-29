======================================
Génération du topology.conf pour slurm
======================================

Permet de générer tout ou partie du fichier ``topology.conf`` pour slurm.

Pré-requis :

.. code-block:: bash

    python3 -m pip install ClusterShell execo

génération des fichiers d'input
===============================


fichier de topology infiniband
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sur un noeud de l'arbre infiniband (n'importe lequel).

.. code-block:: bash

    ibnetdiscover > ibtopofile.$cluster


fichier map hostname (optionnel)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(association GUID infiniband <-> hostname)

Sur une machine ayant accés à tous les noeuds du cluster, en ssh (utilise execo).

.. code-block:: bash

    python3 map_GUID.py @clusternodes >> map.$cluster


Ce qui donne, exemple :

.. code-block:: bash

    H-0002c90300080d28 r510gluster4
    H-78e7d10300227744 sl390lin1
    H-78e7d103002276bc sl390lin2
    H-78e7d1030022a0dc sl390lin3


fichier de spine (optionnel)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour différencier les switches de niveau 0 (ou d'épine dorsale en langue perfide), des switchs de niveau 1 (feuilles).

Repérer les GUID de switches, dans le ibtopofile.$cluster, qui ne sont connectés qu'a d'autres switchs.

Créer un fichier 'spine.$cluster' qui contient juste les GUID, un par ligne. Exemple :

.. code-block:: bash

    S-0002c903007d9440
    S-0002c90300674430
    ...

Génération des snippets topology.conf
=====================================

.. code-block:: bash

    python3 ibmap2slurm.py [-d, -h] [-m map.$cluster] [-s spine.$cluster] [-o $file] ibtopofile.$cluster

"Et voilà !"

Vérifiez et propagez sur vos clusters.
