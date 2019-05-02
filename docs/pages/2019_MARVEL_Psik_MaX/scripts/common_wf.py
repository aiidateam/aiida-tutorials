from aiida.plugins import CalculationFactory, DataFactory
from aiida_quantumespresso.utils.pseudopotential import validate_and_prepare_pseudos_inputs
import numpy as np

PwCalculation = CalculationFactory('quantumespresso.pw')


def generate_scf_input_params(structure, code, pseudo_family):
    # The inputs
    builder = PwCalculation.get_builder()

    # The structure
    builder.structure = structure

    builder.code = code
    builder.metadata.label = "PW test"
    builder.metadata.description = "My first AiiDA calculation of Silicon with Quantum ESPRESSO"
    builder.metadata.options.resources = {'num_machines': 1}
    builder.metadata.options.max_wallclock_seconds = 30 * 60

    # Kpoints
    KpointsData = DataFactory('array.kpoints')
    kpoints = KpointsData()
    kpoints_mesh = 2
    kpoints.set_kpoints_mesh([kpoints_mesh, kpoints_mesh, kpoints_mesh])
    builder.kpoints = kpoints

    # Calculation parameters
    parameters_dict = {
        'CONTROL': {
            'calculation': 'scf',
            'tstress': True,  # Important that this stays to get stress
            'tprnfor': True,
        },
        'SYSTEM': {
            'ecutwfc': 30.,
            'ecutrho': 200.,
        },
        'ELECTRONS': {
            'conv_thr': 1.e-6,
        }
    }
    Dict = DataFactory('dict')
    builder.parameters = Dict(dict=parameters_dict)

    # Pseudopotentials
    builder.pseudos = validate_and_prepare_pseudos_inputs(structure, pseudo_family=pseudo_family)

    return builder


def birch_murnaghan(V, E0, V0, B0, B01):
    r = (V0 / V) ** (2. / 3.)
    return E0 + 9. / 16. * B0 * V0 * (r - 1.) ** 2 * \
                (2. + (B01 - 4.) * (r - 1.))


def fit_birch_murnaghan_params(volumes_, energies_):
    from scipy.optimize import curve_fit

    volumes = np.array(volumes_)
    energies = np.array(energies_)
    params, covariance = curve_fit(
        birch_murnaghan, xdata=volumes, ydata=energies,
        p0=(
            energies.min(),  # E0
            volumes.mean(),  # V0
            0.1,  # B0
            3.,  # B01
        ),
        sigma=None
    )
    return params, covariance


def plot_eos(eos_pk):
    """
    Plots equation of state taking as input the pk of the ProcessCalculation
    printed at the beginning of the execution of run_eos_wf
    """
    import pylab as pl
    from aiida.orm import load_node
    eos_calc = load_node(eos_pk)
    eos_result = eos_calc.out.result
    raw_data = eos_result.dict.eos_data

    data = []
    for V, E, units in raw_data:
        data.append((V, E))

    data = np.array(data)
    params, covariance = fit_birch_murnaghan_params(data[:, 0], data[:, 1])

    vmin = data[:, 0].min()
    vmax = data[:, 0].max()
    vrange = np.linspace(vmin, vmax, 300)

    pl.plot(data[:, 0], data[:, 1], 'o')
    pl.plot(vrange, birch_murnaghan(vrange, *params))

    pl.xlabel("Volume (ang^3)")
    # I take the last value in the list of units assuming units do not change
    pl.ylabel("Energy ({})".format(units))
    pl.show()
