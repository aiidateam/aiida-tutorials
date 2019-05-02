from aiida.orm import CalculationFactory, DataFactory
from aiida.orm import Float, Str, StructureData
from aiida.engine import run, submit, WorkChain, ToContext, while_
from common_wf import generate_scf_input_params
from create_rescale import rescale, create_diamond_fcc

PwCalculation = CalculationFactory('quantumespresso.pw')


def run_eos(structure, element="Si", code='qe-pw-6.2.1@localhost', pseudo_family='GBRV_lda'):
    return run(PressureConvergence, structure=structure, code=Str(code), pseudo_family=Str(pseudo_family), volume_tolerance=Float(0.1))


# Set up the factories
Dict = DataFactory('dict')
ParameterData = DataFactory('parameter')
KpointsData = DataFactory('array.kpoints')


def get_first_deriv(stress):
    """
    Return the energy first derivative from the stress
    """
    from numpy import trace

    GPa_to_eV_over_ang3 = 1. / 160.21766208

    # Get the pressure (GPa)
    p = trace(stress) / 3.

    # Pressure is -dE/dV; moreover p in kbar, we need to convert it to eV/angstrom^3 to be consistent
    dE = -p * GPa_to_eV_over_ang3
    return dE


def get_volume_energy_and_derivative(output_parameters):
    """
    Given the output parameters of the pw calculation,
    return the volume (ang^3), the energy (eV), and the energy
    derivative (eV/ang^3)
    """
    V = output_parameters.dict.volume
    E = output_parameters.dict.energy
    dE = get_first_deriv(output_parameters.dict.stress)

    return (V, E, dE)


def get_second_derivative(outp1, outp2):
    """
    Given the output parameters of the two pw calculations,
    return the second derivative obtained from finite differences
    from the pressure of the two calculations (eV/ang^6)
    """
    dE1 = get_first_deriv(outp1.dict.stress)
    dE2 = get_first_deriv(outp2.dict.stress)
    V1 = outp1.dict.volume
    V2 = outp2.dict.volume
    return (dE2 - dE1) / (V2 - V1)


def get_abc(V, E, dE, ddE):
    """
    Given the volume, energy, energy first derivative and energy
    second derivative, return the a,b,c coefficients of
    a parabola E = a*V^2 + b*V + c
    """
    a = ddE / 2.
    b = dE - ddE * V
    c = E - V * dE + V**2 * ddE / 2.

    return a, b, c


def get_structure(original_structure, new_volume):
    """
    Given a structure and a new volume, rescale the structure to the new volume
    """
    initial_volume = original_structure.get_cell_volume()
    scale_factor = (new_volume / initial_volume)**(1. / 3.)
    scaled_structure = rescale(original_structure, Float(scale_factor))
    return scaled_structure


class PressureConvergence(WorkChain):
    """
    Converge to minimum using Newton's algorithm on the first derivative of the energy (minus the pressure).
    """

    @classmethod
    def define(cls, spec):
        super(PressureConvergence, cls).define(spec)
        spec.input('structure', valid_type=StructureData)
        spec.input('volume_tolerance', valid_type=Float)
        spec.input('code', valid_type=Str)
        spec.input('pseudo_family', valid_type=Str)
        spec.outline(
            cls.setup,
            cls.put_step0_in_ctx,
            cls.move_next_step,
            while_(cls.not_converged)(
                cls.move_next_step,
            ),
            cls.finish
        )

    def setup(self):
        """
        Launch the first calculation for the input structure,
        and a second calculation for a shifted volume (increased by 4 angstrom^3)
        Store the outputs of the two calcs in r0 and r1
        """
        print "Workchain node identifiers: {}".format(self.calc)

        inputs0 = generate_scf_input_params(
            self.inputs.structure, str(self.inputs.code), self.inputs.pseudo_family)

        initial_volume = self.inputs.structure.get_cell_volume()
        new_volume = initial_volume + 4.  # In ang^3

        scaled_structure = get_structure(self.inputs.structure, new_volume)
        inputs1 = generate_scf_input_params(
            scaled_structure, str(self.inputs.code), self.inputs.pseudo_family)

        self.ctx.last_structure = scaled_structure

        # Run PW
        future0 = submit(PwCalculation, **inputs0)
        future1 = submit(PwCalculation, **inputs1)

        # Wait to complete before next step
        return ToContext(r0=future0, r1=future1)

    def put_step0_in_ctx(self):
        """
        Store the outputs of the very first step in a specific dictionary
        """
        V, E, dE = get_volume_energy_and_derivative(self.ctx.r0.get_outputs_dict()['output_parameters'])

        self.ctx.step0 = {'V': V, 'E': E, 'dE': dE}

        # Prepare the list containing the steps
        # step 1 will be stored here by move_next_step
        self.ctx.steps = []

    def move_next_step(self):
        """
        Main routine that reads the two previous calculations r0 and r1,
        uses the Newton's algorithm on the pressure (i.e., fits the results
        with a parabola and sets the next point to calculate to the parabola
        minimum).
        r0 gets replaced with r1, r1 will get replaced by the results of the
        new calculation.
        """
        r0_out = self.ctx.r0.get_outputs_dict()
        r1_out = self.ctx.r1.get_outputs_dict()
        ddE = get_second_derivative(r0_out['output_parameters'], r1_out['output_parameters'])
        V, E, dE = get_volume_energy_and_derivative(r1_out['output_parameters'])
        a, b, c = get_abc(V, E, dE, ddE)

        new_step_data = {'V': V, 'E': E, 'dE': dE, 'ddE': ddE, 'a': a, 'b': b, 'c': c}
        self.ctx.steps.append(new_step_data)

        # Minimum of a parabola
        new_volume = -b / 2. / a

        # remove older step
        self.ctx.r0 = self.ctx.r1
        scaled_structure = get_structure(self.inputs.structure, new_volume)
        self.ctx.last_structure = scaled_structure

        inputs = generate_scf_input_params(
            scaled_structure, str(self.inputs.code), self.inputs.pseudo_family)

        # Run PW
        future = submit(PwCalculation, **inputs)
        # Replace r1
        return ToContext(r1=future)

    def not_converged(self):
        """
        Return True if the worflow is not converged yet (i.e., the volume changed significantly)
        """
        r0_out = self.ctx.r0.get_outputs_dict()
        r1_out = self.ctx.r1.get_outputs_dict()

        return abs(r1_out['output_parameters'].dict.volume -
                   r0_out['output_parameters'].dict.volume) > self.inputs.volume_tolerance

    def finish(self):
        """
        Output final quantities
        """
        self.out('steps', Dict(dict={'steps': self.ctx.steps, 'step0': self.ctx.step0}))
        self.out('structure', self.ctx.last_structure)


if __name__ == '__main__':
    structure = create_diamond_fcc(element=Str('Si'))
    wf_results = run_eos(structure=structure)
    print 'Initial structure:', structure
    print 'Workflow results:'
    print 'Final energies and fit parameters are stored in the Dict {}'.format(wf_results['steps'].pk)
    print 'The optimized structure is stored in StructureData with pk {}'.format(wf_results['structure'].pk)
