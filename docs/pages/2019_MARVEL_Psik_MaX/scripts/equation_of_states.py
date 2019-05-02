from create_rescale import create_diamond_fcc, rescale
from common_wf import generate_scf_input_params
from aiida.work.workchain import WorkChain, ToContext
from aiida.work.run import run, submit
from aiida.orm.data.base import Str, Float
from aiida.orm import CalculationFactory, DataFactory

PwCalculation = CalculationFactory('quantumespresso.pw')

scale_facs = (0.96, 0.98, 1.0, 1.02, 1.04)
labels = ["c1", "c2", "c3", "c4", "c5"]

class EquationOfStates(WorkChain):
    @classmethod
    def define(cls, spec):
        super(EquationOfStates, cls).define(spec)
        spec.input("element", valid_type=Str)
        spec.input("code", valid_type=Str)
        spec.input("pseudo_family", valid_type=Str)
        spec.outline(
            cls.run_pw,
            cls.return_results,
        )

    def run_pw(self):
        print "Workchain node identifiers: {}".format(self.calc)
        #Instantiate a JobCalc process and create basic structure
        JobCalc = PwCalculation.process()
        self.ctx.s0 = create_diamond_fcc(Str(self.inputs.element))
        self.ctx.eos_names = []

        calcs = {}
        for label, factor in zip(labels, scale_facs):
            s = rescale(self.ctx.s0,Float(factor))
            inputs = generate_scf_input_params(s, str(self.inputs.code), self.inputs.pseudo_family)
            print "Running a scf for {} with scale factor {}".format(self.inputs.element, factor)
            future = submit(JobCalc, **inputs)
            calcs[label] = future

        # Ask the workflow to continue when the results are ready and store them
        # in the context
        return ToContext(**calcs)

    def return_results(self):
        eos = []
        for label in labels:
            eos.append(get_info(self.ctx[label].get_outputs_dict()))

        #Return information to plot the EOS
        ParameterData = DataFactory("parameter")
        retdict = {
                'initial_structure': self.ctx.s0,
                'result': ParameterData(dict={'eos_data': eos})
           }
        for link_name, node in retdict.iteritems():
            self.out(link_name, node)

def get_info(calc_results):
    return (calc_results['output_parameters'].dict.volume,
            calc_results['output_parameters'].dict.energy,
            calc_results['output_parameters'].dict.energy_units)

def run_eos(element="Si", code='qe-pw-6.2.1@localhost', pseudo_family='GBRV_lda'):
    return run(EquationOfStates, element=Str(element), code=Str(code), pseudo_family=Str(pseudo_family))

if __name__ == '__main__':
    run_eos()
