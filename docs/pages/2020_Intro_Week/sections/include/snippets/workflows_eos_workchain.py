# -*- coding: utf-8 -*-
"""Equation of State WorkChain."""
from aiida.engine import WorkChain, ToContext, calcfunction
from aiida.orm import Code, Dict, Float, Str, StructureData
from aiida.plugins import CalculationFactory

from rescale import rescale
from common_wf import generate_scf_input_params

PwCalculation = CalculationFactory('quantumespresso.pw')
scale_facs = (0.96, 0.98, 1.0, 1.02, 1.04)
labels = ['c1', 'c2', 'c3', 'c4', 'c5']


@calcfunction
def get_eos_data(**kwargs):
    """Store EOS data in Dict node."""
    eos = [(result.dict.volume, result.dict.energy, result.dict.energy_units)
           for label, result in kwargs.items()]
    return Dict(dict={'eos': eos})


class EquationOfState(WorkChain):
    """WorkChain to compute Equation of State using Quantum Espresso."""

    @classmethod
    def define(cls, spec):
        """Specify inputs and outputs."""
        super(EquationOfState, cls).define(spec)
        spec.input('code', valid_type=Code)
        spec.input('pseudo_family', valid_type=Str)
        spec.input('initial_structure', valid_type=StructureData)
        spec.output('eos', valid_type=Dict)
        spec.outline(
            cls.run_eos,
            cls.results,
        )

    def run_eos(self):
        """Run calculations for equation of state."""
        # Create basic structure and attach it as an output
        initial_structure = self.inputs.initial_structure

        calculations = {}

        for label, factor in zip(labels, scale_facs):

            structure = rescale(initial_structure, Float(factor))
            inputs = generate_scf_input_params(structure, self.inputs.code,
                                               self.inputs.pseudo_family)

            self.report(
                'Running an SCF calculation for {} with scale factor {}'.
                format(initial_structure.get_formula(), factor))
            future = self.submit(PwCalculation, **inputs)
            calculations[label] = future

        # Ask the workflow to continue when the results are ready and store them in the context
        return ToContext(**calculations)

    def results(self):
        """Process results."""
        inputs = {
            label: self.ctx[label].get_outgoing().get_node_by_label(
                'output_parameters')
            for label in labels
        }
        eos = get_eos_data(**inputs)

        # Attach Equation of State results as output node to be able to plot the EOS later
        self.out('eos', eos)
