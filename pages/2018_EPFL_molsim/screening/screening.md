Screening
=========

For the screening part of the work, you can choose one of two possible
routes:

1.  **Quick and simple:** Use `for` loops in your scripts to loop over
    the structures in your database, submitting in total
    1 (Zeo++) + 2 (Raspa) = 3 calculations per structure.

    This should require very little changes to your python scripts and
    is a perfectly valid solution.

2.  **Reusable and elegant:** Write an AiiDA `Workchain` that takes a
    structure, performs all necessary calculations, and outputs the
    result.

    This route requires more advanced python concepts and involves a bit
    of coding, but makes your workflow more robust and reusable.

Quick and simple
----------------

Just use the `QueryBuilder` to load the `CifData` nodes from the AiiDA
database and loop over them.

Computed properties are automatically linked to `CifData` nodes via
calculation nodes.

Try `verdi graph generate <PK>` on a zeo++ or RASPA calculation node to
get an overview of the AiiDA graph.

In order to automatically determine how many unit cells to use in the
simulation, you may use the following function for convenience:

```python
def multiply_cell(cif, cutoff):
     """ Determine number of replica of unit cell.

     Works for cells of arbitrary shape.

     :param cif:  CifData object
     :param cutoff:  cutoff radius of interaction
     :returns:  String of integers specifying replica of unit cell,
                suitable for 'UnitCells' parameter of raspa calculation.
     """
     from math import cos, sin, sqrt, pi
     import numpy as np
     deg2rad=pi/180.

     struct = cif.values.dictionary.itervalues().next()

     a = float(struct['_cell_length_a']) 
     b = float(struct['_cell_length_b']) 
     c = float(struct['_cell_length_c'])

     alpha = float(struct['_cell_angle_alpha'])*deg2rad 
     beta = float(struct['_cell_angle_beta'])*deg2rad 
     gamma = float(struct['_cell_angle_gamma'])*deg2rad

     # compute cell vectors following https://en.wikipedia.org/wiki/Fractional_coordinates 
     v = sqrt(1-cos(alpha)**2-cos(beta)**2- cos(gamma)**2+2*cos(alpha)*cos(beta)*cos(gamma))
     cell=np.zeros((3,3))
     cell[0,:] = [a, 0, 0]
     cell[1,:] = [b*cos(gamma), b*sin(gamma),0]
     cell[2,:] = [c*cos(beta), c*(cos(alpha)-cos(beta)*cos(gamma))/(sin(gamma)),
                  c*v /sin(gamma)]
     cell=np.array(cell)

     # diagonalize the cell matrix
     diag = np.diag(cell)
     # and computing nx, ny and nz
     nx, ny, nz = tuple(int(i) for i in np.ceil(cutoff/diag*2.))

     #return nx, ny, nz
     return "{} {} {}".format(nx, ny, nz)
```


Elegant and robust
------------------

Combine the calculations into a workchain using the AiiDA `WorkChain`
class. Here one should define the list of input types using spec.input()
function and the workflow steps using spec.outline() function. In our
case the workflow takes as input CifData object with structure and the
names of Zeo++ and Raspa codes.


```python
class DcMethane(WorkChain):
     """ Compute deliverable capacity for methane. """

     @classmethod
     def define(cls, spec):
         """ Define input, logic and output of Workchain. """
         super(DcMethane, cls).define(spec)

         # First we define the inputs, specifying the type we expect
         spec.input("structure", valid_type=CifData, required=True)
         spec.input("zeopp_codename", valid_type=Str, required=True)
         spec.input("raspa_codename", valid_type=Str, required=True)

         # The outline describes the business logic that defines
         # which steps are executed in what order and based on
         # what conditions. We will implement each `cls.method` below 
         spec.outline(
             cls.init,
             cls.run_geom_zeopp,
             cls.run_loading_raspa_5_8,
             cls.parse_loading_raspa,
             cls.run_loading_raspa_65,
             cls.parse_loading_raspa,
             cls.extract_results,
        )

         # Here we define the output the Workchain will generate and
         # return. Dynamic output allows a variety of AiiDA data nodes
         # to be returned
         spec.dynamic_output()
```
             
The workchain consists of **7 steps**. 

### Step 1: Prepare input parameters and variables

   ```python
   def init(self):
        """
        Initialize variables
        """
        # Define cutoff for the methane-methane interactions
        cutoff = 12.00

        self.ctx.loading_average = {}

        self.ctx.parameters = {<adapt the parameters dictionary defined in the section 3>}
        # Note: You'll need the multiply_cell function mentioned in section 4.1

        self.ctx.options = {
            "resources": {
                "num_machines": 1,
                "tot_num_mpiprocs": 1,
                "num_mpiprocs_per_machine": 1,
            },
            "max_wallclock_seconds": 10 * 60 * 60, # 10 hours
            "max_memory_kb": 2000000, # limiting the
            "withmpi": False,
   }
   ```

### Step 2: Compute the geometric parameters of the MOFs.  
Draw upon how we submitted Zeo++ calculations  in section 2. 
The main difference here is that the calculation inputs,
 such as Code or structure, are provided as a dictionary.

```python
def run_geom_zeopp(self):
    """ Perform a zeo++ calculation. """

    # Create the input dictionary
    NetworkParameters = DataFactory('zeopp.parameters') 
    sigma = 1.86
    params = {
        'ha': True,
        'res': True,
        'sa': [sigma, sigma, 100000], 
        'volpo': [sigma, sigma, 100000],
    }

    inputs = { 
        'code':        : Code.get_from_string(self.inputs.zeopp_codename.value), 
        'structure':   : self.inputs.structure,
        'parameters':  : NetworkParameters(dict=params),
        '_options':    : self.ctx.options,                                      
    }

    # Create the calculation process and launch it
    process = ZeoppCalculation.process()
    future  = submit(process, **inputs)
    self.report("pk: {} | Running geometry analysis with zeo++".format(future.pid))

    return ToContext(zeopp=Outputs(future))
 ```

### Step 3,5: Compute the methane loading 
Steps 3 and 5 compute the methane loading in units of [molecules/cell] at
5.8 and 65 bars respectively. Since the same calculation is performed twice
in this workchain, we put the common part of those steps into a function:

```python
def _run_loading_raspa(self, pressure):
    """ Perform a raspa calculation for one pressure. """
    self.ctx.parameters['GeneralSettings']['ExternalPressure'] = pressure

     # Create the input dictionary
     inputs = { 
         'code'       : Code.get_from_string(self.inputs.zeopp_codename.value),   
         'structure'  : self.inputs.structure,
         'parameters' : NetworkParameters(dict=params),
         '_options'   : self.ctx.options,                                        
    }
    
    # Create the calculation process and launch it
    process = RaspaCalculation.process()
    future = submit(process, **inputs)
    self.report("pk: {} | Running raspa for the pressure {} [bar]" \
        .format(future.pid, pressure/1e5)

    return ToContext(raspa=Outputs(future))
```

The `run_loading_raspa_5_8` and `run_loading_raspa_65` functions
are defined as follows:

```python
def run_loading_raspa_5_8(self):
    return self._run_loading_raspa(pressure = 5.8e5)

def run_loading_raspa_65(self):
     return self._run_loading_raspa(pressure = 6.5e6)
```

### Step 4,6: Extract pressure and methane loading

Steps 4 and 6 extract pressure and methane loading from the input and
output parameters of the calculation and put them into context (`ctx`)
that is used to store any data that should be persisted between step.

```python
def parse_loading_raspa(self):
     """ Extract the pressure and loading average of the last completed raspa calculation """
    pressure = self.ctx.parameters['GeneralSettings']['ExternalPressure'] 
    loading_average = self.ctx.raspa["component_0"].dict.loading_absolute_average 
    self.ctx.loading_average[str(int(pressure))] = loading_average
```


Last step stores the selected computed parameters as the output of the
`DcMethane` workchain:

```python
def extract_results(self):
     """ Attach the results of raspa calculation and the initial structure to the outputs """
     dc = self.ctx.loading_average['6500000'] - self.ctx.loading_average['580000']

     zeopp = self.ctx.zeopp
     res = {
         'density'                        : zeopp['pore_volume_volpo'].get_attr('Density'),
         'density_units'                  : 'g/cm^3',
         'pore_accesible_volume'          : zeopp['pore_volume_volpo'].get_attr('POAV_A^3'), 
         'pore_accesible_volume_units'    : 'A^3',
         'unitcell_volume'                : zeopp['pore_volume_volpo'].get_attr( 'Unitcell_volume'),
         'unitcell_volume_units'          : 'A^3',
         'largest_included_sphere'        : zeopp['free_sphere_res'].get_attr('Largest_included_sphere'), 
         'largest_included_sphere_units'  : 'A',
         'accessible_surface_area'        : zeopp['surface_area_sa'].get_attr('ASA_m^2/g'), 
         'accessible_surface_area_units'  : 'm^2/g',
         'deliverable_capacity'           : dc,
         'deliverable_capacity_units'     : 'molecules/unit cell',                                          
     }
     self.out("result",  ParameterData(dict=res))

    self.report("Workchain <{}> completed successfully".format(self.calc.pk)) 
    return
```

To submit the calculation please adapt the following script. Please
note, the file containing the `DcMethane` workchain should be accessible
from the python shell. To achieve that just place the file into a folder
listed in `PYTHONPATH` system variable and rename it to
`deliverable_capacity.py`.

```python
import os
from deliverable_capacity import DcMethane
from aiida.orm.data.cif import CifData
from aiida.orm.data.base import Str
from aiida.work.run import run, submit

for s in structures:
    outputs = submit(DcMethane, structure=s, 
        zeopp_codename=Str('zeopp@deneb-molsim'), raspa_codename=Str('raspa@deneb-molsim'),
    )
```

Where structures is the list of `CifData` nodes stored in your AiiDA
database.
