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
         "NumberOfCycles"                : <int>,
         "NumberOfInitializationCycles"  : <int>,
         "PrintEvery"                    : 100,

         "CutOff"                        : 12.0,

         "Forcefield"                    : "UFF-TraPPE",
         "ChargeMethod"                  : "None",
         "UnitCells"                     : "<int> <int> <int>",

         "ExternalTemperature"           : <float (K)>,
         "ExternalPressure"              : <float (Pa)>,
    },
    "Component": [{
         "MoleculeName"                  : "methane",
         "MoleculeDefinition"            : "TraPPE",
         "MolFraction"                   : "TraPPE",
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

## Submitting the calculation

To start please [download the AiiDA submission script]({{ site.baseurl}}/assets/2019_molsim_school_Amsterdam/test_raspa.py). To
launch a calculation, you will need to interact with AiiDA mainly in the
<span>`verdi shell`</span>. We strongly suggest you to first try the
commands in the shell, and then copy them in a script “test\_pw.py”
using a text editor. This will be very useful for later execution of a
similar series of commands.

**The best way to run python scripts using AiiDA functionalities is to
run them in a terminal by means of the command**

```terminal
$ verdi run <scriptname>
```

Every calculation sent to a cluster is linked to a code, which describes
the executable file to be used. Therefore, first load the suitable code:

```python
from aiida.common.example_helpers import test_and_get_code 
code = test_and_get_code(codename, expected_code_type='raspa')
```

Here `test_and_get_code` is an AiiDA function handling all possible
codes, and `code` is a class instance provided as `codename` (see the
first part of the tutorial for listing all codes installed in your AiiDA
machine). For this example use codename `raspa@bazis`.

AiiDA calculations are instances of the class `Calculation`, more
precisely of one of its subclasses, each corresponding to a code
specific plugin (for example, the Raspa plugin). We create a new
calculation using the `new_calc` method of the `code` object:

```python
calc = code.new_calc()
```

This creates and initializes an instance of the `RaspaCalculation`
class, the subclass associated with the `raspa` plugin. Sometimes, you might find convenient to annotate
information assigning a (short) label or a (long) description, like:

```python
calc.label='Raspa test'
calc.description='My first AiiDA calc with Raspa'
```

This information will be saved in the database for later query or
inspection.

Now you have to specify the number of machines (a.k.a. cluster nodes)
you are going to run on and the maximum time allowed for the calculation
— this information is passed to the scheduler that handles the queue:

```python
calc.set_resources('num_machines': 1, 'num_mpiprocs_per_machine':1)
calc.set_max_wallclock_seconds(30*60)
```


> **Note**  
> Once running, the calculation should finish within 5 minutes.

