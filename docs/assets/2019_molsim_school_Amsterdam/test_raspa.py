#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
import os

from aiida.common.example_helpers import test_and_get_code
from aiida.orm import DataFactory
from aiida.work.run import submit

# data objects
CifData = DataFactory('cif')
ParameterData = DataFactory('parameter')
RaspaCalculation = CalculationFactory('raspa')

# code
codelabel = "raspa@fidis"
code = test_and_get_code(codelabel, expected_code_type='raspa')

# calc object
calc = code.new_calc()

# resources
options = {
    "resources": {
        "num_machines": 1,
        "tot_num_mpiprocs": 1,
        "num_mpiprocs_per_machine": 1,
        },
    "max_wallclock_seconds": 1 * 60 * 60,
    "max_memory_kb": 2000000,
    "withmpi": False,
}

# parameters
cutoff = 12.00

parameters = ParameterData(
    dict={
            "GeneralSettings":
            {
            "SimulationType"                   : "MonteCarlo",
            "NumberOfCycles"                   : 1000,  
            "NumberOfInitializationCycles"     : 1000, 
            "PrintEvery"                       : 100,

            "CutOff"                           : cutoff,

            "Forcefield"                       : "UFF-TraPPE",
            "ChargeMethod"                     : "None",
            "UnitCells"                        : "? ? ?",

            "ExternalTemperature"              : ?, # in K
            "ExternalPressure"                 : ?, # in Pa
            },
            "Component":
            [{
            "MoleculeName"                     : "methane",
            "MoleculeDefinition"               : "TraPPE",
            "MolFraction"                      : "TraPPE",
            "TranslationProbability"           : ?, # between 0 and 1
            "RotationProbability"              : ?, #
            "ReinsertionProbability"           : ?, #
            "SwapProbability"                  : ?, #
            "CreateNumberOfMolecules"          : 0,
            }],
    })

# HKUST1 structure that is already present in the database
cif = load_node('31037e3c-6b15-4a5d-90e3-16c6e0951159')

inputs = {
    'code': code,
    'structure': cif,
    'parameters': parameters,
    '_options': options,
}

process = RaspaCalculation.process()
future = submit(process, **inputs)
