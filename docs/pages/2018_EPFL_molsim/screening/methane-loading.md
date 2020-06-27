Compute methane loading for one MOF
===================================

The average loading of the MOF at a given pressure will be computed
using grand-canonical Monte Carlo (GCMC) simulations with the
[RASPA](https://github.com/numat/RASPA2) code.

- The RASPA code needs several input parameters, some of which you
  will need to figure out

  ```python
  parameters = ParameterData(dict={
      "GeneralSettings": {
          "SimulationType"               : "MonteCarlo",
          "NumberOfCycles"               : 2000,
          "NumberOfInitializationCycles" : 2000,
          "PrintEvery"                   : 2000,
          "ChargeMethod"                 : "Ewald",
          "CutOff"                       : 12.0,
          "Forcefield"                   : "<string>",
          "EwaldPrecision"               : 1e-6,
          "Framework"                    : 0,
          "UnitCells"                    : "<int> <int> <int>",
          "HeliumVoidFraction"           : 0.0,
          "ExternalTemperature"          : <float (Kelvin)>,
          "ExternalPressure"             : <float (Pascal)>,
      },
      "Component": [{
          "MoleculeName"                 : "methane"
          "MoleculeDefinition"           : "TraPPE",
          "TranslationProbability"       : 0.5,
          "ReinsertionProbability"       : 0.5,
          "SwapProbability"              : 1.0,
          "CreateNumberOfMolecules"      :0,
      }],
  })
  ```

  - Our simulations are performed under periodic boundary
    conditions. This means, we need to make our simulation cell
    large enough that a molecule will never interact with a two
    periodic copies of any of its neighbors. Given the cutoff radius
    of $12$ Angstroms, how often do you need to replicate the unit
    cell of the material?

    *Hint:* The CIF files include information on the size of the
    unit cell.

  - To make things more interesting, we are going to use different
    force fields. Ask your instructor to give you a force field
    identifier.

- You already performed a small GCMC calculation at 10 bar during the
  tutorial. Adapt the input file to your needs and run the
  calculation.
  *Hint:* Once running, the calculation should finish within 5 minutes.
