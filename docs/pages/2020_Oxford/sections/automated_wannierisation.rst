.. _Oxford 2020 autowannier:

Automated high-throughput wannierisation
========================================

In the following tutorial you will learn how to perform automated high-throughput Wannierisation using
a dedicated AiiDA workchain.

The protocol for automating the construction of Wannier functions is discussed in the following article:

* Valerio Vitale, Giovanni Pizzi, Antimo Marrazzo, Jonathan Yates, Nicola Marzari, Arash Mostofi,
  *Automated high-throughput wannierisation*, accepted in npj Computational Materials (2020);
  https://arxiv.org/abs/1909.00433

whose data is available on the `Materials Cloud Archive <http://archive.materialscloud.org>`_ as:

* Valerio Vitale, Giovanni Pizzi, Antimo Marrazzo, Jonathan R. Yates, Nicola Marzari, Arash A. Mostofi,
  Automated high-throughput Wannierisation, Materials Cloud Archive (2019), `doi: 10.24435/materialscloud:2019.0044/v2 <https://doi.org/10.24435/materialscloud:2019.0044/v2>`_.

The protocol leverages the SCDM method introduced in:

* Anil Damle, Lin Lin, and Lexing Ying,
  `Compressed representation of kohn–sham orbitals via selected columns of the density matrix <https://doi.org/10.1021/ct500985f>`_
  Journal of Chemical Theory and Computation 11, 1463–1469 (2015).

* Anil Damle and L. Lin,
  `Disentanglement via entanglement: A unified method for wannier localization <https://doi.org/10.1137/17M1129696>`_,
  Multiscale Modeling & Simulation 16, 1392–1410 (2018).

The initial workflow was written by Antimo Marrazzo (EPFL) and Giovanni Pizzi (EPFL) (and is available, in a Virtual Machine, on the Materials Cloud entry mentioned above). It was later
substantially improved and upgraded to AiiDA v1.x by Junfeng Qiao (EFPL). The SCDM implementation in
Quantum ESPRESSO was done by Valerio Vitale (Imperial College London and University of Cambridge).

.. note:: **Launch while you read!**
  The workflow should take a few minutes to run on the virtual machine (5-10 minutes). So, we suggest that you launch it now (following the suggestions below) in the background, while you read through the tutorial.

Preparation
-----------

You can download the launch script for the workflow here: :download:`launch_auto-wannier_workflow.py <include/snippets/launch_auto-wannier_workflow.py>`.
The script accepts one argument, which is the location of the crystal structure file (in XSF format) for which you want to run the Wannierisation.
As an example, you can pick any one of the simple crystal structures from this list below:

    * :download:`Ar2.xsf <include/xsf/Ar2.xsf>`
    * :download:`BrNa.xsf <include/xsf/BrNa.xsf>`
    * :download:`GaAs.xsf <include/xsf/GaAs.xsf>`
    * :download:`F4Ni2.xsf <include/xsf/F4Ni2.xsf>`
    * :download:`O2Rb2.xsf <include/xsf/O2Rb2.xsf>`
    * :download:`BaS.xsf <include/xsf/BaS.xsf>`
    * :download:`C6Mg4.xsf <include/xsf/C6Mg4.xsf>`
    * :download:`FNa.xsf <include/xsf/FNa.xsf>`
    * :download:`O2Sr.xsf <include/xsf/O2Sr.xsf>`
    * :download:`BeO4S.xsf <include/xsf/BeO4S.xsf>`
    * :download:`CaO.xsf <include/xsf/CaO.xsf>`
    * :download:`Cr2F4.xsf <include/xsf/Cr2F4.xsf>`
    * :download:`O2Pb2.xsf <include/xsf/O2Pb2.xsf>`
    * :download:`PtS2.xsf <include/xsf/PtS2.xsf>`
    * :download:`Br2Ti.xsf <include/xsf/Br2Ti.xsf>`
    * :download:`Cl2O2Ti2.xsf <include/xsf/Cl2O2Ti2.xsf>`
    * :download:`CsH.xsf <include/xsf/CsH.xsf>`
    * :download:`O2Pd2.xsf <include/xsf/O2Pd2.xsf>`

Once you downloaded both the launcher script and one of the XSF files, launch the script with the following command:

.. code:: bash

    verdi run launch_auto-wannier_workflow.py CsH.xsf

(in the following, we will use CsH as an example); you can replace ``CsH.xsf`` with any other structure of the list above, e.g. ``PtS2.xsf``, or ``Br2Ti.xsf``, ...


Introduction
------------

The use of maximally-localised Wannier functions (MLWFs) in high-throughput (HT) workflows
has been hindered by the fact that generating MLWFs automatically and robustly without any user
intervention and for arbitrary materials is, in general, very challenging.

The procedure to obtain MLWFs requires to specify
a number of parameters that depends on the specific system under study,
such as

* the type of projections to build the :math:`A_{mn}({\mathbf{k}})` matrix

and, in the case entangled bands, many other parameters like

* the number of Wannier functions,
* the frozen energy window,
* the outer energy window, ...

The SCDM method allows to circumvent the need to specify initial projections,
by introducting an algorithm that builds the :math:`A_{mn}({\mathbf{k}})` matrix by
optimally selecting columns of the density matrix :math:`P_{\mathbf{k}}`

.. math ::

    P_{\mathbf{k}}(\mathbf{r},\mathbf{r'})=\sum_{n=1}^{J}f(\epsilon_{n\mathbf{k}})\psi_{n{\mathbf{k}}}(\mathbf{r})\psi^*_{n{\mathbf{k}}}(\mathbf{r'})

where :math:`f(\epsilon_{n\mathbf{k}})` is an occupation function.
The SCDM algorithm is based on a QR factorization with column pivoting (QRCP) and it is
currently implemented in the ``pw2wannier90.x`` code of Quantum Espresso.

It is worth to stress that the occupation function does not necessarily correspond to
a physical smearing, but it used as a "window function" that restricts the manifold to the energy region of interest.
For example, the isolated-band case can be recovered by setting :math:`f(\epsilon_{n\mathbf{k}})=1` for energy values
:math:`\epsilon_{n\mathbf{k}}` within the energy range of the isolated bands, and zero elsewhere.

Another typical choice for the occupation function is the so-called *complementary error function* (``erfc``)

.. math ::

  f(\epsilon)=\frac{1}{2}\mathrm{erfc}\left(\frac{\epsilon - \mu}{\sigma}\right)

and it is used to to deal with a manifold of bands that are entangled only in the upper energy region (e.g. for metals, or for the conduction band of insulators).
Another possible choice for the occupation function could be a Gaussian, for instance to extract bands in a specific energy range from a fully
entangled manifold.

While the SCDM method allows to avoid the disentanglement procedure, and so the need to specify
the frozen and outer window, it does not provide a recipe to set the smearing function parameters
:math:`\mu` and :math:`\sigma`. In addition, the number of Wannier function remains to be set and
a sensible value typically requires some chemical consideration, such as counting the number of atomic orbitals
of a given orbital character (e.g. :math:`s`, :math:`p`, :math:`d`, :math:`sp^3`, ...).

The ``Wannier90BandsWorkChain`` (distributed in the `aiida-wannier90-workflows package <https://github.com/aiidateam/aiida-wannier90-workflows>`_) is an AiiDA workchain that implements a protocol that deals with the choice
of the number of Wannier functions and sets the parameters :math:`\mu` and :math:`\sigma` defining
the smearing function. For a full explanation of protocol we refer to the article
`Automated high-throughput wannierisation  <https://arxiv.org/abs/1909.00433>`_, while here we
just outline the main features.

The workflow starts by running a DFT calculation (with Quantum ESPRESSO) using automated workchains distributed within the `aiida-quantumespresso <https://github.com/aiidateam/aiida-quantumespresso>`_ plugin, that take care of
automation for the calculations performed with Quantum ESPRESSO (QE).
This is followed by a calculation of the *projectability*, that is the projection of the Kohn-Sham states
onto localised atomic orbitals:

.. math ::

    p_{n\mathbf{k}} = \sum_{I,l,m}|\langle \psi_{n\mathbf{k}} | \phi_{Ilm}^{\mathbf{k}}\rangle|^2,

where the :math:`\phi_{Ilm}(\mathbf{k})` are the pseudo-atomic orbitals (PAO) employed in
the generation of the pseudopotentials, :math:`I` is an index running over the atoms in the cell
and :math:`lm` define the usual angular momentum quantum numbers.

The workflow is designed for the specific use case where we are interested in Wannierise the occupied bands (plus, optionally, some unoccupied
or partially occupied bands) in insulators and in metals.

The **number of Wannier functions** is automatically set equal to the number of PAOs defined in the pseudopotentials (and the pseudopotentials are automatically taken from the `SSSP efficiency library <https://www.materialscloud.org/discover/sssp/table/efficiency>`_).
The projectabilities on these PAO orbitals are then computed and used to
set the **optimal smearing function (erfc) parameters** :math:`\mu` and :math:`\sigma` as explained in the paper
`Automated high-throughput wannierisation  <https://arxiv.org/abs/1909.00433>`_.
After the calculation of the projectabilities, the workflow proceeds with the usual Wannierisation step: first
it computes the overlap and projection matrices using ``pw2wannier90``, and then it runs the Wannier90 code.

Here we summarise the main steps of the ``Wannier90BandsWorkChain``:

* SCF (QuantumESPRESSO ``pw.x``)
* NSCF (QuantumESPRESSO ``pw.x``)
* Projectability (QuantumESPRESSO ``projwfc.x``)
* Wannier90 pre-processing (``wannier90.x -pp``)
* Overlap matrices :math:`M_{mn}`, initial projections with SCDM :math:`A_{mn}` (QuantumESPRESSO ``pw2wannier90.x``)
* Wannierisation (``wannier90.x``)

The output of the workflow includes several nodes, including the projectabilities
and interpolated band structure, that we are going to inspect after the run.


Running the workflow
--------------------

If you have not launch the script yet, let's do it now!

Here we focus on how to run the ``Wannier90BandsWorkChain``, the AiiDA workchain
that implements the automation workflow to obtain MLWFs, for the full code documentation of the
AiiDA-Wannier90 plugin please visit the
`AiiDA-Wannier90 documentation <https://aiida-wannier90.readthedocs.io/en/latest/>`_.

If you have not done it yet, you can start by downloading the
:download:`launch_auto-wannier_workflow.py <include/snippets/launch_auto-wannier_workflow.py>` script to your work directory.
The script is reported also here below and allows to initialise and launch the AiiDA workchain.

.. literalinclude:: include/snippets/launch_auto-wannier_workflow.py

The script can accept one commandline argument for specifying
the location of the crystal structure file in the xsf format.
You can again download some simple crystal structures from this list

    * :download:`Ar2.xsf <include/xsf/Ar2.xsf>`
    * :download:`BrNa.xsf <include/xsf/BrNa.xsf>`
    * :download:`GaAs.xsf <include/xsf/GaAs.xsf>`
    * :download:`F4Ni2.xsf <include/xsf/F4Ni2.xsf>`
    * :download:`O2Rb2.xsf <include/xsf/O2Rb2.xsf>`
    * :download:`BaS.xsf <include/xsf/BaS.xsf>`
    * :download:`C6Mg4.xsf <include/xsf/C6Mg4.xsf>`
    * :download:`FNa.xsf <include/xsf/FNa.xsf>`
    * :download:`O2Sr.xsf <include/xsf/O2Sr.xsf>`
    * :download:`BeO4S.xsf <include/xsf/BeO4S.xsf>`
    * :download:`CaO.xsf <include/xsf/CaO.xsf>`
    * :download:`Cr2F4.xsf <include/xsf/Cr2F4.xsf>`
    * :download:`O2Pb2.xsf <include/xsf/O2Pb2.xsf>`
    * :download:`PtS2.xsf <include/xsf/PtS2.xsf>`
    * :download:`Br2Ti.xsf <include/xsf/Br2Ti.xsf>`
    * :download:`Cl2O2Ti2.xsf <include/xsf/Cl2O2Ti2.xsf>`
    * :download:`CsH.xsf <include/xsf/CsH.xsf>`
    * :download:`O2Pd2.xsf <include/xsf/O2Pd2.xsf>`

Launch the script with the following command

.. code:: bash

    verdi run launch_auto-wannier_workflow.py CsH.xsf

You can use a different structure now, so replace CsH.xsf with any other structure that you saw above folder, e.g. O2Sr.xsf or PtS2.xsf.

**NB** Here for the tutorial we run the workflow in *testing* mode, where all the wavefunction cutoffs are halved to
speed up the calculations. For production please use the 'theos-ht-1.0' protocol or any other sensible choice.

To get a list of all the AiiDA workchains that are running and their status you can use

.. code:: bash

    verdi process list

Analyzing the outputs of the workflow
-------------------------------------

Now we analyse the reports and outputs of the workflow using the command line.

While the ``Wannier90BandsWorkChain`` is running you can monitor the progress of the workflow by
looking at the report using the command

.. code:: bash

    verdi process report <PK>

where PK corresponds to the workchain pk. You will see a log with messages printed by the workchain,
including the pks of all the sub-workchains and calculations launched by the ``Wannier90BandsWorkChain``,
similar to the following:

.. literalinclude:: include/snippets/workchain_report.txt


Once the workchain has finished to run, you can look at all the inputs and outputs with

.. code:: bash

    verdi node show <PK>

You should obtain an output similar to what follows:

.. literalinclude:: include/snippets/workchain_show.txt


Analyzing and comparing the band structure
------------------------------------------

First let's give a look at the interpolated band structure by exporting a pdf file with

.. code:: bash

    verdi data bands export --format mpl_pdf --output band_structure.pdf <PK_bands>

where PK_bands stands for the ``BandsData`` pk produced by the workflow.
You can find it :code:`verdi node show <PK>` with PK being the workchain pk.
You should obtain a pdf like the following:

.. figure:: include/images/CsH_wan_band.png
   :width: 100%

Now we compare the Wannier-interpolated bands with the full DFT bands calculation.
For convenience, we have already computed for you all the full DFT band structures for the
compounds you find the xsf folder. You can download the full DFT bands in the xmgrace (.agr) format form this list:

    * :download:`Ar2_dft_bands.agr <include/dft_bands/Ar2_dft_bands.agr>`
    * :download:`BrNa_dft_bands.agr <include/dft_bands/BrNa_dft_bands.agr>`
    * :download:`AsGa_dft_bands.agr <include/dft_bands/AsGa_dft_bands.agr>`
    * :download:`F4Ni2_dft_bands.agr <include/dft_bands/F4Ni2_dft_bands.agr>`
    * :download:`O2Rb2_dft_bands.agr <include/dft_bands/O2Rb2_dft_bands.agr>`
    * :download:`BaS_dft_bands.agr <include/dft_bands/BaS_dft_bands.agr>`
    * :download:`C6Mg4_dft_bands.agr <include/dft_bands/C6Mg4_dft_bands.agr>`
    * :download:`FNa_dft_bands.agr <include/dft_bands/FNa_dft_bands.agr>`
    * :download:`O2Sr_dft_bands.agr <include/dft_bands/O2Sr_dft_bands.agr>`
    * :download:`BeO4S_dft_bands.agr <include/dft_bands/BeO4S_dft_bands.agr>`
    * :download:`CaO_dft_bands.agr <include/dft_bands/CaO_dft_bands.agr>`
    * :download:`Cr2F4_dft_bands.agr <include/dft_bands/Cr2F4_dft_bands.agr>`
    * :download:`O2Pb2_dft_bands.agr <include/dft_bands/O2Pb2_dft_bands.agr>`
    * :download:`PtS2_dft_bands.agr <include/dft_bands/PtS2_dft_bands.agr>`
    * :download:`Br2Ti_dft_bands.agr <include/dft_bands/Br2Ti_dft_bands.agr>`
    * :download:`Cl2O2Ti2_dft_bands.agr <include/dft_bands/Cl2O2Ti2_dft_bands.agr>`
    * :download:`CsH_dft_bands.agr <include/dft_bands/CsH_dft_bands.agr>`
    * :download:`O2Pd2_dft_bands.agr <include/dft_bands/O2Pd2_dft_bands.agr>`

Take CsH as an example, you can first export the bands in the xmgrace format with

.. code:: bash

    verdi data bands export --format agr --output CsH_wan_bands.agr <PK_bands>

and compare it with the full DFT band structure using xmgrace

.. code:: bash

    xmgrace CsH_dft_bands.agr CsH_wan_bands.agr

where you can replace CsH with any chemical formula of the other crystal structures we provide.
For a reference, here are the two agr files
:download:`CsH_dft_bands.agr <include/dft_bands/CsH_dft_bands.agr>`
:download:`CsH_wan_bands.agr <include/dft_bands/CsH_wan_bands.agr>`

You should obtain something like this:


.. figure:: include/images/CsH_diff_bands.png
   :width: 100%


Analyzing the projectabilities
------------------------------

Now you will see how to look at the projectabilities that were use in the automation protocol.
You can download the following script
:download:`plot_projectabilities.py <include/snippets/plot_projectabilities.py>` and run it

.. code:: bash

    verdi run plot_projectabilities.py <PK>

where PK stands for the ``Wannier90BandsWorkChain`` pk.

You should obtain a plot similar to the following:

.. figure:: include/images/CsH_proj.png
   :width: 100%

As you can see the protocol to choose :math:`\mu` and :math:`\sigma` ensures that the
SCDM algorithm is applied to a density-matrix that is made only by Kohn-Sham states
that can be projected on the manifold spanned by the PAOs.

Analyzing the provenance graph
------------------------------

We begin by generating the provenance graph with

.. code:: bash

    verdi node graph generate <PK>

where the PK correspond to the workflow you have just run.
You should obtain something like the following

.. figure:: include/images/CsH.dot.jpg
   :width: 100%

   Provenance graph for a single ``Wannier90BandsWorkChain`` run. (PDF version
   :download:`CsH.dot.pdf <include/images/CsH.dot.pdf>`)

As you can see, AiiDA has tracked all the inputs provided to the calculation, allowing you (or anyone else) to reproduce it later on.
AiiDA's record of a calculation is best displayed in the form of a provenance graph


(Optional) Maximal localisation & SCDM
--------------------------------------

Try to modify the :download:`launch_auto-wannier_workflow.py <include/snippets/launch_auto-wannier_workflow.py>` script to disable the MLWF
procedure in order to obtain Wannier functions with SCDM projections that are not localised.
Run the code for 1-2 materials of the dataset, do you notice any difference?

(Optional) Browse your database with the REST API
-------------------------------------------------

Connect to the `AiiDA REST API <https://www.materialscloud.org/explore/connect>`_ and browse your database!
Follow the instruction that you find on the `Materials Cloud website <https://www.materialscloud.org/explore/connect>`_.

(Optional) More on AiiDA
------------------------

You now have a first taste of the type of problems AiiDA tries to solve.
Here are some options for how to continue:

 * Continue with the in-depth tutorial and learn more about the ``verdi``, ``verdi shell`` and ``python`` interfaces to AiiDA.
   There is more than enough material to keep you busy for a day.
 * Try `setting up AiiDA directly on your laptop <https://aiida-core.readthedocs.io/en/latest/install/quick_installation.html>`_.

   .. note:: **For advanced Linux & python users only**.
     AiiDA depends on a number of services and software that require some skill to set up.
     Unfortunately, we don't have the human resources to help you solve
     issues related to your setup in a tutorial context.
