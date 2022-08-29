(data-groups)=

# Organising your data

In this module of the tutorial we will focus on how to organise the data in an AiiDA database.
To explain these concepts, we will be importing and using the information of an external pre-existing database.
Start by importing the archive that contains this data using the following CLI command:

```{code-block} console
$ verdi archive import https://object.cscs.ch/v1/AUTH_b1d80408b3d340db9f03d373bbde5c1e/marvel-vms/tutorials/aiida_tutorial_2022_10_perovskites_main_0001.aiida
```

:::{note}

This command can take some time to complete on the AiiDAlab JupyterHub cluster.
This is perfectly normal, just have a ☕️ and start reading the hands-on while AiiDA is importing the data.

:::

## How to group nodes

AiiDA's database is great for automatically storing all your data, but sometimes it can be tricky to navigate this flat data store.
To create some order in this mass of data, you can *group* sets of nodes together, just as you would with files in folders on your filesystem.
Each group instance can hold any amount of nodes and any node can be contained in any number of groups.
A typical use case is to store all nodes that share a common property in a single group.

### Listing existing groups

Let's explore the groups already present in the imported archive, by executing the following command:

```{code-block} console
$ verdi group list -a -A
PK    Label            Type string    User
----  ---------------  -------------  ---------------
(...)
   1  tutorial_pbesol  core           aiida@localhost
   2  tutorial_lda     core           aiida@localhost
   3  tutorial_pbe     core           aiida@localhost
   4  GBRV_pbe         core.upf       aiida@localhost
   5  GBRV_pbesol      core.upf       aiida@localhost
   6  GBRV_lda         core.upf       aiida@localhost
   7  20200705-071658  core.import    aiida@localhost
```

:::{important}

Similar to the _node_ PKs, the _group_ PKs in the examples will differ from those in your database.

:::

The default table shows us four pieces of information:

* **PK**: The Primary Key of the group.
* **Label**: The label by which the group can be identified.
* **Type string**: This tells us what type of group this is.
* **User**: The email of the user that created this group.

:::{tip}

The `-a` and `-A` flags used above ensure that groups for *all* type strings and users are shown, respectively.

:::

You can then inspect the content of a group by its label (if it is unique) or the PK:

```{code-block} console
$ verdi group show tutorial_pbesol
-----------------  ----------------
Group label        tutorial_pbesol
Group type_string  core
Group description  <no description>
-----------------  ----------------
# Nodes:
PK    Type         Created
----  -----------  -----------------
 380  CalcJobNode  2078D:17h:46m ago
1273  CalcJobNode  2078D:18h:03m ago
...
```

Conversely, if you want to see all the groups a node belongs to, you can use its PK and run, (where `<PK>` should be the PK of the node):

```{code-block} console
$ verdi group list -a -A --node <PK>
PK    Label            Type string    User
----  ---------------  -------------  ---------------
   1  tutorial_pbesol  core           aiida@localhost
   7  20200705-071658  core.import    aiida@localhost
```

### Creating and manipulating groups

Let's make a new group:

```{code-block} console
$ verdi group create a_group
Success: Group created with PK = 8 and name 'a_group'
```

You can change the name of a group using the `verdi group relabel` command:

```{code-block} console
$ verdi group relabel a_group my_group
Success: Label changed to my_group
```

Add one or more nodes to your new group using node PKs from the `tutorial_pbesol` group we inspected earlier:

```{code-block} console
$ verdi group add-nodes -G my_group 380 1273
Do you really want to add 2 nodes to Group<my_group>? [y/N]: y
```

You can also copy *all* nodes from an existing group to another group using:

```{code-block} console
$ verdi group copy tutorial_pbesol my_group
Warning: Destination group<my_group> already exists and is not empty.
Do you wish to continue anyway? [y/N]: y
Success: Nodes copied from group<tutorial_pbesol> to group<my_group>
```

Double check that the nodes have been added to your new group:

```{code-block} console
$ verdi group show my_group
-----------------  ----------------
Group label        my_group
Group type_string  core
Group description  <no description>
-----------------  ----------------
# Nodes:
PK    Type         Created
----  -----------  -----------------
74  CalcJobNode  2078D:17h:51m ago
76  CalcJobNode  2078D:17h:57m ago
...
```

Removing nodes from the group is similar to adding them, try:

```{code-block} console
$ verdi group remove-nodes -G my_group <PK>
Do you really want to remove 1 nodes from Group<my_group>? [y/N]: y
```

and finally to remove the group entirely:

```{code-block} console
$ verdi group delete my_group
Are you sure to delete Group<my_group>? [y/N]: y
Success: Group<my_group> deleted.
```

:::{important}

Any deletion operation related to groups will not affect the nodes themselves.
For example if you delete a group, the nodes that belonged to the group will remain in the database.
The same happens if you remove nodes from the group -- they will remain in the database but won't belong to the group any more.

:::

## Organising groups in hierarchies

Earlier we mentioned that groups are like files in folders on your filesystem.
Similar to folders and sub-folders, you may wish to structure your groups in a hierarchy once the number of groups in your database grows larger.
Groups in AiiDA are inherently "flat", meaning groups may only contain nodes and not other groups.
However, it is possible to construct *virtual* group hierarchies based on delimited group labels, using the `grouppath` utility.

Like folder paths on Unix systems, `grouppath` requires delimitation by forward slash (`/`) characters.
Let's copy and rename the three tutorial groups:

```{code-block} console
$ verdi group copy tutorial_lda tutorial/lda/basic
$ verdi group copy tutorial_pbe tutorial/gga/pbe
$ verdi group copy tutorial_pbesol tutorial/gga/pbesol
```

You can now list the groups in a new way:

```{code-block} console
$ verdi group path ls -l
Path             Sub-Groups
---------------  ------------
tutorial                    3
tutorial_lda                0
tutorial_pbe                0
tutorial_pbesol             0
```

:::{note}

In the terminal, paths that contain nodes are listed in bold.

:::

You can see that the actual groups we just created do not appear, only the initial part of the path (`tutorial`), and how many subgroups that path contains.
You can then step into a path:

```{code-block} console
$ verdi group path ls -l tutorial
Path          Sub-Groups
------------  ------------
tutorial/gga             2
tutorial/lda             1
```

This feature is also particularly useful in the `verdi shell`:

```{code-block} ipython
In [1]: from aiida.tools.groups import GroupPath
In [2]: for subpath in GroupPath("tutorial/gga").walk(return_virtual=False):
   ...:     print(subpath.get_group())
   ...:
Group<tutorial/gga/pbe>
Group<tutorial/gga/pbesol>
```

:::{seealso}

Please see the {ref}`corresponding section in the documentation <aiida:how-to:data:organize>` for more details on groups and how to use them.

:::

## Cleaning up

Before moving on to the next module, let's clean up these duplicated group paths:

```{code-block} console
$ verdi group delete  -f tutorial/lda/basic
$ verdi group delete  -f tutorial/gga/pbe
$ verdi group delete  -f tutorial/gga/pbesol
```
