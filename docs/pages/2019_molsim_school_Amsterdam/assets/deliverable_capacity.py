from __future__ import absolute_import
from aiida.orm import CalculationFactory, DataFactory, Code
from aiida.orm.data.base import Float
from aiida.work import WorkChain, workfunction, submit
from aiida.work.workchain import ToContext, Outputs

CifData = DataFactory('cif')
ParameterData = DataFactory('parameter')
NetworkParameters = DataFactory('zeopp.parameters')
SingleFile = DataFactory('singlefile')
RaspaCalculation = CalculationFactory('raspa')
ZeoppCalculation = CalculationFactory('zeopp.network')

@workfunction
def update_raspa_parameters(parameters, pressure):
    """Store input parameters of Raspa for given pressure.
    
    Note: In order to keep the provenance of both Raspa calculations,
    changing the pressure force us to create a new ParameterData node.
    "workfunctions" will take care of linking the user-provided ParameterData
    node to the new one containing the pressure.
    """
    param_dict = parameters.get_dict()
    param_dict['GeneralSettings']['ExternalPressure'] = pressure.value
    return ParameterData(dict=param_dict)


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
        spec.input("atomic_radii", valid_type=SingleFile, required=True)
        spec.input("raspa_parameters", valid_type=ParameterData, required=True)
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

    def init(self):
        """Initialize variables."""

        self.ctx.loading_average = {}
        self.ctx.loading_dev = {}

        self.ctx.options = {
            "resources": {
                "num_machines": 1,                 # run on 1 node
                "tot_num_mpiprocs": 1,             # use 1 process
                "num_mpiprocs_per_machine": 1,
            },
            "max_wallclock_seconds": 4 * 60 * 60,  # 1h walltime
            "max_memory_kb": 2000000,              # 2GB memory
            "queue_name": "molsim",                # slurm partition to use
            "withmpi": False,                      # we run in serial mode
        }

    def run_block_zeopp(self):
        """This function will perform a zeo++ calculation to block inaccessible pockets."""

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

    def run_loading_raspa_low_p(self):
        self.ctx.current_pressure = 5.8e5
        self.ctx.current_pressure_label = "low"
        return self._run_loading_raspa()

    def run_loading_raspa_high_p(self):
        self.ctx.current_pressure = 65e5
        self.ctx.current_pressure_label = "high"
        return self._run_loading_raspa()

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

    def parse_loading_raspa(self):
        """Extract pressure and loading average of last completed raspa calculation."""
        loading_average = self.ctx.raspa[
            "component_0"].dict.loading_absolute_average
        loading_dev = self.ctx.raspa[
            "component_0"].dict.loading_absolute_dev
        self.ctx.loading_average[self.ctx.
                                 current_pressure_label] = loading_average
        self.ctx.loading_dev[self.ctx.
                                 current_pressure_label] = loading_dev

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
