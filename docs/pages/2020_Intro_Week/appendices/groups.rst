.. _2020_virtual_intro:groups:

*********************
AiiDA groups of nodes
*********************

In AiiDA, calculations (and more generally nodes) can be organized in groups, which are particularly useful to organise your data, and assign a set of calculations or data to a common subproject.
This allows you to have quick access to a whole set of calculations with no need for tedious browsing of the database or writing complex scripts for retrieving the desired nodes.
Type in the terminal:

.. code-block:: console

    $ verdi group list -a -A

to show a list of all groups that exist in the database.
Choose the PK of the group named ``tutorial_pbesol`` and look at the calculations that it contains by typing:

.. code-block:: console

    $ verdi group show <IDENTIFIER>

In this case, we have used the name of the group to organize calculations according to the pseudopotential that has been used to perform them.
Among the rows printed by the last command you will be able to find the calculation we have been inspecting until now.

If, instead, you want to know all the groups to which a specific node belongs, you can run:

.. code-block:: console

    $ verdi group list -N/--node <IDENTIFIER>
