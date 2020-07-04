.. _2020_virtual_intro:exploring_provenance:

******************************
Exploring the provenance graph
******************************

Accessing node inputs and outputs
=================================

Load again the calculation node from the :ref:`2020_virtual_aiidagraph` section:

.. code:: python

    calc = load_node(PK)

Then type

.. code:: python

    calc.inputs.

and press ``TAB``:
you will see all the link names between the calculation and its input nodes.
You can use a specific linkname to access the corresponding input node, e.g.:

.. code:: python

    calc.inputs.structure

Similarly, if you type:

.. code:: python

    calc.outputs.

and then ``TAB``, you will list all output link names of the calculation.
One of them leads to the structure that was the input of ``calc`` we loaded previously:

.. code:: python

    calc.outputs.output_structure

Note that links have a single name, that was assigned by the calculation which used the corresponding input or produced the corresponding output, as illustrated in section :ref:`2020_virtual_aiidagraph`.

For a more programmatic approach, you can get a representation of the inputs and outputs of a node, say ``calc``, through the following methods:

.. code:: python

    calc_incoming = calc.get_incoming()
    calc_outgoing = calc.get_outgoing()

These methods will return an instance of the ``LinkManager`` class.
You can print all nodes calling the ``.all()`` method:

.. code:: python

    print(calc_incoming.all())

or you can just iterate over the neighboring nodes and check the link properties as follows:

.. code:: python

    for entry in calc.get_outgoing():
        print(entry.link_label, entry.link_type, entry.node)

each entry is a named tuple (called ``LinkTriple``), from which you can get the link label and type and the neighboring node itself.
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

    calc.get_outgoing(link_label_filter='output%').all()

The provenance browser
======================

While the ``verdi`` CLI provides full access to the data underlying the provenance graph, a more intuitive tool for browsing AiiDA graphs is the interactive provenance browser available on `Materials Cloud <https://www.materialscloud.org>`__.

In order to use it, we first need to start the :ref:`AiiDA REST API <reference:rest-api>`:

.. code:: bash

    verdi restapi
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
