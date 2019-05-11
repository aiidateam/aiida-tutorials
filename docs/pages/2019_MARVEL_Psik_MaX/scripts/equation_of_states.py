# -*- coding: utf-8 -*-
from __future__ import absolute_import
from aiida.engine import WorkChain, ToContext, calcfunction
from aiida.orm import Code, Dict, Float, Str, StructureData
from aiida.plugins import CalculationFactory

from .create_rescale import create_diamond_fcc, rescale
from .common_wf import generate_scf_input_params
from six.moves import zip

PwCalculation = CalculationFactory('quantumespresso.pw')
scale_facs = (0.96, 0.98, 1.0, 1.02, 1.04)
labels = ['c1', 'c2', 'c3', 'c4', 'c5']


@calcfunction
def get_eos_data(**kwargs):
    eos = [(result.dict.volume, result.dict.energy, result.dict.energy_units)
           for label, result in kwargs.items()]
    return Dict(dict={'eos': eos})


class EquationOfStates(WorkChain):
    @classmethod
    def define(cls, spec):
        super(EquationOfStates, cls).define(spec)
        spec.input('code', valid_type=Code)
        spec.input('element', valid_type=Str)
        spec.input('pseudo_family', valid_type=Str)
        spec.output('initial_structure', valid_type=StructureData)
        spec.output('eos', valid_type=Dict)
        spec.outline(
            cls.run_eos,
            cls.results,
        )

    def run_eos(self):
        # Create basic structure and attach it as an output
        initial_structure = create_diamond_fcc(self.inputs.element)
        self.out('initial_structure', initial_structure)

        calculations = {}

        for label, factor in zip(labels, scale_facs):

            structure = rescale(initial_structure, Float(factor))
            inputs = generate_scf_input_params(structure, self.inputs.code,
                                               self.inputs.pseudo_family)

            self.report(
                'Running an SCF calculation for {} with scale factor {}'.
                format(self.inputs.element, factor))
            future = self.submit(PwCalculation, **inputs)
            calculations[label] = future

        # Ask the workflow to continue when the results are ready and store them in the context
        return ToContext(**calculations)

    def results(self):
        inputs = {
            label: self.ctx[label].get_outgoing().get_node_by_label(
                'output_parameters')
            for label in labels
        }
        eos = get_eos_data(**inputs)

        # Attach Equation of State results as output node to be able to plot the EOS later
        self.out('eos', eos)
