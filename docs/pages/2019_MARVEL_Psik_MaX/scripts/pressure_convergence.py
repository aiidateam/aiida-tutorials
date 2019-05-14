# -*- coding: utf-8 -*-
"""Pressure convergence WorkChain"""
from __future__ import absolute_import
from __future__ import print_function
from aiida.engine import WorkChain, ToContext, while_, calcfunction, workfunction
from aiida.orm import Code, Float, Str, StructureData
from aiida.plugins import CalculationFactory, DataFactory

from common_wf import generate_scf_input_params
from create_rescale import rescale

Dict = DataFactory('dict')
KpointsData = DataFactory('array.kpoints')
PwCalculation = CalculationFactory('quantumespresso.pw')


def get_energy_first_derivative(stress):
    """Return the energy first derivative from the stress.

    :param stress: the stress tensor in GPa
    :return: first derivative of the energy in eV/Å^3
    """
    from numpy import trace

    GPa_to_eV_over_ang3 = 1. / 160.21766208

    # Get the pressure (GPa)
    pressure = trace(stress) / 3.

    # Pressure is -dE/dV; moreover p in kbar, we need to convert it to eV/Å^3 to be consistent
    dE = -pressure * GPa_to_eV_over_ang3

    return dE


def get_volume_energy_and_derivative(output_parameters):
    """Return the volume, energy and energy derivative for given `PwCalculation` output parameters.

    Volume is in Å^3, energy in eV and energy derivative eV/Å^3

    :param output_parameters: the `output_parameters` `Dict` result node of a `PwCalculation`
    :return: tuple with volume, energy and energy derivative
    """
    V = output_parameters.dict.volume
    E = output_parameters.dict.energy
    dE = get_energy_first_derivative(output_parameters.dict.stress)

    return V, E, dE


def get_energy_second_derivative(output_parameters_one, output_parameters_two):
    """Return second derivative of the energy with respect to the volume given the results of two `PwCalculations`.

    The derivate is computed using the finite differences method.

    :param output_parameters_one: the `output_parameters` `Dict` result node of the first `PwCalculation`
    :param output_parameters_two: the `output_parameters` `Dict` result node of the second `PwCalculation`
    :return: the second derivative of the energy with respect to the volume
    """
    dE1 = get_energy_first_derivative(output_parameters_one.dict.stress)
    dE2 = get_energy_first_derivative(output_parameters_two.dict.stress)
    V1 = output_parameters_one.dict.volume
    V2 = output_parameters_two.dict.volume

    return (dE2 - dE1) / (V2 - V1)


def get_parabola_coefficients(V, E, dE, ddE):
    """Return coefficients of a parabola fit to E = a*V^2 + b*V + c for the given volume and energy.

    :param V: volume in Å^3
    :param E: energy in eV
    :param dE: the first derivative of the energy with respect to the volume
    :param ddE: the second derivative of the energy with respect to the volume
    :return: coefficients a, b and c
    """
    a = ddE / 2.
    b = dE - ddE * V
    c = E - V * dE + V**2 * ddE / 2.

    return a, b, c


@workfunction
def get_structure(structure, step_data=None):
    """Return a scaled version of the given structure, where the new volume is determined by the given step data."""
    initial_volume = structure.get_cell_volume()

    if step_data is None:
        new_volume = initial_volume + 4.  # In Å^3
    else:
        # Minimum of a parabola
        new_volume = -step_data.dict.b / 2. / step_data.dict.a

    scale_factor = (new_volume / initial_volume)**(1. / 3.)
    scaled_structure = rescale(structure, Float(scale_factor))
    return scaled_structure


@calcfunction
def get_step_data(parameters_first, parameters_second=None):
    """Generate a dictionary with the step parameters from the output parameters of a completed `PwCalculation`."""

    # If the parameters of the second calculation are not passed, this is for the first step and we only return
    # a dictionary with the volume, energy and derivative
    if parameters_second is None:
        V, E, dE = get_volume_energy_and_derivative(parameters_first)
        return Dict(dict={'V': V, 'E': E, 'dE': dE})

    # Otherwise, this is an iteration step and we return the difference between the steps
    V, E, dE = get_volume_energy_and_derivative(parameters_first)
    ddE = get_energy_second_derivative(parameters_first, parameters_second)
    a, b, c = get_parabola_coefficients(V, E, dE, ddE)

    return Dict(dict={
        'V': V,
        'E': E,
        'dE': dE,
        'ddE': ddE,
        'a': a,
        'b': b,
        'c': c
    })


@calcfunction
def bundle_step_data(step0, **kwargs):
    """Bundle step data into Dict."""
    steps = [step.get_dict() for step in kwargs.values()]
    print((step0, type(step0)))
    print((steps, type(steps)))
    return Dict(dict={'step0': step0.get_dict(), 'steps': steps})


class PressureConvergence(WorkChain):
    """Relax a structure using Newton's algorithm on the first derivative of the energy (minus the pressure)."""

    @classmethod
    def define(cls, spec):
        """Define spec of WorkChain."""
        # yapf: disable
        # pylint: disable=bad-continuation
        super(PressureConvergence, cls).define(spec)
        spec.input('code', valid_type=Code,
            help='Code setup to run `pw.x` to use for the calculations.')
        spec.input('structure', valid_type=StructureData,
            help='The structure to minimize.')
        spec.input('pseudo_family', valid_type=Str,
            help='Family of pseudopotentials to use for the calculations.')
        spec.input('volume_tolerance', valid_type=Float,
            help='Stop if the volume difference of two consecutive calculations is less than this threshold.')
        spec.output('steps', valid_type=Dict,
            help='The data of all the steps in the minimization process containing info about energy and volume')
        spec.output('structure', valid_type=StructureData,
            help='Final relaxed structure.')
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
        """Launch the first calculation for the input structure, and a second calculation for a shifted volume."""
        scaled_structure = get_structure(self.inputs.structure)
        self.ctx.last_structure = scaled_structure

        inputs0 = generate_scf_input_params(self.inputs.structure,
                                            self.inputs.code,
                                            self.inputs.pseudo_family)
        inputs1 = generate_scf_input_params(scaled_structure, self.inputs.code,
                                            self.inputs.pseudo_family)

        # Run two `PwCalculations`
        future0 = self.submit(PwCalculation, **inputs0)
        future1 = self.submit(PwCalculation, **inputs1)

        # Wait for them to complete before going to the next step
        return ToContext(r0=future0, r1=future1)

    def put_step0_in_ctx(self):
        """Store the outputs of the very first step in a specific dictionary."""
        self.ctx.step0 = get_step_data(self.ctx.r0.outputs.output_parameters)

        # Prepare the list containing the steps: step 1 will be stored here by move_next_step
        self.ctx.steps = []

    def move_next_step(self):
        """Main part of the algorithm.

        Compare the results of two consecutive calculations and use Newton's algorithm on the pressure by fitting the
        results with a parabola and setting the next volume to calculate to the parabola minimum.

        The oldest calculation gets replaced by the most recent and a new calculation is launched that will replace
        the most recent.
        """
        # Computer the new Volume using Newton's algorithm and create the new corresponding structure by scaling it
        new_step_data = get_step_data(self.ctx.r0.outputs.output_parameters,
                                      self.ctx.r1.outputs.output_parameters)
        scaled_structure = get_structure(self.inputs.structure, new_step_data)
        self.ctx.steps.append(new_step_data)

        # Replace the older step with the latest and set the current structure
        self.ctx.r0 = self.ctx.r1
        self.ctx.last_structure = scaled_structure

        inputs = generate_scf_input_params(scaled_structure, self.inputs.code,
                                           self.inputs.pseudo_family)
        future = self.submit(PwCalculation, **inputs)

        return ToContext(r1=future)

    def not_converged(self):
        """Return True if the worflow is not converged yet (i.e. the volume changed significantly)."""
        r0_out = self.ctx.r0.outputs.output_parameters
        r1_out = self.ctx.r1.outputs.output_parameters

        return abs(r1_out.dict.volume -
                   r0_out.dict.volume) > self.inputs.volume_tolerance

    def finish(self):
        """Attach the result nodes as outputs."""
        steps = {
            'step{}'.format(index + 1): step
            for index, step in enumerate(self.ctx.steps)
        }
        bundled_steps = bundle_step_data(step0=self.ctx.step0, **steps)

        self.out('steps', bundled_steps)
        self.out('structure', self.ctx.last_structure)
