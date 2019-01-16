# Screening

In order to compute the deliverable capacity of a material, you need to compute the
methane loading both at the loading and at the discharge pressure,
and then do some simple math - in other words, a simple *workflow*.

AiiDA provides [WorkChains](https://aiida-core.readthedocs.io/en/stable/work/index.html#workchains)
 to orchestrate the running of calculations.  
We've prepared a WorkChain to compute the deliverable methane capacity, download it 
[from here]({{ site.baseurl}}/assets/2019_molsim_school_Amsterdam/deliverable_capacity.py). 

In the following, we will go through each step of the WorkChain.
Your task will be to write a script to run the WorkChain for each of your candidate structures.


## Step 0: define inputs, outputs and the steps
First, when setting up the class one should define the list of input types using spec.input()
function. 

In our case the workflow takes as an input the following objects:
1. CifData object (named `structure`)
2. Zeo++ and Raspa parameters (`zeopp_parameters` and `raspa_parameters` of type `ParameterData`)
3. A file with atomic radii (`atomic_radii` of type `SingleFile`)
4. Zeo++ and Raspa codes (`zeopp_code` and `raspa_code` of type `Code`).

```python
class DcMethane(WorkChain):
    """Compute methane deliverable capacity for a given structure."""

    @classmethod
    def define(cls, spec):
        """Define workflow specification.
        
        This is the most important method of a Workchain, which defines the
        inputs it takes, the logic of the execution and the outputs
        that are generated in the process.
        """
        super(DcMethane, cls).define(spec)

        # First we define the inputs, specifying the type we expect

        spec.input("structure", valid_type=CifData, required=True)
        spec.input(
            "zeopp_parameters", valid_type=NetworkParameters, required=True)
        spec.input("raspa_parameters", valid_type=ParameterData, required=True)
        spec.input("atomic_radii", valid_type=SingleFile, required=True)
        spec.input("zeopp_code", valid_type=Code, required=True)
        spec.input("raspa_code", valid_type=Code, required=True)

        # The outline describes the basic logic that defines
        # which steps are executed in what order and based on
        # what conditions. Each `cls.method` is implemented below
        spec.outline(
            cls.init,
            cls.run_block_zeopp,
            cls.run_loading_raspa_low_p,
            cls.parse_loading_raspa,
            cls.run_loading_raspa_high_p,
            cls.parse_loading_raspa,
            cls.extract_results,
        )

        # Here we define the output the Workchain will generate and
        # return. Dynamic output allows a variety of AiiDA data nodes
        # to be returned
        spec.dynamic_output()
```

Using the spec.outline() function we specify the steps of the workchain.
All **7 steps** will be executed consequently. 

The outputs of the workchain can be specified either using `spec.output()` function, in case 
we want to keep a fixed list of the output parameters. Otherwise we call `spec.dynamic_output()`
emphasizing any number of AiiDA object can be outputed.

Now, we shift our focus to every step of the `DcMethane` workchain and will try understand them better.

## Step 1: Prepare input parameters and variables

   ```python
    def init(self):
        """Initialize variables."""

        self.ctx.loading_average = {}
        self.ctx.loading_dev = {}

        self.ctx.options = {
            "resources": {
                "num_machines": 1,
                "tot_num_mpiprocs": 1,
                "num_mpiprocs_per_machine": 1,
            },
            "max_wallclock_seconds": 4 * 60 * 60,
            "max_memory_kb": 2000000,
			"queue_name": "molsim",
            "withmpi": False,
        }
   ```
Please notice the usage of the **context** (`self.ctx`) variable -- a container that is accesible
along the whole life of the `DcMethane` workchain. Using `self.ctx` we can
pass information to the other steps of it.

In this particular case we are
creating two empty dictionaries to store the loading average and its deviation 
at different pressures. We also specify the code options that will be used by every calculation:


## Step 2: Compute the geometric parameters of the MOFs.


* `BlockPockets` and `BlockPocketsFileName` will be filled by AiiDA: if Zeo++ finds
some non accessible pore volume, it can generate a .block file with the positions
and the radii of blocking spheres. These spheres are inserted in the framework to prevent
Raspa from inserting molecules in the non accessible pore.



Here we will compute blocked pockets of a particular material employing the Zeo++ code.
```python
    def run_block_zeopp(self):
        """This function will perform a zeo++ calculation to obtain the blocked pockets."""

        # Create the input dictionary
        inputs = {
            'code': self.inputs.zeopp_code,
            'structure': self.inputs.structure,
            'parameters': self.inputs.zeopp_parameters,
            'atomic_radii': self.inputs.atomic_radii,
            '_options': self.ctx.options,
        }

        # Create the calculation process and launch it
        process = ZeoppCalculation.process()
        future = submit(process, **inputs)
        self.report("pk: {} | Running Zeo++ to obtain blocked pockets".format(
            future.pid))

        return ToContext(zeopp=Outputs(future))
```
As you can see: in order to run the calculation one just needs to provide code, structure,
parameters and atomic\_radii file that are all directly taken from the workflow inputs. The
job submission happens in exactly the same way as it was for the [single raspa calculation]({{site.baseurl}}/pages/2019_molsim_school_Amsterdam/screening/methane-loading#submitting-the-calculation)
that we tried previously.

A new function that you may notice in this step is the `self.report()` that provides a report message, a 
convinient way to monitor the stage of the workflow. 

## Step 3, 5: Compute the methane loading 
Steps 3 (`run_loading_raspa_low_p`) and 5 (`run_loading_raspa_high_p`) compute the methane loading at 5.8 and 65 bars respectively in [molecules/cell] units.
The functions are defined as follows:

```python
    def run_loading_raspa_low_p(self):
        self.ctx.current_pressure = 5.8e5
        self.ctx.current_pressure_label = "low"
        return self._run_loading_raspa()

    def run_loading_raspa_high_p(self):
        self.ctx.current_pressure = 65e5
        self.ctx.current_pressure_label = "high"
        return self._run_loading_raspa()
```
Since the same calculation is performed twice in this workchain, we put the common part of those steps into a separate function:

```python
    def _run_loading_raspa(self):
        """Perform raspa calculation at given pressure.
        
        Most of the runtime will be spent in this function.
        """
        # Create the input dictionary
        inputs = {
            'code': self.inputs.raspa_code,
            'structure': self.inputs.structure,
            'parameters': update_raspa_parameters(self.inputs.raspa_parameters,
                Float(self.ctx.current_pressure)),
            'block_component_0': self.ctx.zeopp['block'],
            '_options': self.ctx.options,
        }

        # Create the calculation process and launch it
        process = RaspaCalculation.process()
        future = submit(process, **inputs)
        self.report("pk: {} | Running raspa for the pressure {} [bar]".format(
            future.pid, self.ctx.current_pressure / 1e5))

        return ToContext(raspa=Outputs(future))
```

Again, please notice here the usage of the **context**. Thanks to it the results
computed by raspa will be available in every part of the workchain. In this particular
case `ToContext()` will create a variable `self.ctx.raspa` that will contain the results
of the calculation. `Outputs()` function will wait fot the calculation to be completed.


## Step 4, 6: Extract pressure and methane loading

Steps 4 and 6 extract pressure and methane loading (with deviation) and puts them into
`loading_average` and `loading_dev` dictionaries stored in the **context**.

```python
        """Extract pressure and loading average of last completed raspa calculation."""
        loading_average = self.ctx.raspa[
            "component_0"].dict.loading_absolute_average
        loading_dev = self.ctx.raspa[
            "component_0"].dict.loading_absolute_dev
        self.ctx.loading_average[self.ctx.
                                 current_pressure_label] = loading_average
        self.ctx.loading_dev[self.ctx.
                                 current_pressure_label] = loading_dev
```


## Step 7: Store the selected computed parameters as the output node
This final step is to prepare the results of the `DcMethane` workchain extracting the
most relevant information and putting it in a `ParameterData` object (the AiiDA way to store
python dictionaries).

In particular, we extract the deliverable capacities at low and high pressures
that are computed in previous steps. We transform data from [molecule/unit cell] units
to [cm^3\_STP/cm^3] using the conversion factor provided by raspa (`conversion_factor_molec_uc_to_cm3stp_cm3`).
We also compute the standard deviation of the deliverable capacity assuming loading averages to be
[independent normally distributed random variables](https://en.wikipedia.org/wiki/Sum_of_normally_distributed_random_variables).

```python
    def extract_results(self):
        """Extract results of the workflow.
        
        Attaches the results of the raspa calculation and the initial structure to the outputs.
        """
        from math import sqrt
        cf = self.ctx.raspa["component_0"].dict.conversion_factor_molec_uc_to_cm3stp_cm3
        dc = self.ctx.loading_average["high"] - self.ctx.loading_average["low"]
        dc_dev = sqrt(self.ctx.loading_dev["high"]**2 + self.ctx.loading_dev["low"]**2)

        result = {
            "deliverable_capacity": dc * cf,
            "deliverable_capacity_units": "cm^3_STP/cm^3",
            "deliverable_capacity_dev":  dc_dev * cf,
            "loading_absolute_average_low_p" : self.ctx.loading_average["low"] * cf,
            "loading_absolute_dev_low_p" : self.ctx.loading_dev["low"] * cf,
            "loading_units" : "cm^3_STP/cm^3", 
            "loading_absolute_average_high_p" : self.ctx.loading_average["high"] * cf,
            "loading_absolute_dev_high_p" : self.ctx.loading_dev["high"] * cf,
        }
        self.out("result", ParameterData(dict=result))

        self.report("Workchain <{}> completed successfully".format(
            self.calc.pk))
        return
```
We pack our results into the `result` object of type `ParameterData` and set it as the input of the WorkChain.

## Exercises

1. Before you actually start doing the calculations please setup the zeo++ code as shown here:

   ```terminal
    * PK:             60109
    * UUID:           8a37224a-1247-4484-b3c8-ce3e8f37cee7
    * Label:          zeopp
    * Description:    zeo++ code for the molsim course
    * Default plugin: zeopp.network
    * Used by:        1 calculations
    * Type:           remote
    * Remote machine: bazis
    * Remote absolute path: 
      /home/molsim20/network
    * prepend text:
      # No prepend text.
    * append text:
      # No append text.
   ```
   Should you have any doubts, just consult the
   [Computer setup and configuration]({{ site.baseurl}}/pages/2019_molsim_school_Amsterdam/screening/calculations#computer-setup-and-configuration) part of our tutorial.

 
2. Adapt the following script and submit the `DcMethane` workchain.  
 

   ```python
   from aiida.backends.utils import load_dbenv, is_dbenv_loaded
   if not is_dbenv_loaded():
           load_dbenv()
   
   import os
   import sys
   import time
   from deliverable_capacity import DcMethane
   
   from aiida.orm import DataFactory
   from aiida.orm.data.cif import CifData
   from aiida.orm.data.base import Float
   from aiida.work.run import run, submit
   
   NetworkParameters = DataFactory('zeopp.parameters')
   ParameterData = DataFactory('parameter')
   
   
   cutoff = <float (A)>
   probe_radius = <float (A)>
   
   zeopp_params = NetworkParameters(dict={
       'ha': True,
       'block': [probe_radius, 100],
   })
       
   raspa_params = ParameterData(dict={
       "GeneralSettings":
       {
       "SimulationType"                   : "MonteCarlo",
       "NumberOfCycles"                   : <int>,  
       "NumberOfInitializationCycles"     : <int>, 
       "PrintEvery"                       : <int>,
   
       "CutOff"                           : cutoff,
   
       "Forcefield"                       : "UFF-TraPPE",
       "ChargeMethod"                     : "None",
       "UnitCells"                        : "<int> <int> <int>",
       "ExternalTemperature"              : <float (K)>,
   
       },
       "Component":
       [{
       "MoleculeName"                     : "methane",
       "MoleculeDefinition"               : "TraPPE",
       "MolFraction"                      : 1.0,
       "TranslationProbability"           : <float>, # between 0 and 1
       "RotationProbability"              : <float>, # between 0 and 1
       "ReinsertionProbability"           : <float>, # between 0 and 1
       "SwapProbability"                  : <float>, # between 0 and 1
       "CreateNumberOfMolecules"          : 0,
       }],
   })
   
   q = QueryBuilder()
   q.append(CifData, filters={}) # find a way to specify particular Structures
   for item in q.all():
       cif = item[0]
       print (cif)
       outputs = submit(
               DcMethane,
               structure=cif,
               zeopp_parameters = zeopp_params,
               raspa_parameters = raspa_params,
               atomic_radii = load_node('27d2af72-3af0-48a6-a563-24d1d6d6eb60'), # already present in your database
               zeopp_code=Code.get_from_string('zeopp@bazis1'),
               raspa_code=Code.get_from_string('raspa@bazis1'),
           )
       time.sleep(40)
   ```
   
   In order to automatically determine how many unit cells to use in the simulation (`UnitCells` input parameter), you may employ
   [this function]({{ site.baseurl}}/assets/2019_molsim_school_Amsterdam/multiply_unitcell.py) for your convenience. The function takes as the input parameter a `CifData`
   object and a cutoff of the intermolecular interactions.
   
   > **Note**    
   > The file containing the `DcMethane` workchain should be accessible
   > from the python shell. To achieve that just place the file into a folder
   > listed in `PYTHONPATH` system variable and rename it to
   > `deliverable_capacity.py`.
   > In case you want to place the python file in your own directory, just add
   > the path to it into `PYTHONPATH` variable running
   > ```terminal
   >    $ export PYTHONPATH=/path/to/your/directory/:$PYTHONPATH
   > ```
   > and do not forget to restart the AiiDA daemon **in the same shell**
   > ```terminal
   >    $ verdi daemon restart
   > ```
   
   Consult the [Querying the AiiDA database]({{ site.baseurl}}/pages/2019_molsim_school_Amsterdam/tutorial/queries) part of the tutorial
   in order to find out which filter you should put in `q.append(CifData, filters={})` to select the appropriate
   structures.
