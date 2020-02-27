#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
import sys
import argparse
from aiida.common.exceptions import NotExistent
from aiida.orm.data.base import Str
from aiida.orm.data.upf import UpfData
from aiida.orm.data.parameter import ParameterData
from aiida.orm.data.structure import StructureData
from aiida.orm.data.array.kpoints import KpointsData
from aiida.orm.data.array.bands import BandsData
from aiida.orm.utils import WorkflowFactory
from aiida.work.run import run,submit
from aiida_quantumespresso.workflows.pw.custom_band_structure_workchain import CustomPwBandStructureWorkChain
from aiida.orm.calculation.work import WorkCalculation
from aiida.common import links
from collections import Counter
import json
import os, shutil

def erfc_scdm(x,mu,sigma):
    from scipy.special import erfc
    return 0.5*erfc((x-mu)/sigma)

def get_mu_and_sigma_from_projections(bands, projections, thresholds):
    import numpy as np

    def find_max(proj_list,max_value):
        f = lambda x : True if x<max_value else False
        bool_list = map(f,proj_list)
        for i,item in enumerate(bool_list):
            if item:
                break
        print i,proj_list[i]

    def fit_erfc(f,xdata,ydata):
        from scipy.optimize import curve_fit
        return curve_fit(f, xdata, ydata,bounds=([-50,0],[50,50]))

    # List of specifications of atomic orbitals in dictionary form
    dict_list = [i.get_orbital_dict() for i in projections.get_orbitals()]
    # Sum of the projections on all atomic orbitals (shape kpoints x nbands)
    out_array = sum([sum([x[1] for x in projections.get_projections(
        **get_dict)]) for get_dict in dict_list])
    # Flattening (projection modulus squared according to QE, energies)
    projwfc_flat, bands_flat = out_array.flatten(), bands.get_bands().flatten()
    # Sorted by energy
    sorted_bands, sorted_projwfc = zip(*sorted(zip(bands_flat, projwfc_flat)))
    popt,pcov = fit_erfc(erfc_scdm,sorted_bands,sorted_projwfc)
    mu = popt[0]
    sigma = popt[1]
    # Temporary, TODO add check on interpolation
    success = True
    return mu, sigma, sorted_bands, sorted_projwfc

if __name__ == "__main__":

    pwbands_calc = load_node(dft_band).get_inputs(link_type=links.LinkType.CREATE)[0]

    pwscf_calc = pwbands_calc.inp.parent_calc_folder.get_inputs(link_type=links.LinkType.CREATE)[0]

    # bands inherit fermi from scf
    #assert pwscf_calc.inp.parameters.dict.CONTROL['calculation'] == 'scf' 
    fermi_energy = pwscf_calc.res.fermi_energy

    w90_calc = load_node(w90_band).get_inputs(link_type=links.LinkType.CREATE)[0]
    sigma = w90_calc.inp.parameters.dict.scdm_sigma
    mu = w90_calc.inp.parameters.dict.scdm_mu

    projections = w90_calc.inp.parameters.inp.output_parameters.inp.projections
    orbital_count = Counter(orb.get_orbital_dict()['kind_name'] for orb in projections.get_orbitals())
    # I actually use the kind names to get 0 when they are missing, otherwise I would not see them
    num_orbitals_string = ", ".join("{}: {}".format(k, orbital_count[k]) for k in 
    #    sorted(orbital_count.iterkeys()))
        sorted(k.name for k in structures[formula].kinds))

    #print "{:6s}: {:13.10f} eV; mu: {:13.10f} eV; sigma: {:13.10f} eV".format(
    #    formula, fermi_energy, mu, sigma)
    #print "{:6s}: {}".format(formula, (mu - fermi_energy) / sigma)

    print "{:6s}:".format(formula)
    #print "{:6s}: mu-3sigma = {}; {}".format(formula, mu - 3 * sigma, num_orbitals_string)
    print "        mu = {}, e_fermi = {}, sigma = {}".format(mu, fermi_energy, sigma)

    proj_bands = projections.inp.projections.out.bands
    mu_fit, sigma_fit, sorted_bands, sorted_projwfc = get_mu_and_sigma_from_projections(proj_bands, projections, {'sigma_factor_shift': 0.})
    import pylab as pl
    pl.figure()
    pl.plot(sorted_bands, sorted_projwfc, 'o')
    pl.plot(sorted_bands, erfc_scdm(sorted_bands, mu_fit, sigma_fit))
    pl.axvline([mu_fit], color='red', label=r"$\mu$")
    pl.axvline([mu_fit - 3. * sigma_fit], color='orange', label=r"$\mu-3\sigma$")
    pl.axvline([fermi_energy], color='green', label=r"$E_f$")
    pl.title(formula)
    pl.legend(loc='auto')
    pl.savefig('{}/{}.png'.format(suffix, formula))

