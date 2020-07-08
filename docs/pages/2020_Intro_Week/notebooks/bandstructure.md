---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: '0.9'
    jupytext_version: 1.5.1
kernelspec:
  display_name: Python 3
  language: python
  name: python3
language_info:
  file_extension: ".py"
  name: "python"
---

# A real world workchain example: electronic band structure

Let us start with some preliminary imports.

Before starting to run, make sure that you are using the `quicksetup` profile as the default profile!
You can check which is the default profile using `verdi profile list` (it will be the one with a `*` in front).

If it is not the default profile, use `verdi profile setdefault quicksetup`, and then restart your kernel before running the following lines.

```{code-cell} ipython3
%matplotlib inline
%aiida

from datetime import datetime, timedelta
from aiida.engine import run
from aiida.plugins import DbImporterFactory
CodDbImporter = DbImporterFactory('cod')

PwBandStructureWorkChain = WorkflowFactory('quantumespresso.pw.band_structure')
```

## Calculating the electronic band structure with an AiiDA workchain
This tutorial will show how useful a workchain can be in performing a well defined task, such as computing and visualizing the electronic band structure for a simple crystal structure. The goal of this tutorial is not to show you the intricacies of the actual workchain itself, but rather to serve as an example that workchains can simplify standard workflows in computational materials science. The workchain that we will use here will employ Quantum ESPRESSO's `pw.x` code to calculate the charge densities for several crystal structures and compute a band structure from those. Many choices that normally face the researcher before being able to perform this calculation, such as the selection of suitable pseudo potentials, energy cutoff values, k-point grids and k-point paths along high symmetry points, are now performed automatically by the workchain. All that remains for the user to do is to simply define a structure, pass it to the workchain and sit back!

+++

Below, we import the crystal structure of Al (aluminium) as an example, and run the `PwBandStructureWorkChain` for that structure. The estimated run time is noted in a comment in the calculation cell.

```{code-cell} ipython3
# Loading the COD importer so we can directly import structure from COD id's
importer = CodDbImporter()
# Make sure here to define the correct codename that corresponds to the pw.x code installed on your machine of choice
codename = 'qe-6.5-pw@localhost'
code = Code.get_from_string(codename)
```

### Importing example crystal structures from COD to AiiDA structure objects

```{code-cell} ipython3
# Al COD ID='9008460'
structure_Al = importer.query(id='9008460')[0].get_aiida_structure()

structure_Al.get_formula()

# The following structure can be used instead of Al, but will take much longer on the AWS machine.
# CaF2 COD ID='1000043' -- approximately 1/2 hour to run
# h-BN COD ID='9008997' -- approximately 45 mins to run
# GaAs COD ID='9008845' -- approximately 2 hours to run
```

### Now we run the bandstructure workchain for the selected structures

+++

The bandstructure workchain follows the following protocol:
* Determine the primitive cell of the input structure
* Run a vc-relax to relax the structure
* Refine the symmetry of the relaxed structure to ensure the primitive cell is used and run a self-consistent field calculation on it
* Run a non self-consistent field band structure calculation along a path of high symmetry k-points determined by [seekpath](http://materialscloud.org/tools/seekpath)

Numerical parameters for the default 'theos-ht-1.0' protocol are determined as follows:
* Suitable pseudopotentials and energy cutoffs are automatically searched from the [SSSP library](http://materialscloud.org/sssp) installed on your machine  (it uses the efficiency version 1.1).
* K-point mesh is selected to have a minimum k-point density of 0.2 Å<sup>-1</sup>
* A Marzari-Vanderbilt smearing of 0.02 Ry is used for the electronic occupations

In case the pseudopotentials are not installed, they can be downloaded in a terminal as:

    mkdir sssp_pseudos
    wget 'https://archive.materialscloud.org/record/file?filename=SSSP_1.1_PBE_efficiency.tar.gz&record_id=23&file_id=d2ce4186-bf76-4e05-8b39-444b4da30273' -O SSSP_1.1_PBE_efficiency.tar.gz
    tar -C sssp_pseudos -zxvf SSSP_1.1_PBE_efficiency.tar.gz
    verdi data upf uploadfamily sssp_pseudos 'SSSP' 'SSSP pseudopotential library'

The protocol looks for a UPF file with a specific hash code, that is unique for each different file.
You can check that you have the right
one by performing a search in the database:

    UpfData = DataFactory('upf')
    qb=QueryBuilder()
    qb.append(UpfData, filters={'attributes.md5':{'==':'cfc449ca30b5f3223ec38ddd88ac046d'}})
    len(qb.all())

'md5' is a searchable attribute of the pseudopotential data object.

```{code-cell} ipython3
# This will take approximately 6 minutes on the tutorial AWS (for Al)
results = run(
    PwBandStructureWorkChain,
    code=code,
    structure=structure_Al
)
```

```{code-cell} ipython3
fermi_energy = results['scf_parameters'].dict.fermi_energy
results['band_structure'].show_mpl(y_origin=fermi_energy, plot_zero_axis=True)

print("""Final crystal symmetry: {spacegroup_international} (number {spacegroup_number})
Extended Bravais lattice symbol: {bravais_lattice_extended}
The system has inversion symmetry: {has_inversion_symmetry}""".format(
    **results['seekpath_parameters'].get_dict()))
```

If you want to use a different pseudopotential family (or version of the family) (for instance [SSSP v1.0](https://doi.org/10.24435/materialscloud:2018.0001/v1) instead of the default SSSP v1.1) you can pass an additional parameter when calling the WorkChain, as follows:

    run(
        # ...,
        protocol = Dict(dict={
           'name':'theos-ht-1.0',
           'modifiers': {
           'pseudo' : 'SSSP-efficiency-1.0'
           }
        })
    )

(note that only some values are accepted for pseudo, that you can find [here](https://github.com/aiidateam/aiida-quantumespresso/blob/a52266d096afe48dbc6b38b63ac17a9989dd12fe/aiida_quantumespresso/utils/protocols/pw.py#L24); and that you will have to import the pseudopotentials in AiiDA first).
