========================
Color map for InfiniBand
========================


Meant to spot defectives cables, cabling errors, etc.

Requirements:

.. code-block:: bash

    apt install graphviz


.. code-block:: bash

    python3 -m pip install ClusterShell execo


Input files generation
======================


infiniband topology file
~~~~~~~~~~~~~~~~~~~~~~~~

On a node (server) from the infiniband tree (any of them).

.. code-block:: bash

    ibnetdiscover > $cluster.topofile


hostname map file (optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(GUID infiniband <-> hostname association )

On a server with SSH access to all of cluster's nodes (using execo python module).

.. code-block:: bash

    python3 map_GUID.py @clusternodes >> $cluster.map


Which gives, example:

.. code-block:: bash

    H-0002c90300080d28 r510gluster4
    H-78e7d10300227744 sl390lin1
    H-78e7d103002276bc sl390lin2
    H-78e7d1030022a0dc sl390lin3


spine file (optional)
~~~~~~~~~~~~~~~~~~~~~

Level 0 switches (known as 'spine' switchs), to differentiate them from the level 1 (leaf) switchs.

Manually edit ``$cluster.topofile``, search for switches only connected to switches, that's your spines.

Create a file ($cluster.spine, for example), which only contains GUID, one by line. For example:

.. code-block:: bash

    S-0002c903007d9440
    S-0002c90300674430
    ...


Color map generation
====================


.. code-block:: bash

    python3 ibmapviz.py [-d, -h] [-m $cluster.map] [-s $cluster.spine] [-o $cluster.dot] $cluster.topofile


"Et voilà!"

Direct visualization, with xdot: ``xdot -f [dot, neato, twopi, circo, fdp] $cluster.dot``

PDF file generation (often more legiable): ``neato -Goverlap=false -Tpdf $cluster.dot -o $cluster.pdf``

dot, neato, twopi, circo and fdp are graphviz commands. Theses are differents ''placement/routing'' algorithms. They all have their pros and cons. You'll have to try.

Examples
========

See ``X5`` files in repository (from X5 PSMN's cluster).

