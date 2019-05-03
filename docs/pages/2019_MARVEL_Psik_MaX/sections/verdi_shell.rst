.. role:: raw-latex(raw)
   :format: latex
..

Verdi shell and AiiDA objects
=============================

In this section we will use an interactive IPython environment with all the basic AiiDA classes
already loaded. We propose two realizations of such a tool. The first consists of a special IPython
shell where all the AiiDA classes, methods and functions are accessible. Type in the terminal

.. code:: console

     verdi shell

For all the everyday AiiDA-based operations, i.e. creating, querying, and using AiiDA objects,
the ``verdi shell`` is probably the best tool. In this case, we suggest that you use two terminals,
one for the ``verdi shell`` and one to execute bash commands.

The second option is based on Jupyter notebooks and is probably most suitable to the purposes of
our tutorial. Go to the browser where you have opened ``jupyter`` and click ``New``
(:raw-latex:`\to`) ``Python 2`` (top right corner). This will open an IPython-based Jupyter notebook
based on cells where you can type portions of python code. The code will not be executed until you
press ``Shift+Enter`` from within a cell. Type in the first cell

.. code:: python

     %aiida

and execute it. This will set exactly the same environment as the ``verdi shell``. The notebook will
be automatically saved upon any modification and when you think you are done, you can export your
notebook in many formats by going to ``File`` (:raw-latex:`\to`) ``Download as``. We suggest you to
have a look to the drop-down menus ``Insert`` and ``Cell`` where you will find the main commands to
manage the cells of your notebook.

.. note::

     The ``verdi shell`` and Jupyter
     notebook are completely equivalent. Use either according to your
     personal preference.

You will still sometimes need to type command-line instructions in ``bash`` in the first terminal
you opened. To differentiate these from the commands to be typed in the ``verdi shell``, the latter
will be marked in this document by a yellow background, like:

.. code:: python

     some verdi shell command

while command-line instructions in ``bash`` to be typed into a terminal will be written with a white
background:

.. code:: console

     some bash command

Alternatively, to avoid changing terminal, you can execute ``bash`` commands within the
``verdi shell`` or the notebook adding an exclamation mark before the command itself

.. code:: python

     !some bash command

Loading a node[:code:`load_node`]
------------------------

Most AiiDA objects are represented by nodes, identified in the database by its ``PK`` number
(an integer). You can access a node using the following command in the shell:

.. code:: python

     node = load_node(PK)

Load a node using one of the calculation ``PK`` s visible in the graph you
displayed in the previous section of the tutorial. Then get the energy
of the calculation with the command

.. code:: python

     node.res.energy

You can also type

.. code:: python

     node.res.

and then press ``TAB`` to see all the possible output results of the
calculation.

Loading different kinds of nodes
--------------------------------

Pseudopotentials
~~~~~~~~~~~~~~~~

From the graph displayed in Section [sec:aiidagraph], find the pk of the
barium pseudopotential file (LDA). Load it and verify that it describes
barium. Type

.. code:: python

     upf = load_node(PK)
     upf.element

All methods of ``UpfData`` are accessible by typing ``upf.`` and then
pressing ``TAB``.

k-points
~~~~~~~~

A set of k-points in the Brillouin zone is represented by an instance of
the ``KpointsData`` class. Choose one from the graph of
Section [sec:aiidagraph], load it as ``kpoints`` and inspect its
content:

.. code:: python

     kpoints.get_kpoints_mesh()

Then get the full (explicit) list of k-points belonging to this mesh
using

.. code:: python

     kpoints.get_kpoints_mesh(print_list=True)

If you incurred in a ``AttributeError``, it means that the kpoints
instance does not represent a regular mesh but rather a list of k-points
defined by their crystal coordinates (typically used when plotting a
band structure). In this case, get the list of k-points coordinates
using

.. code:: python

     kpoints.get_kpoints()

If you prefer Cartesian (rather than crystal) coordinates, type

.. code:: python

     kpoints.get_kpoints(cartesian=True)

For later use in this tutorial, let us try now to create a kpoints
instance, to describe a regular
(2:raw-latex:`\times`2:raw-latex:`\times`2) mesh of k-points, centered
at the Gamma point (i.e. without offset). This can be done with the
following commands:

.. code:: python

     from aiida.orm.data.array.kpoints import KpointsData
     kpoints = KpointsData()
     kpoints_mesh = 2
     kpoints.set_kpoints_mesh([kpoints_mesh,kpoints_mesh,kpoints_mesh])
     kpoints.store()

The import performed in the first line is however unpractical as it
requires to remember the exact location of the module containing the
KpointsData class. Instead, it is easier to use the ``DataFactory``
function instead of an explicit import.

.. code:: python

     KpointsData = DataFactory("array.kpoints")

This function loads the appropriate class defined in a string (here
``array.kpoints``).[1] Therefore, ``KpointsData`` is not a class
instance, but the kpoints class itself!

Parameters
~~~~~~~~~~

Nested dictionaries with individual parameters, as well as lists and
arrays, are represented in AiiDA with ``ParameterData`` objects. Get the
PK and load the input parameters of a calculation in the graph of
Section [sec:aiidagraph]. Then display its content by typing

.. code:: python

     params.get_dict()

where ``params`` is the ``ParameterData`` node you loaded. Modify the
dictionary content so that the wave-function cutoff is now set to 20 Ry.
Note that you cannot modify an object already stored in the database. To
save the modification, you must create a new ParameterData object.
Similarly to what discussed before, first load the ``ParameterData``
class by typing

.. code:: python

     ParameterData = DataFactory('parameter')

Then an instance of the class (i.e. the parameter object that we want to
create) is created and initialized by the command

.. code:: python

     new_params = ParameterData(dict=YOUR_DICT)

where ``YOUR_DICT`` is the modified dictionary. Note that the parameter
object is not yet stored in the database. In fact, if you simply type
``new_params`` in the verdi shell, you will be prompted with a string
notifying you the “unstored” status. To save an entry in the database
corresponding to the ``new_params`` object, you need to type a last
command in the verdi shell:

.. code:: python

     new_params.store()

Structures
~~~~~~~~~~

Find a structure in the graph of Section [sec:aiidagraph] and load it.
Display its chemical formula, atomic positions and species using

.. code:: python

     structure.get_formula()
     structure.sites

where ``structure`` is the structure you loaded. If you are familiar
with ASE and PYMATGEN, you can convert this structure to those formats
by typing

.. code:: python

     structure.get_ase()
     structure.get_pymatgen()

Let’s try now to define a new structure to study, specifically a silicon
crystal. In the ``verdi shell``, define a cubic unit cell as a
(3:raw-latex:`\times`3) matrix, with lattice parameter (a\_{lat}=5.4) Å:

.. code:: python

     alat = 5.4
     the_cell = [[alat/2,alat/2,0.],[alat/2,0.,alat/2],[0.,alat/2,alat/2]]

**Note**: Default units for crystal structure cell and coordinates in
AiiDA are Å.

Structures in AiiDA are instances of ``StructureData`` class: load it in
the verdi shell

.. code:: python

     StructureData = DataFactory("structure")

Now, initialize the class instance (i.e. is the structure we want to
study) by the command

.. code:: python

     structure = StructureData(cell=the_cell)

which sets the cubic cell defined before. From now on, you can access
the cell with the command

.. code:: python

     structure.cell

Finally, append each of the 2 atoms of the cell command. You can do it
using commands like

.. code:: python

     structure.append_atom(position=(alat/4.,alat/4.,alat/4.),symbols="Si")

for the first ‘Si’ atom. Repeat it for the other atomic site
(:raw-latex:`\left`(0,0,0:raw-latex:`\right`)). You can access and
inspect[2] the structure sites with the command

.. code:: python

     structure.sites

If you make a mistake, start over from
``structure = StructureData(cell=the_cell)``, or equivalently use
``structure.clear_kinds()`` to remove all kinds (atomic species) and
sites. Alternatively, AiiDA structures can also be converted directly
from ASE  structures using[3]

.. code:: python

     from ase.lattice.spacegroup import crystal
     ase_structure = crystal('Si', [(0,0,0)], spacegroup=227,
                     cellpar=[alat, alat, alat, 90, 90, 90],primitive_cell=True)
     structure=StructureData(ase=ase_structure)

Now you can store the new structure object in the database with the
command:

.. code:: python

     structure.store()

Finally, we can also import the silicon structure from an external
(online) repository such as the Crystallography Open Database :

.. code:: python

    from aiida.tools.dbimporters.plugins.cod import CodDbImporter 
    importer = CodDbImporter()
    for entry in importer.query(formula='Si',spacegroup='F d -3 m'):
            structure = entry.get_aiida_structure()
            print "Formula", structure.get_formula()
            print "Unit cell volume: ", structure.get_cell_volume()

In that case two duplicate structures are found for Si.

Accessing inputs and outputs
----------------------------

Load again the calculation node used in Section [loadnode]:

.. code:: python

     calc = load_node(PK)

Then type

.. code:: python

     calc.inp.

and press ``TAB``: you will see all the link names between the
calculation and its input nodes. You can use a specific linkname to
access the corresponding input node, e.g.:

.. code:: python

     calc.inp.structure

You can use the ``inp`` method multiple times in order to browse the
graph. For instance, if the input structure node that you just accessed
is the output of another calculation, you can access the latter by
typing

.. code:: python

     calc2 = calc.inp.structure.inp.output_structure

Here ``calc2`` is the ``PwCalculation`` that produced the structure used
as an input for ``calc``.

Similarly, if you type:

.. code:: python

     calc2.out.

and then ``TAB``, you will list all output link names of the
calculation. One of them leads to the structure that was the input of
``calc`` we loaded previously:

.. code:: python

     calc2.out.output_structure

Note that links have a single name, that was assigned by the calculation
that used the corresponding input or produced the corresponding output,
as illustrated in Fig. [fig:graph].

For a more programmatic approach, you can get a list of the inputs and
outputs of a node, say ``calc``, with the methods

.. code:: python

     calc.get_inputs()
     calc.get_outputs()

Alternatively, you can get a dictionary where the keys are the link
names and the values are the linked objects, with the methods

.. code:: python

     calc.get_inputs_dict()
     calc.get_outputs_dict()

Note: You will sometime see entries in the dictionary with names like
``output_kpoints_3511``. These exist because standard python
dictionaries require unique key names while link labels may not be
unique. Therefore, we use the link label plus the PK separated by
underscores.

Pseudopotential families
------------------------

Pseudopotentials in AiiDA are grouped in “families” that contain one
single pseudo per element. We will see how to work with UPF
pseudopotentials (the format used by Quantum ESPRESSO and some other
codes). Download and untar the SSSP  pseudopotentials via the commands:

.. code:: console

     wget https://archive.materialscloud.org/file/2018.0001/v1/SSSP_efficiency_pseudos.tar.gz
     tar -zxvf SSSP_efficiency_pseudos.tar.gz

Then you can upload the whole set of pseudopotentials to AiiDA by to the
following ``verdi`` command:

.. code:: console

    verdi data upf uploadfamily SSSP_efficiency_pseudos 'SSSP' 'SSSP pseudopotential library'

In the command above, ``SSSP_efficiency_pseudos`` is the folder
containing the pseudopotentials, ’SSSP’ is the name given to the family
and the last argument is its description. Finally, you can list all the
pseudo families present in the database with

.. code:: console

     verdi data upf listfamilies
