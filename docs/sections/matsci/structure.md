
(matsci-structure)=

# Structures

Next, let's have a look at the `StructureData` node, which represents a crystalline structure.
We can consider for instance the input structure to the calculation we were considering before (it should have the UUID `3a4b1270`).
Such objects can be inspected interactively by means of an atomic viewer such as the one provided by `ase`.
AiiDA however supports several other viewers such as `xcrysden`, `jmol`, and `vmd`.
Type in the terminal:

```{code-block} console

$ verdi data structure show --format ase <IDENTIFIER>

```

to show the selected structure, although it will take a few seconds to appear (it has to go over a tunnel on your SSH connection).
You should be able to rotate the view with the right mouse button.

```{note}

If you receive some errors, make sure your X-forwarding settings have been set up correctly, as explained in (**TODO: FIX LINK**).

```

Alternatively, especially if showing them interactively is too slow over SSH, you can export the content of a structure node in various popular formats such as `xyz`, `xsf` or `cif`.
This is achieved by typing in the terminal:

```{code-block} console

$ verdi data structure export --format xsf <IDENTIFIER> > BaTiO3.xsf

```

This outputs the structure in `xsf` format and writes it to a file.

You can open the generated `xsf` file and observe the cell and the coordinates.
Then, you can then copy `BaTiO3.xsf` from the Amazon machine to your local one and then visualize it, e.g. with [xcrysden](<http://www.xcrysden.org>) (if you have it installed):

```{code-block} console

$ xcrysden --xsf BaTiO3.xsf

```

The `StructureData` node can also be investigated using the `verdi shell`.
First, open the `verdi shell` and load the structure node:

```{code-block} ipython

In [1]: structure = load_node('3a4b1270')
In [2]: structure
Out[2]: <StructureData: uuid: 3a4b1270-82bf-4d66-a51f-982294f6e1b3 (pk: 1161)>

```

You can display its chemical formula using:

```{code-block} ipython

In [3]: structure.get_formula()
Out[3]: 'BaO3Ti'

```

or, to obtain the atomic positions and species:

```{code-block} ipython

In [4]: structure.sites
Out[4]:
[<Site: kind name 'Ba' @ 0.0,1.78886419607596e-30,0.0>,
 <Site: kind name 'Ti' @ 1.98952035955311,1.98952035955311,1.98952035955311>,
 <Site: kind name 'O' @ 1.98952035955311,1.98952035955311,0.0>,
 <Site: kind name 'O' @ 1.98952035955311,2.33671938655715e-31,1.98952035955311>,
 <Site: kind name 'O' @ 0.0,1.98952035955311,1.98952035955311>]

```

If you are familiar with [ASE](<https://wiki.fysik.dtu.dk/ase/>) and [Pymatgen](<https://pymatgen.org/>), you can convert this structure to those formats by typing either

```{code-block} ipython

In [5]: structure.get_ase()
Out[5]: Atoms(symbols='BaTiO3', pbc=True, cell=[3.97904071910623, 3.97904071910623, 3.97904071910623], masses=...)

```

```{code-block} ipython

In [6]: structure.get_pymatgen()
Out[6]:
Structure Summary
Lattice
    abc : 3.97904071910623 3.97904071910623 3.97904071910623
 angles : 90.0 90.0 90.0
 volume : 62.999216807333035
      A : 3.97904071910623 0.0 0.0
      B : 0.0 3.97904071910623 0.0
      C : 0.0 0.0 3.97904071910623
PeriodicSite: Ba (0.0000, 0.0000, 0.0000) [0.0000, 0.0000, 0.0000]
PeriodicSite: Ti (1.9895, 1.9895, 1.9895) [0.5000, 0.5000, 0.5000]
PeriodicSite: O (1.9895, 1.9895, 0.0000) [0.5000, 0.5000, 0.0000]
PeriodicSite: O (1.9895, 0.0000, 1.9895) [0.5000, 0.0000, 0.5000]
PeriodicSite: O (0.0000, 1.9895, 1.9895) [0.0000, 0.5000, 0.5000]

```

Of course, the structure above is already in our database, after we imported it at the start of this section.
In order to add new structures to your AiiDA database, you can also define a structure by hand, or import it from an online repository:

```{dropdown} Defining a structure and storing it in the database

Let’s try now to define a new structure to study, specifically a silicon crystal.
In the `verdi shell`, define a cubic unit cell as a 3 x 3 matrix, with lattice parameter `alat` = 5.4 Å:

```{code-block} ipython

In [1]: alat = 5.4
    ...: unit_cell = [[alat/2, alat/2, 0.], [alat/2, 0., alat/2], [0., alat/2, alat/2]]

```

```{note}

Default units for crystal structure cell and coordinates in AiiDA are Å (Ångström).

```

In order to store a structure in the AiiDA database, we need to create an instance of the `StructureData` class.
We can load this class using the `DataFactory`:

```{code-block} ipython

In [2]: StructureData = DataFactory('structure')

```

Now, initialize the class instance using the unit cell you defined:

```{code-block} ipython

In [3]: structure = StructureData(cell=unit_cell)

```

From now on, you can access the cell with the command

```{code-block} ipython

In [4]: structure.cell
Out[4]: [[2.7, 2.7, 0.0], [2.7, 0.0, 2.7], [0.0, 2.7, 2.7]]

```

Of course, at this point we only have an empty unit cell.
So, let's append the 2 Si atoms to the crystal structure, starting with:

```{code-block} ipython

In [5]: structure.append_atom(position=(alat/4., alat/4., alat/4.), symbols="Si")

```

for the first ‘Si’ atom.
Repeat this command for the other Si site with coordinates (0, 0, 0).
You can access and inspect the structure sites by accessing the corresponding property:

```{code-block} ipython

In [6]: structure.sites
Out[6]: [<Site: kind name 'Si' @ 1.35,1.35,1.35>, <Site: kind name 'Si' @ 0.0,0.0,0.0>]

```

If you make a mistake, start over from
`structure = StructureData(cell=the_cell)`, or equivalently use `structure.clear_kinds()` to remove all kinds (atomic species) and sites.

Alternatively, AiiDA structures can also be converted directly from ASE structures [#f4]_ using

```{code-block} ipython

In [7]: from ase.spacegroup import crystal
    ...: ase_structure = crystal('Si', [(0, 0, 0)], spacegroup=227,
    ...:             cellpar=[alat, alat, alat, 90, 90, 90], primitive_cell=True)
    ...: structure = StructureData(ase=ase_structure)

```

Now you can store the new structure object in the database with the command:

```{code-block} ipython

In [8]: structure.store()

```

```{note}

Similarly, a ``StructureData`` instance can also be intialized from a pymatgen structure using ``StructureData(pymatgen=pmg_structure)``.

```

```

```{dropdown} Importing a structure from an online repository

Another way of obtaining the silicon structure is to import it from an external (online)
repository such as the [Crystallography Open Database (COD)](http://www.crystallography.net/cod/).
Try executing the following code snippet in the `verdi shell`:

```{code-block} python

from aiida.tools.dbimporters.plugins.cod import CodDbImporter
importer = CodDbImporter()
for entry in importer.query(formula='Si', spacegroup='F d -3 m'):
    structure = entry.get_aiida_structure()
    print("Formula:", structure.get_formula())
    print("Unit cell volume:", structure.get_cell_volume())
    print()

```

This will connect to the COD database on the web, perform the query for all entries with formula `Si` and space group `Fd-3m`, fetch the results and convert them to AiiDA StructureData objects.
In this case two structures exist for `Si` in COD and both are shown.
```
