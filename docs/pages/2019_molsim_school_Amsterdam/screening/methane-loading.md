# Compute methane loading for one MOF

With the codes set up and the daemon running, we are ready to do our first calculation using AiiDA --
the methane loading of a MOF at 65 bar.

We will use the [RASPA](../theoretical/settings-raspa.md) code to perform a grand-canonical 
Monte Carlo (GCMC) calculation, trying to insert methane molecules into the nanoporous
framework at the given pressure.

In principle, we could continue to use the `verdi shell` or `jupyter notebooks`
but in order to speed things up, we've already prepared a template python script
that you'll need to adapt to your needs.


## RASPA input parameters

The [aiida-raspa](https://github.com/yakutovicha/aiida-raspa/) plugin uses `ParameterData` nodes
to specify the input parameters of RASPA:

```python
parameters = ParameterData(dict={
    "GeneralSettings": {
         "SimulationType"                : "MonteCarlo",
         "NumberOfCycles"                : 1000,
         "NumberOfInitializationCycles"  : 1000,
         "PrintEvery"                    : 100,

         "CutOff"                        : <float (A)>,

         "Forcefield"                    : "UFF-TraPPE",
         "ChargeMethod"                  : "None",
         "UnitCells"                     : "<int> <int> <int>",

         "ExternalTemperature"           : <float (K)>,
         "ExternalPressure"              : <float (Pa)>,
    },
    "Component": [{
         "MoleculeName"                  : "methane",
         "MoleculeDefinition"            : "TraPPE",
         "MolFraction"                   : 1.0,
         "TranslationProbability"        : <float>, # between 0 and 1
         "RotationProbability"           : <float>, # between 0 and 1
         "ReinsertionProbability"        : <float>, # between 0 and 1
         "SwapProbability"               : <float>, # between 0 and 1
         "CreateNumberOfMolecules"       : 0,
    }],
})
```

---
### Exercise

The `ParameterData` dictionary is missing a number of parameters 
for which you'll need to figure out reasonable values.

-   Our simulations are performed under periodic boundary
    conditions. This means, we need to make our simulation cell
    large enough that a molecule will never interact with a two
    periodic copies of any of its neighbors. Given the cutoff radius
    of 12 Angstroms, how often do you need to replicate the unit
    cell of the material?

    *Hint:* The CIF files include information on the size of the
    unit cell.

---

Another input to the calculation is the structure we want to use --
you can start e.g. with `HKUST1`, which can be loaded using its uuid:

```python
# using uuid of HKUST1
structure = load_node('31037e3c-6b15-4a5d-90e3-16c6e0951159')
```

## Creating the calculation

Every calculation sent to a cluster is linked to a code, which describes
the executable file to be used. We need to load the `raspa@bazis` code
that we set up before:

```python
from aiida.common.example_helpers import test_and_get_code 
raspa_code = test_and_get_code("raspa@bazis", expected_code_type='raspa')
```

Now we'll specify a few pieces of information to
pass on to the [slurm](https://slurm.schedmd.com/) scheduler
that manages calculations on the cluster,
such as how many compute nodes to use
or the maximum time allowed for the calculation

```python
options = {
    "resources": {
        "num_machines": 1,                 # run on 1 node
        "tot_num_mpiprocs": 1,             # use 1 process
        "num_mpiprocs_per_machine": 1,
    },
    "max_wallclock_seconds": 1 * 60 * 60,  # 1h walltime
    "max_memory_kb": 2000000,              # 2GB memory
    "queue_name": "molsim",
    "withmpi": False,
}
```
> **Note**  
> AiiDA supports different types of schedulers via plugins,
> including slurm, pbspro and sge.


## Submitting the calculation

In principle, you can now simply submit the calculation from the `verdi shell`
using

```python
RaspaCalculation = CalculationFactory('raspa')
submit(RaspaCalculation.process(),
    code=raspa_code,
    structure=structure,
    parameters=parameters,
    _options=options,
)
```

At this stage, however, we suggest you use a python script instead
in order to make changes and debug more easily.

We've provided a
[submission script template]({{ site.baseurl}}/assets/2019_molsim_school_Amsterdam/raspa_loading.py),
where you just need to paste your parameters and the structure you selected.

```terminal
$ verdi run <scriptname>
```
> **Note**  
> By default, the daemon polls for new calculations every 30 seconds,
> i.e. you may need to wait up to 30 seconds before your calculation starts running.

Use `verdi calculation list -a` to monitor the state of the calculation.
Once running, the calculation should finish within 5 minutes.

## Analyzing your results

Once the calculation shows up as `FINISHED`, have a look at the result.

TODO (Daniele/Leo):
 * how to compute loading from output
 * mention standard deviation of relevant quantity and ask them to re-run the calculation
   so that it goes below 5%  
  

