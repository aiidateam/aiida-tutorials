# Compute methane loading for one MOF

With the codes set up and the daemon running, we are ready to do our first calculation using AiiDA --
the methane loading of a MOF at 65 bar.

We will use the [RASPA](../theoretical/settings-raspa.md) code to perform a grand-canonical 
Monte Carlo (GCMC) calculation, trying to insert methane molecules into the nanoporous
framework at the given pressure.

In principle, we could continue to use the `verdi shell` or `jupyter notebooks`
but in order to speed things up, we've already prepared a template python script
that you can [download here]({{ site.baseurl}}/assets/2019_molsim_school_Amsterdam/raspa_loading.py).

In the following, you will adapt it to your needs.

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

         "CutOff"                        : 12.0,  # (Angstroms)

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
         "TranslationProbability"        : 1.0,
         "RotationProbability"           : 1.0,
         "ReinsertionProbability"        : 1.0,
         "SwapProbability"               : 1.0,
         "CreateNumberOfMolecules"       : 0,
    }],
})
```

---
### Exercise

The `ParameterData` dictionary is missing a number of parameters 
for which you'll need to figure out reasonable values.

 -  `UnitCells`: Our simulations are performed under periodic boundary
    conditions. This means, we need to make our simulation cell
    large enough that a molecule will never interact with two
    periodic copies of any of its neighbors. Given the cutoff radius
    of 12 Angstroms, how often do you need to replicate the unit
    cell of the material?

    *Hint:* The CIF files include information on the size of the
    unit cell.

 - For `ExternalTemperature`/`ExternalPressure`: Use ambient temperature
   and standard methane desorption pressure for natural gas vehicles.

 - Currently, the probabilies for translation, rotation, reinsertion and swap
   Monte Carlo moves are all equal, which is suboptimal.
   How would optimize them?
   
---

Another input of the calculation is the atomic structure of the MOF we want to use.
Find the structure labelled "ABUWOJ" (hint: filter by the `label`)
and note down its PK or UUID. 

> **Note**  
> Once you know the PK or UUID of a node, you can always load it using
> ```python
> structure = load_node(<pk>)     # load using PK (specific to your database)
> structure = load_node('<uuid>') # load using UUID (same for everyone)
> ```

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
or the maximum time allowed for the calculation:

```python
options = {
    "resources": {
        "num_machines": 1,                 # run on 1 node
        "tot_num_mpiprocs": 1,             # use 1 process
        "num_mpiprocs_per_machine": 1,
    },
    "max_wallclock_seconds": 1 * 60 * 60,  # 1h walltime
    "max_memory_kb": 2000000,              # 2GB memory
    "queue_name": "molsim",                # slurm partition to use
    "withmpi": False,                      # we run in serial mode
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

When the submission script is ready, submit it to the AiiDA daemon:

```terminal
$ verdi run raspa_loading.py
```
> **Note**  
> By default, the daemon polls for new calculations every 30 seconds,
> i.e. you may need to wait up to 30 seconds before your calculation starts running.

Use `verdi calculation list -a` to monitor the state of the calculation.
Once running, the calculation should finish within 5 minutes.

## Analyzing your results

Once the calculation shows up as `FINISHED`, have a look at the result.

Raspa produces two types of output: Outputs related to the whole system (e.g. total energy, temperature) and outputs related to the component -- in our case, there is only one component: methane.

Find the `component_0` output of the calculation and use `verdi data parameter
show` to extract the average and standard deviation of the absolute methane
loading.

---
### Exercise

What is the relative standard deviation of the loading?
How could you decrease it?

Re-run the calculation with adapted settings in order to decrease the
relative standard deviation below 5%

---
