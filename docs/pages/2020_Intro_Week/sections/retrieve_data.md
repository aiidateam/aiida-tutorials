# Retrieving tutorial data

If you wish to retrieve the data which you have generated on your tutorial cloud machine, you can follow the steps below.

Note, these steps needs to be done for each AiiDA profile you wish to retrieve data from.
In the following sections, we will be demonstrating this using the profile `TUTORIAL_PROFILE`.

```{important}
Shortly after the tutorial has ended we shall terminate your virtual machine, at which point the data will be irretrievable!
```

## Save all Nodes in a Group and export

First, we store all Nodes from a profile into a Group for easy exporting:

```console
$ verdi -p TUTORIAL_PROFILE shell
Python 3.6.9 ...
```

```ipython
In[1]: nodes = QueryBuilder().append(Node).all(flat=True)

In[2]: all_nodes = Group("all_nodes").store()

In[3]: all_nodes.add_nodes(nodes)

In[4]: !verdi -p TUTORIAL_PROFILE export create -G {all_nodes.pk} -- my_tutorial_nodes.aiida
EXPORT
--------------  -----------------------
Archive         my_tutorial_nodes.aiida
Format          Zip (compressed)
Export version  0.9

Inclusion rules
-----------------  ----
...
```

The final stage of this process may take a number of minutes, at which time there is a progress bar to track the status of the export.

You will now have a new export archive `my_tutorial_nodes.aiida` in your current path.
Note down this path, for example below we use the path: `/home/max/my_tutorial_nodes.aiida`.

## Download exported archive

Open a new terminal on your local machine, then you can run the following:

```console
$ scp aiidatutorial:/home/max/my_tutorial_nodes.aiida /path/to/archive/
my_tutorial_nodes.aiida ...
```

where `/path/to/archive/` will be the path on your local machine where you want to download the archive to.
Or you can `cd` to this path and instead use `./`.

## Import exported archive in your local AiiDA installation

You can now import the AiiDA archive like you have done all other archives during the tutorial, using `verdi import`:

```console
$ verdi -p LOCAL_PROFILE import /path/to/archive/my_tutorial_nodes.aiida
Info: importing archive /path/to/archive/my_tutorial_nodes.aiida
...
```

Note, I we are using the profile `LOCAL_PROFILE` here, this should be updated with the profile you wish to import the data into.

If you are currently in the folder where `my_tutorial_nodes.aiida` resides, you can leave out the path and just use `verdi -p LOCAL_PROFILE import my_tutorial_nodes.aiida`.

## Success

You should have now successfully retrieved the complete database of the AiiDA profile `TUTORIAL_PROFILE` on your `aiidatutorial` host and imported it into your local AiiDA profile `LOCAL_PROFILE`.
