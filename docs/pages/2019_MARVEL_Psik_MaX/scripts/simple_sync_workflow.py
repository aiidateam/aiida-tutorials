from aiida.engine import run, Process, calcfunction, workfunction
from aiida.orm import load_code
from aiida.plugins import CalculationFactory, DataFactory

from create_rescale import create_diamond_fcc, rescale
from common_wf import generate_scf_input_params

Dict = DataFactory('dict')
Float = DataFactory('float')
Str = DataFactory('str')

# Load the calculation class 'PwCalculation' using its entry point 'quantumespresso.pw'
PwCalculation = CalculationFactory('quantumespresso.pw')


@workfunction
def run_eos_wf(code, pseudo_family, element):
    # This will print the pk of the work function
    print('Running run_eos_wf<{}>'.format(Process.current().pid))

    scale_factors = (0.96, 0.98, 1.0, 1.02, 1.04)
    labels = ['c1', 'c2', 'c3', 'c4', 'c5']

    results = {}
    initial_structure = create_diamond_fcc(element)

    for label, factor in zip(labels, scale_factors):
        structure = rescale(initial_structure, Float(factor))
        inputs = generate_scf_input_params(structure, code, pseudo_family)

        print('Running a scf for {} with scale factor {}'.format(element, factor))
        results[label] = run(PwCalculation, **inputs)

    inputs = {label: result['output_parameters'] for label, result in results.items()}
    eos = get_eos_data(**inputs)

    result = {
        'initial_structure': initial_structure,
        'eos': eos
    }

    return result


@calcfunction
def get_eos_data(**kwargs):
    eos = [(result.dict.volume, result.dict.energy, result.dict.energy_units) for label, result in kwargs.items()]
    return Dict(dict={'eos': eos})


def run_eos(code=load_code('pw-v6.1'), pseudo_family='SSSP_v1.1_efficiency_PBE', element='Si'):
# def run_eos(code=load_code('qe-pw-6.2.1@localhost'), pseudo_family='GBRV_lda', element='Si'):
    return run_eos_wf(code, Str(pseudo_family), Str(element))


if __name__ == '__main__':
    run_eos()
