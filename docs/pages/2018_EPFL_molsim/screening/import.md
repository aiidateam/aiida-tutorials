Import the structures
=====================

You can download a tar file containing the structures from

```console
$ wget {{ "/assets/2018_EPFL_molsim/mof_structures.tar.gz" | absolute_url }} 
$ tar -xf mof_structures.tar.gz
```

-   Visualize a few structures using `jmol`:

    ```console
    $ cd struct/
    $ jmol <structure>.cif
    ```

    Can you think of two criteria for a high deliverable methane
    capacity?

-   Use the `CifData` class to import the structures into your database,
    e.g.

    ```python
    CifData = DataFactory('cif') 
    cif = CifData(file='/path/to/file.cif')
    cif.store()
    ```

-   Use wildcards with the `glob` and `os` modules to get the file paths
    of all structures like so:

    ```python
    from glob import glob 
    from os import path 
    all_structure_files = glob(path.abspath("/path/to/struct/*"))
    ```

-   Keep track of your structures using groups

    ```python
    # Use get_or_create to be able to run this multiple times mofs,
    created = Group.get_or_create(name='mofs') 
    mofs.add_nodes([cif1, cif2])
    ```

-   Finally, you can load your structures from the group using the
    [AiiDA query builder](http://aiida-core.readthedocs.io/en/latest/querying/querybuilder/usage.html)

    ```python
    qb = QueryBuilder() 
    qb.append(Group, filters = { 'name':'mofs' }) 
    mofs = qb.one()[0]

    for cif in mofs.nodes: 
        print cif
    ```


