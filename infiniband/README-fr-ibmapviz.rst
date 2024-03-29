=============================
plan couleurs pour InfiniBand
=============================


Permet de repérer les câbles défectueux, les erreurs de câblage, etc.

Pré-requis :

.. code-block:: bash

    apt install graphviz


.. code-block:: bash

    python3 -m pip install ClusterShell execo


génération des fichiers d'input
===============================


fichier de topology infiniband
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sur un noeud de l'arbre infiniband (n'importe lequel).

.. code-block:: bash

    ibnetdiscover > $cluster.topofile


fichier map hostname (optionnel)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(association GUID infiniband <-> hostname)

Sur une machine ayant accés à tous les noeuds du cluster, en ssh (utilise execo).

.. code-block:: bash

    python3 map_GUID.py @clusternodes >> $cluster.map


Ce qui donne, exemple :

.. code-block:: bash

    H-0002c90300080d28 r510gluster4
    H-78e7d10300227744 sl390lin1
    H-78e7d103002276bc sl390lin2
    H-78e7d1030022a0dc sl390lin3


fichier de spine (optionnel)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour différencier les switchs de niveau 0 (ou d'épine dorsale en langue perfide), des switchs de niveau 1 (feuilles).

Repérer les GUID de switchs, dans le $cluster.topofile, qui ne sont connectés qu'a d'autres switchs.

Créer un fichier '$cluster.spine' qui contient juste les GUID, un par ligne. Exemple :

.. code-block:: bash

    S-0002c903007d9440
    S-0002c90300674430
    ...


Génération de la carte infiniband
=================================


.. code-block:: bash

    python3 ibmapviz.py [-d, -h] [-m $cluster.map] [-s $cluster.spine] [-o $cluster.dot] $cluster.topofile


"Et voilà !"

Visualisation directe avec xdot : ``xdot -f [dot, neato, twopi, circo, fdp] $cluster.dot``

Génération d'un fichier pdf (parfois plus lisible) : ``neato -Goverlap=false -Tpdf $cluster.dot -o $cluster.pdf``

dot, neato, twopi, circo et fdp sont des commandes qui viennent avec graphviz. Ce sont différent algorithmes de ''placement/routage''. Ils ont tous leurs avantages et inconvénients. Il faut essayer.

Exemples
========

Voir les fichiers ``X5`` dans le dépôt (cluster X5 du PSMN).
