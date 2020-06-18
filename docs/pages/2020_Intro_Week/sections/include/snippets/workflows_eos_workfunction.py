# -*- coding: utf-8 -*-
"""Simple workflow example"""
from aiida.engine import run, Process, calcfunction, workfunction
from aiida.orm import Dict, Float
from aiida.plugins import CalculationFactory

from rescale import rescale
from common_wf import generate_scf_input_params

# Load the calculation class 'PwCalculation' using its entry point 'quantumespresso.pw'
PwCalculation = CalculationFactory('quantumespresso.pw')


@calcfunction
def create_eos_dictionary(**kwargs):
    """Create a single `Dict` node from the `Dict` output parameters of completed `PwCalculations`.

    The dictionary will contain a list of tuples, where each tuple contains the volume, total energy and its units
    of the results of a calculation.

    :return: `Dict` node with the equation of state results
    """
    eos = [(result.dict.volume, result.dict.energy, result.dict.energy_units)
           for label, result in kwargs.items()]
    return Dict(dict={'eos': eos})


@workfunction
def run_eos_wf(code, pseudo_family, structure):
    """Run an equation of state of a bulk crystal structure for the given element."""

    # This will print the pk of the work function
    print('Running run_eos_wf<{}>'.format(Process.current().pid))

    scale_factors = (0.96, 0.98, 1.0, 1.02, 1.04)
    labels = ['c1', 'c2', 'c3', 'c4', 'c5']

    calculations = {}

    # Loop over the label and scale_factor pairs
    for label, factor in list(zip(labels, scale_factors)):

        # Generated the scaled structure from the initial structure
        structure = rescale(structure, Float(factor))

        # Generate the inputs for the `PwCalculation`
        inputs = generate_scf_input_params(structure, code, pseudo_family)

        # Launch a `PwCalculation` for each scaled structure
        print('Running a scf for {} with scale factor {}'.format(
            structure.get_formula(), factor))
        calculations[label] = run(PwCalculation, **inputs)

    # Bundle the individual results from each `PwCalculation` in a single dictionary node.
    # Note: since we are 'creating' new data from existing data, we *have* to go through a `calcfunction`, otherwise
    # the provenance would be lost!
    inputs = {
        label: result['output_parameters']
        for label, result in calculations.items()
    }
    eos = create_eos_dictionary(**inputs)

    # Finally, return the eos Dict node
    return eos
