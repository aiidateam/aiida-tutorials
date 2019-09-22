Verdi shell and AiiDA objects
=============================

In this section we will use an interactive IPython environment with all the
basic AiiDA classes already loaded. We propose two realizations of such a
tool. The first consists of a special IPython shell where all the AiiDA
classes, methods and functions are accessible. Type in the terminal

.. code:: bash

    verdi shell

For all the everyday AiiDA-based operations, i.e. creating, querying, and
using AiiDA objects, the ``verdi shell`` is probably the best tool. In this
case, we suggest that you use two terminals, one for the ``verdi shell`` and
one to execute bash commands.

The second option is based on Jupyter notebooks and is probably most suitable
to the purposes of our tutorial. Go to the browser where you have opened
``jupyter`` and click ``New`` → ``Python 3`` (top right corner). This will
open an IPython-based Jupyter notebook, made of cells in which you can type
portions of python code. The code will not be executed until you press
``Shift+Enter`` from within a cell. Type in the first cell

.. code:: ipython

    %aiida

and execute it. This will set exactly the same environment as the
``verdi shell``. The notebook will be automatically saved upon any
modification and when you think you are done, you can export your notebook in
many formats by going to ``File`` → ``Download as``. We suggest you to have a
look at the drop-down menus ``Insert`` and ``Cell`` where you will find the
main commands to manage the cells of your notebook.

.. note::

    The ``verdi shell`` and Jupyter
    notebook are completely equivalent. Use either according to your
    personal preference.

You will still sometimes need to type command-line instructions in ``bash`` in
the first terminal you opened. To differentiate these from the commands to be
typed in the ``verdi shell``, the latter will be marked in this document by a
green background, like:

.. code:: python

    some verdi shell command

while command-line instructions in ``bash`` to be typed into a terminal will
be written with a blue background:

.. code:: bash

    some bash command

Alternatively, to avoid changing terminal, you can execute ``bash`` commands
within the ``verdi shell`` or the notebook by adding an exclamation mark before
the command itself:

.. code:: ipython

    !some bash command

.. _2019_sintef_loadnode:

Loading a node
--------------

Most AiiDA objects are represented by nodes, identified in the database by its
``PK`` (an integer). You can access a node using the following command
in the shell:

.. code:: python

    node = load_node(PK)

Load a node using one of the calculation ``PK`` s visible in the graph you
displayed in the previous section of the tutorial. Then get the energy of the
calculation with the command

.. code:: python

    node.res.energy

You can also type

.. code:: python

    node.res.

and then press ``TAB`` to see all the available output results of the
calculation.

Loading specific kinds of nodes
-------------------------------

Pseudopotentials
~~~~~~~~~~~~~~~~

From the graph you generated in  section :ref:`2019_sintef_aiidagraph`,
find the ``PK`` of the pseudopotential file (LDA). Load it and
show what elements it corresponds to by typing:

.. code:: python

    upf = load_node(PK)
    upf.element

All methods of ``UpfData`` are accessible by typing ``upf.`` and then pressing ``TAB``.

k-points
~~~~~~~~

A set of k-points in the Brillouin zone is represented by an instance of the
``KpointsData`` class. Choose one from the graph of
produced in section :ref:`2019_sintef_aiidagraph`,
load it as ``kpoints`` and inspect its content:

.. code:: python

    kpoints.get_kpoints_mesh()

Then get the full (explicit) list of k-points belonging to this mesh using

.. code:: python

    kpoints.get_kpoints_mesh(print_list=True)

If this throws an ``AttributeError``, it means that the kpoints instance does not represent a regular mesh but rather a list of k-points defined by their crystal coordinates (typically used when plotting a band structure).
In this case, get the list of k-points coordinates using

.. code:: python

    kpoints.get_kpoints()

Conversely, if the `KpointsData` node `does` actually represent a mesh, this method is the one, that when called, will throw an ``AttributeError``.

If you prefer Cartesian (rather than crystal) coordinates, type

.. code:: python

    kpoints.get_kpoints(cartesian=True)

For later use in this tutorial, let us try now to create a kpoints instance,
to describe a regular (2 x 2 x 2) mesh of k-points, centered at the Gamma
point (i.e. without offset). This can be done with the following commands:

.. code:: python

    KpointsData = DataFactory('array.kpoints')
    kpoints = KpointsData()
    kpoints_mesh = 2
    kpoints.set_kpoints_mesh([kpoints_mesh] * 3)
    kpoints.store()

This function loads the appropriate class defined in a string (here
``array.kpoints``). Therefore, ``KpointsData`` is not a class instance, but
the kpoints class itself!

While it is also possible to import ``KpointsData`` directly, it is recommended
to use the ``DataFactory`` function instead, as this is more future-proof:
even if the import path of the class changes in the future, its entry point
string (``array.kpoints``) will remain stable.

Parameters
~~~~~~~~~~

Dictionaries with various parameters are represented in AiiDA by ``Dict`` nodes.
Get the PK and load the input parameters of a calculation in the graph produced in  section :ref:`2019_sintef_aiidagraph`.
Then display its content by typing

.. code:: python

    params = load_node('<IDENTIFIER>')
    YOUR_DICT = params.get_dict()
    YOUR_DICT

Modify the python dictionary ``YOUR_DICT`` so that the wave-function cutoff is now set to 20
Ry. Note that you cannot modify an object already stored in the database. To
write the modified dictionary to the database, create a new object of class ``Dict``:

.. code:: python

    Dict = DataFactory('dict')
    new_params = Dict(dict=YOUR_DICT)

where ``YOUR_DICT`` is the modified python dictionary.
Note that ``new_params`` is not yet stored in the database.
In fact, typing ``new_params`` in the verdi shell will print a string notifying you of its 'unstored' status.
Let's finish by storing the ``new_params`` dictionary node in the datbase:

.. code:: python

    new_params.store()

Structures
~~~~~~~~~~

Find a structure in the graph you generated in section :ref:`2019_sintef_aiidagraph` and load it.
Display its chemical formula, atomic positions and species using

.. code:: python

    structure.get_formula()
    structure.sites

where ``structure`` is the structure you loaded. If you are familiar with ASE
and PYMATGEN, you can convert this structure to those formats by typing

.. code:: python

    structure.get_ase()
    structure.get_pymatgen()

Let’s try now to define a new structure to study, specifically a silicon
crystal. In the ``verdi shell``, define a cubic unit cell as a 3 x 3 matrix,
with lattice parameter `a`\ :sub:`lat`\ `= 5.4` Å:

.. code:: python

    alat = 5.4
    the_cell = [[alat/2, alat/2, 0.], [alat/2, 0., alat/2], [0., alat/2, alat/2]]

.. note::

    Default units for crystal structure cell and coordinates in AiiDA are Å (Ångström).

Structures in AiiDA are instances of the class ``StructureData``: load it in the
verdi shell

.. code:: python

    StructureData = DataFactory('structure')

Now, initialize the class instance (i.e. the actual structure we want to study) by
the command

.. code:: python

    structure = StructureData(cell=the_cell)

which sets the cubic cell defined before. From now on, you can access the cell
with the command

.. code:: python

    structure.cell

Finally, append each of the 2 atoms of the cell command. You can do it using
commands like

.. code:: python

    structure.append_atom(position=(alat/4., alat/4., alat/4.), symbols="Si")

for the first ‘Si’ atom. Repeat it for the other atomic site (0, 0, 0). You
can access and inspect the structure sites with the command

.. code:: python

    structure.sites

If you make a mistake, start over from
``structure = StructureData(cell=the_cell)``, or equivalently use
``structure.clear_kinds()`` to remove all kinds (atomic species) and sites.
Alternatively, AiiDA structures can also be converted directly from ASE
structures [#f1]_ using

.. code:: python

    from ase.spacegroup import crystal
    ase_structure = crystal('Si', [(0, 0, 0)], spacegroup=227,
                 cellpar=[alat, alat, alat, 90, 90, 90], primitive_cell=True)
    structure = StructureData(ase=ase_structure)

Now you can store the new structure object in the database with the command:

.. code:: python

    structure.store()

Finally, we can also import the silicon structure from an external (online)
repository such as the Crystallography Open Database (COD):

.. code:: python

    from aiida.tools.dbimporters.plugins.cod import CodDbImporter
    importer = CodDbImporter()
    for entry in importer.query(formula='Si', spacegroup='F d -3 m'):
        structure = entry.get_aiida_structure()
        print("Formula", structure.get_formula())
        print("Unit cell volume: ", structure.get_cell_volume())

In that case two duplicate structures are found for 'Si'.

Accessing inputs and outputs
----------------------------

Load again the calculation node used in Section :ref:`2019_sintef_loadnode`:

.. code:: python

    calc = load_node(PK)

Then type

.. code:: python

    calc.inputs.

and press ``TAB``: you will see all the link names between the calculation and
its input nodes. You can use a specific linkname to access the corresponding
input node, e.g.:

.. code:: python

    calc.inputs.structure

Similarly, if you type:

.. code:: python

    calc.outputs.

and then ``TAB``, you will list all output link names of the calculation. One
of them leads to the structure that was the input of ``calc`` we loaded
previously:

.. code:: python

    calc.outputs.output_structure

Note that links have a single name, that was assigned by the calculation that
used the corresponding input or produced the corresponding output, as
illustrated in section :ref:`2019_sintef_aiidagraph`.

For a more programmatic approach, you can get a represenation of the inputs and outputs of a node, say ``calc``, through the following methods:

.. code:: python

    calc_incoming = calc.get_incoming()
    calc_outgoing = calc.get_outgoing()

These methods will return an instance of the ``LinkManager`` class.
You can iterate over the neighboring nodes by calling the ``.all()`` method:

.. code:: python

    for entry in calc.get_outgoing():
        print(entry.link_label, entry.link_type, entry.node)

each entry returned by ``.all()`` is a ``LinkTriple``, a named tuple, from which you can get the link label and type and the neighboring node itself.
If you print one, you will see something like:

.. code:: python

    LinkTriple(node=<Dict: uuid: fac99f59-c69e-4ccd-9655-c7da1d469145 (pk: 1050)>, link_type=<LinkType.CREATE: 'create'>, link_label=u'output_parameters')

There are many other convenience methods on the ``LinkManager``.
For example if you are only interested in the link labels you can use:

.. code:: python

    calc.get_outgoing().all_link_labels()

which will return a list of all the labels of the outgoing links.
Likewise, ``.all_nodes()`` will give you a list of all the nodes to which links are going out from the ``calc`` node.
If you are looking for the node with a specific label, you can use:

.. code:: python

    calc.get_outgoing().get_node_by_label('output_parameters')

The ``get_outgoing`` and ``get_incoming`` methods also support filtering on various properties, such as the link label.
For example, if you only want to get the outgoing links whose label starts with ``output``, you can do the following:

.. code:: python

    calc.get_outgoing(link_label_filter='output%').all_nodes()


Pseudopotential families
------------------------

Pseudopotentials in AiiDA are grouped in 'families' that contain one single
pseudo per element. We will see how to work with UPF pseudopotentials (the
format used by Quantum ESPRESSO and some other codes). Download and untar the
SSSP pseudopotentials via the commands:

.. code:: bash

    wget https://archive.materialscloud.org/file/2018.0001/v3/SSSP_efficiency_pseudos.tar.gz
    tar -zxvf SSSP_efficiency_pseudos.tar.gz

Then you can upload the whole set of pseudopotentials to AiiDA by using the
following ``verdi`` command:

.. code:: bash

    verdi data upf uploadfamily SSSP_efficiency_pseudos 'SSSP' 'SSSP pseudopotential library'

In the command above, ``SSSP_efficiency_pseudos`` is the folder containing the
pseudopotentials, ``'SSSP'`` is the name given to the family, and the last argument
is its description. Finally, you can list all the pseudo families present in
the database with

.. code:: bash

    verdi data upf listfamilies


.. rubric:: Footnotes

.. [#f1] We purposefully do not provide advanced commands for crystal structure manipulation in AiiDA, because python packages that accomplish such tasks already exist (such as ASE or pymatgen).
