# Retrieve tutorial data

If you wish to retrieve the data from your tutorial cloud machine, you can follow these steps:

Note, these steps needs to be done for each AiiDA profile you wish to retrieve data from.
In the following, I will be showing it using the profile `TUTORIAL_PROFILE`.

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

The last part may take a while, a progress bar should help you see that stuff is going on.

## Download exported archive

Note down the path to your new export archive `my_tutorial_nodes.aiida`.
In the following, I use the path: `/home/max/my_tutorial_nodes.aiida`.

First, open a new terminal on your local machine.
Either `cd` into the path you wish to store the export archive or note down the path.
In the following, I use the path: `/path/to/archive/`.
But if you are running the command from the path you wish to store the export archive, you could use `./` instead of `/path/to/archive/`.

```console
$ scp aiidatutorial:/home/max/my_tutorial_nodes.aiida /path/to/archive/
my_tutorial_nodes.aiida ...
```

## Import exported archive in your local AiiDA installation

For the last part, you can import the AiiDA archive like you have done all other archives during the tutorial, using `verdi import`:

```console
$ verdi -p LOCAL_PROFILE import /path/to/archive/my_tutorial_nodes.aiida
Info: importing archive /path/to/archive/my_tutorial_nodes.aiida
...
```

Note, I am using the profile `LOCAL_PROFILE` here, this should be updated with the profile you wish to import the data into.

If you're currently in the folder where `my_tutorial_nodes.aiida` resides, you can leave out the path and just write `verdi -p LOCAL_PROFILE import my_tutorial_nodes.aiida`.

## Success

That should be it!

You should have now successfully retrieved the complete database of the AiiDA profile `TUTORIAL_PROFILE` on your `aiidatutorial` host and imported it into your local AiiDA profile `LOCAL_PROFILE`.
