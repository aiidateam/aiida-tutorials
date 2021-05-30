(matsci-kpoints)=

# `KpointsData`

A set of k-points in the Brillouin zone is represented by an instance of the `KpointsData` class.
Look for an identifier (PK or UUID) of the `KpointsData` input node of the `PwCalculation` whose provenance graph you generated earlier, and load the node in the `verdi shell`:

```{code-block} ipython

In [1]: kpoints = load_node(<IDENTIFIER>)

```

You can get the k-points mesh using:

```{code-block} ipython

In [2]: kpoints.get_kpoints_mesh()
Out[2]: ([6, 6, 6], [0.0, 0.0, 0.0])

```

To get the full (explicit) list of k-points belonging to this mesh, use:

```{code-block} ipython

In [3]: kpoints.get_kpoints_mesh(print_list=True)
Out[3]:
array([[0.        , 0.        , 0.        ],
       [0.        , 0.        , 0.16666667],
       ...
       [0.83333333, 0.83333333, 0.66666667],
       [0.83333333, 0.83333333, 0.83333333]])

```

If this throws an `AttributeError`, it means that the kpoints instance does not represent a regular mesh but rather a list of k-points defined by their crystal coordinates (typically used when plotting a band structure).
In this case, get the list of k-points coordinates using

```{code-block} ipython

In [3]: kpoints.get_kpoints()

```

Conversely, if the `KpointsData` node *does* actually represent a mesh, this method is the one, that when called, will throw an `AttributeError`.

If you prefer Cartesian (rather than fractional) coordinates, type:

```{code-block} ipython

In [4]: kpoints.get_kpoints(cartesian=True)

```

For later use in this tutorial, let us try now to create a k-points instance, to describe a regular (2 x 2 x 2) mesh of k-points, centered at the Gamma point (i.e. without offset).
This can be done with the following set of commands:

```{code-block} ipython

In [5]: KpointsData = DataFactory('array.kpoints')
   ...: kpoints = KpointsData()
   ...: kpoints.set_kpoints_mesh([2, 2, 2])

```

Here, we first load the `KpointsData` class using the `DataFactory` and the entry point (`array.kpoints`).
Then, we create an instance of the `KpointData` class, and use the `set_kpoints_mesh()` method to set the mesh to a regular 2x2x2 Gamma-point centered mesh.
