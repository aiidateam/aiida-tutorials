.. _2020_virtual_intro:exploring_provenance:

******************************
Exploring the provenance graph
******************************

Accessing node inputs and outputs
=================================

Load again the calculation node from the :ref:`2020_virtual_aiidagraph` section:

.. code-block:: ipython

    In [1]: calc = load_node(uuid='ce81c420')

Then type

.. code-block:: ipython

    In [2]: calc.inputs.

and press ``TAB``:
you will see all the link names between the calculation and its input nodes.
You can use a specific linkname to access the corresponding input node, e.g.:

.. code-block:: ipython

    In [2]: calc.inputs.structure
    Out[2]: <StructureData: uuid: 3a4b1270-82bf-4d66-a51f-982294f6e1b3 (pk: 1161)>

Similarly, if you type:

.. code-block:: ipython

    In [3]: calc.outputs.

and then ``TAB``, you will list all output link names of the calculation.
One of them leads to the structure that was the input of ``calc`` we loaded previously:

.. code-block:: ipython

    In [3]: calc.outputs.output_structure
    Out[3]: <StructureData: uuid: 254e5a86-7478-4b91-ab2d-7e980eced9be (pk: 816)>

Note that links have a single name, that was assigned by the calculation which used the corresponding input or produced the corresponding output, as illustrated in section :ref:`2020_virtual_aiidagraph`.

For a more programmatic approach, you can get a representation of the inputs and outputs of a node, say ``calc``, through the following methods:

.. code-block:: ipython

    In [4]: calc.get_incoming()                                                                                                          
    Out[4]: <aiida.orm.utils.links.LinkManager at 0x14a27ca6f240>

.. code-block:: ipython

    In [5]: calc.get_outgoing()                                                                                                          
    Out[5]: <aiida.orm.utils.links.LinkManager at 0x14a27d038940>

These methods return an instance of the ``LinkManager`` class.
You can obtain all nodes calling the ``.all()`` method:

.. code-block:: ipython

    In [6]: print(calc.get_incoming().all())                                                                           

or you can just iterate over the neighboring nodes and check the link properties as follows:

.. code-block:: ipython

    In [7]: for entry in calc.get_outgoing(): 
       ...:     print(entry.link_label, entry.link_type, entry.node) 

each entry is a named tuple (called ``LinkTriple``), from which you can get the link label and type and the neighboring node itself.
If you print one, you will see something like:

.. code-block:: python

    LinkTriple(node=<Dict: uuid: fac99f59-c69e-4ccd-9655-c7da1d469145 (pk: 1050)>, link_type=<LinkType.CREATE: 'create'>, link_label=u'output_parameters')

There are many other convenience methods on the ``LinkManager``.
For example if you are only interested in the link labels you can use:

.. code-block:: ipython

    In [8]: calc.get_outgoing().all_link_labels()
    Out[8]: 
    ['retrieved',
     'output_parameters',
     'remote_folder',
     'output_structure',
     'output_trajectory_array',
     'output_kpoints']

which will return a list of all the labels of the outgoing links.
Likewise, ``.all_nodes()`` will give you a list of all the nodes to which links are going out from the ``calc`` node.
If you are looking for the node with a specific label, you can use:

.. code-block:: ipython

    In [9]: calc.get_outgoing().get_node_by_label('output_parameters')
    Out[9]: <Dict: uuid: 0119c80c-fb2d-46d7-b2f0-a4b59a62ae5b (pk: 817)>

The ``get_outgoing`` and ``get_incoming`` methods also support filtering on various properties, such as the link label.
For example, if you only want to get the outgoing links whose label starts with ``output``, you can do the following:

.. code-block:: ipython

    In [10]: calc.get_outgoing(link_label_filter='output%').all()
    Out[10]: 
    [LinkTriple(node=<Dict: uuid: 0119c80c-fb2d-46d7-b2f0-a4b59a62ae5b (pk: 817)>, link_type=<LinkType.CREATE: 'create'>, link_label='output_parameters'),
     LinkTriple(node=<StructureData: uuid: 254e5a86-7478-4b91-ab2d-7e980eced9be (pk: 816)>, link_type=<LinkType.CREATE: 'create'>, link_label='output_structure'),
     LinkTriple(node=<ArrayData: uuid: db55db3b-ba60-44b3-a479-65fcb62f5988 (pk: 818)>, link_type=<LinkType.CREATE: 'create'>, link_label='output_trajectory_array'),
     LinkTriple(node=<KpointsData: uuid: fa84ce2b-788c-403a-83d3-52faf2724c3c (pk: 1483)>, link_type=<LinkType.CREATE: 'create'>, link_label='output_kpoints')]

The provenance browser
======================

While the ``verdi`` CLI provides full access to the data underlying the provenance graph, a more intuitive tool for browsing AiiDA graphs is the interactive provenance browser available on `Materials Cloud <https://www.materialscloud.org>`__.

In order to use it, we first need to start the :ref:`AiiDA REST API <reference:rest-api>`:

.. code-block:: console

    $ verdi restapi
     * REST API running on http://127.0.0.1:5000/api/v4
     * Serving Flask app "aiida.restapi.run_api" (lazy loading)
     * Environment: production
       WARNING: This is a development server. Do not use it in a production deployment.
       Use a production WSGI server instead.
     * Debug mode: off
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Now you can connect the provenance browser to your local REST API:

-  Open the |provenance_browser| on your laptop
-  In the form, paste the (local) URL ``http://127.0.0.1:5000/api/v4`` of our REST API
-  Click "GO!"

.. |provenance_browser| raw:: html

   <a href="https://www.materialscloud.org/explore/connect" target="_blank">provenance explorer</a>

Once the provenance browser javascript application has been loaded by your browser, it is communicating directly with the REST API and your data never leaves your computer.

.. note::
    In order for this to work on your laptop, while the REST API is running on the virtual machine, we've enabled SSH tunneling for port ``5000`` in :ref:`2020_virtual_intro:setup`.

Start by clicking on the details of a calculation job and use the graph explorer to complete the exercise below (you can filter by calculation jobs using the menu on the left, under ``Process -> Calculation -> Calculation job``).
If you ever get lost, just go to the "Details" tab, enter ``ce81c420-7751-48f6-af8e-eb7c6a30cec3`` and click on the "GO" button.

.. admonition:: Exercise

   Use the provenance browser in order to figure out:

   -  When was the calculation run and who run it?
   -  Was it a serial or a parallel calculation? How many MPI processes were used?
   -  What inputs did the calculation take?
   -  What code was used and what was the name of the executable?
   -  How many calculations were performed using this code?
