# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

from aiida.common.example_helpers import test_and_get_code
from aiida.orm import DataFactory, CalculationFactory
from aiida.work.run import submit
from aiida.orm import load_node

# Data classes
CifData = DataFactory('cif')
ParameterData = DataFactory('parameter')
RaspaCalculation = CalculationFactory('raspa')

# Raspa input parameters
parameters = ParameterData(dict={
    "GeneralSettings": {
         "SimulationType"                : "MonteCarlo",
         "NumberOfCycles"                : 1000,
         "NumberOfInitializationCycles"  : 1000,
         "PrintEvery"                    : 100,

         "CutOff"                        : 12.0,  # (Angstroms)

         "Forcefield"                    : "UFF-TraPPE",
         "ChargeMethod"                  : "None",
         "UnitCells"                     : "<int> <int> <int>",

         "ExternalTemperature"           : <float (K)>,
         "ExternalPressure"              : <float (Pa)>,
    },
    "Component": [{
         "MoleculeName"                  : "methane",
         "MoleculeDefinition"            : "TraPPE",
         "MolFraction"                   : 1.0,
         "TranslationProbability"        : 1.0,
         "RotationProbability"           : 1.0,
         "ReinsertionProbability"        : 1.0,
         "SwapProbability"               : 1.0,
         "CreateNumberOfMolecules"       : 0,
    }],
})

# Calculation resources
options = {
    "resources": {
        "num_machines": 1,                 # run on 1 node
        "tot_num_mpiprocs": 1,             # use 1 process
        "num_mpiprocs_per_machine": 1,
    },
    "max_wallclock_seconds": 1 * 60 * 60,  # 1h walltime
    "max_memory_kb": 2000000,              # 2GB memory
    "queue_name": "molsim",                # slurm partition to use
    "withmpi": False,                      # we run in serial mode
}

submit(RaspaCalculation.process(),
    code=test_and_get_code("raspa@bazis", expected_code_type='raspa'),
    structure=load_node("<uuid>"),
    parameters=parameters,
    _options=options
)
