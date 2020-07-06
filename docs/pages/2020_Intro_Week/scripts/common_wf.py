# -*- coding: utf-8 -*-
"""Helper functions."""
import numpy as np
from aiida.plugins import CalculationFactory, DataFactory
from aiida_quantumespresso.utils.pseudopotential import validate_and_prepare_pseudos_inputs

Dict = DataFactory('dict')
KpointsData = DataFactory('array.kpoints')
PwCalculation = CalculationFactory('quantumespresso.pw')


def generate_scf_input_params(structure, code, pseudo_family):
    """Construct a builder for the `PwCalculation` class and populate its inputs.

    :return: `ProcessBuilder` instance for `PwCalculation` with preset inputs
    """
    parameters = {
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

    kpoints = KpointsData()
    kpoints.set_kpoints_mesh([2, 2, 2])

    builder = PwCalculation.get_builder()
    builder.code = code
    builder.structure = structure
    builder.kpoints = kpoints
    builder.parameters = Dict(dict=parameters)
    builder.pseudos = validate_and_prepare_pseudos_inputs(
        structure, pseudo_family=pseudo_family)
    builder.metadata.label = "PW test"
    builder.metadata.description = "My first AiiDA calculation of Silicon with Quantum ESPRESSO"
    builder.metadata.options.resources = {'num_machines': 1}
    builder.metadata.options.max_wallclock_seconds = 30 * 60

    return builder


def birch_murnaghan(V, E0, V0, B0, B01):
    """Compute energy by Birch Murnaghan formula."""
    r = (V0 / V)**(2. / 3.)
    return E0 + 9. / 16. * B0 * V0 * (r - 1.)**2 * (2. + (B01 - 4.) * (r - 1.))


def fit_birch_murnaghan_params(volumes_, energies_):
    """Fit Birch Murnaghan parameters."""
    from scipy.optimize import curve_fit

    volumes = np.array(volumes_)
    energies = np.array(energies_)
    params, covariance = curve_fit(
        birch_murnaghan,
        xdata=volumes,
        ydata=energies,
        p0=(
            energies.min(),  # E0
            volumes.mean(),  # V0
            0.1,  # B0
            3.,  # B01
        ),
        sigma=None)
    return params, covariance


def plot_eos(eos_pk):
    """
    Plots equation of state taking as input the pk of the ProcessCalculation
    printed at the beginning of the execution of run_eos_wf
    """
    import pylab as pl
    from aiida.orm import load_node
    eos_calc = load_node(eos_pk)

    data = []
    for V, E, units in eos_calc.outputs.result.dict.eos:
        data.append((V, E))

    data = np.array(data)
    params, _covariance = fit_birch_murnaghan_params(data[:, 0], data[:, 1])

    vmin = data[:, 0].min()
    vmax = data[:, 0].max()
    vrange = np.linspace(vmin, vmax, 300)

    pl.plot(data[:, 0], data[:, 1], 'o')
    pl.plot(vrange, birch_murnaghan(vrange, *params))

    pl.xlabel("Volume (ang^3)")
    # I take the last value in the list of units assuming units do not change
    pl.ylabel("Energy ({})".format(units))  # pylint: disable=undefined-loop-variable
    pl.show()
