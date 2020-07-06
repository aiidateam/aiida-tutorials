.. _2020_virtual_intro:data:

*******************************************
Working with data and querying your results
*******************************************

In this section of the tutorial we will focus on how to organise and explore the data you hopefully have now generated from running some computations.

This section has been written using an AiiDA profile populated with the data from :download:`this archive <../archives/tutorial_perovskites_v0.1.aiida>`.
To follow the tutorial then, you can use the profile that you have already using for the previous sections, or you may wish to try creating a new profile and importing the archive:

.. code-block:: console

   $ verdi quicksetup --profile data
   $ verdi profile setdefault data
   $ verdi import --migration <FILE_OR_URL>

where the ``FILE_OR_URL`` can be the local path where you have placed the archive (on you virtual machine) or the URL to the file source on GitHub, e.g. ``https://github.com/aiidateam/aiida-tutorials/raw/master/docs/pages/2020_Intro_Week/archives/tutorial_perovskites_v0.1.aiida``.


How to group nodes
------------------

AiiDA's database is great for automatically storing all your data, but sometimes it can be tricky to navigate this flat data store.
To create some order in this mass of data, you can *group* sets of nodes together, just as you would with files in folders on your filesystem.
Each group instance can hold any amount of nodes and any node can be contained in any number of groups.
A typical use case is to store all nodes that share a common property in a single group.

Listing existing groups
^^^^^^^^^^^^^^^^^^^^^^^

Lets explore the groups already present in the imported archive:

.. code-block:: console

   $ verdi group list -a -A
   PK  Label            Type string    User
   ----  ---------------  -------------  ---------------
      1  tutorial_pbesol  core           aiida@localhost
      2  tutorial_lda     core           aiida@localhost
      3  tutorial_pbe     core           aiida@localhost
      4  GBRV_pbe         core.upf       aiida@localhost
      5  GBRV_pbesol      core.upf       aiida@localhost
      6  GBRV_lda         core.upf       aiida@localhost
      7  20200705-071658  core.import    aiida@localhost

The default table shows us four pieces of information:

PK
   The Primary Key of the group
Label
   The label by which the group has been named
Type string
   This tells us the what "sub-class" of group this is.
   Type strings can be used to class certain types of data, for example here we have general groups (core), groups containing pseudopotentials (core.upf), and an auto-generated group containing the nodes we imported from the archive (core.import).
   For advanced use, you can create your own group subclass plugins, with specialised methods. 
User
   The email of the user that created this group.

.. tip::

   The ``-a`` and ``-A`` flags we used above ensure that groups for all type strings and users are shown respectively.

We can then inspect a groups contents, by the label (if it is unique) or the PK:

.. code-block:: console

   $ verdi group show tutorial_pbesol
   -----------------  ----------------
   Group label        tutorial_pbesol
   Group type_string  core
   Group description  <no description>
   -----------------  ----------------
   # Nodes:
   PK  Type         Created
   ----  -----------  -----------------
   1149  CalcJobNode  2077D:13h:38m ago
   1404  CalcJobNode  2077D:13h:38m ago
   ...

Conversely, if you want to see all the groups a node belongs to, you can run:

.. code-block:: console

   $ verdi group list -a -A --node 1149
   PK  Label            Type string    User
   ----  ---------------  -------------  ---------------
      1  tutorial_pbesol  core           aiida@localhost
      7  20200705-071658  core.import    aiida@localhost

Creating and manipulating groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Lets make a new group:

.. code-block:: console

   $ verdi group create a_group
   Success: Group created with PK = 8 and name 'a_group'

If we want to change the name of the group at any time:

.. code-block:: console

   $ verdi group relabel a_group my_group
   Success: Label changed to my_group

Now we can add one or more nodes to it:

.. code-block:: console

   $ verdi group add-nodes -G my_group 1149 1404
   Do you really want to add 2 nodes to Group<my_group>? [y/N]: y

We can also copy the nodes from an existing group to another group:

.. code-block:: console

   $ verdi group copy tutorial_pbesol my_group
   Warning: Destination group<my_group> already exists and is not empty.
   Do you wish to continue anyway? [y/N]: y
   Success: Nodes copied from group<tutorial_pbesol> to group<my_group>
   $ verdi group show my_group
   -----------------  ----------------
   Group label        my_group
   Group type_string  core
   Group description  <no description>
   -----------------  ----------------
   # Nodes:
   PK  Type         Created
   ----  -----------  -----------------
   35  CalcJobNode  2077D:13h:53m ago
   87  CalcJobNode  2076D:22h:48m ago
   ...

To remove nodes from the group run:

.. code-block:: console

   $ verdi group remove-nodes -G my_group 1149
   Do you really want to remove 1 nodes from Group<my_group>? [y/N]: y

and finally to remove the group entirely:

.. code-block:: console

   $ verdi group delete --clear my_group
   Are you sure to delete Group<my_group>? [y/N]: y
   Success: Group<my_group> deleted.

.. important::

   Any deletion operation related to groups won't affect the nodes themselves.
   For example if you delete a group, the nodes that belonged to the group will remain in the database.
   The same happens if you remove nodes from the group -- they will remain in the database but won't belong to the group any more.

Organising groups in hierarchies
--------------------------------

Earlier we mentioned that groups are like files in folders on your filesystem.
As with folders and sub-folders then, as the amount of groups we have grows, we may also wish to structure our groups in a hierarchy. 
Groups in AiiDA are inherently "flat", in that groups may only contain nodes and not other groups.
However it is possible to construct *virtual* group hierarchies based on delimited group labels, using the ``grouppath`` utility.

Like folder paths grouppath requires delimitation by `/` characters.
Lets copy and rename the three tutorial groups:

.. code-block:: console

   $ verdi group copy tutorial_lda tutorial/lda/basic
   $ verdi group copy tutorial_pbe tutorial/gga/pbe
   $ verdi group copy tutorial_pbesol tutorial/gga/pbesol

We can now list the groups in a new way:

.. code-block:: console

   $ verdi group path ls -l
   Path               Sub-Groups
   ---------------  ------------
   tutorial                    3
   tutorial_lda                0
   tutorial_pbe                0
   tutorial_pbesol             0

.. note::

   In the terminal, paths that contain nodes are listed in bold

You can see that the actual groups that we create do not show, only the initial part of the "path", and how many sub-groups that path contains.
We can then step into a path:

.. code-block:: console

   $ verdi group path ls -l tutorial
   Path            Sub-Groups
   ------------  ------------
   tutorial/gga             2
   tutorial/lda             1

This feature is also particularly useful in the verdi shell:

.. code-block:: ipython

   In [1]: from aiida.tools.groups import GroupPath
   In [2]: for subpath in GroupPath("tutorial/gga").walk(return_virtual=False):
      ...:     print(subpath.get_group())
      ...:
   "tutorial/gga/pbesol" [type core], of user aiida@localhost
   "tutorial/gga/pbe" [type core], of user aiida@localhost

.. seealso::

   Please see the :ref:`corresponding section in the documentation <aiida:how-to:data:organize>` for more details on groups and how to use them.

Querying for data
-----------------

This part of the tutorial is provided only in interactive mode through a Jupyter notebook, which you will be able to run in your browser.
For instructions on starting the Jupyter server, please refer to the :ref:`setup section<2020_virtual_intro:setup:jupyter>`.
Once the server is running, :jupyter-download:nb:`download this tutorial notebook <../notebooks/querybuilder-tutorial>` and open it in Jupyter.
For instructions on downloading these files on a machine through which you are connected through SSH, refer to :ref:`this section<2020_virtual_intro:setup:downloading_files>`.

The notebook will show you how the ``QueryBuilder`` can be used to query your
database for specific data. It will demonstrate certain concepts and then ask
you to use those to perform certain queries on your own database. Some of these
question cells will have partial solutions that you will have to complete.

Once you have finished the notebook, you can download a
:download:`notebook with the solutions <../notebooks/querybuilder-solutions.ipynb>`
but try not to use them at first!

See below for a rendered version of the notebook:

.. toctree::

   QueryBuilder Notebook <../notebooks/querybuilder-tutorial>
