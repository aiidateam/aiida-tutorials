The RASPA package can perform MC and MD calculations, for a variety of systems.

* [paper](https://www.tandfonline.com/doi/full/10.1080/08927022.2015.1010082)
* [GitHub](https://github.com/numat/RASPA2)
* [Manual](https://github.com/numat/RASPA2/blob/master/Docs/raspa.pdf)

In this tutorial we use this program to perform Grand Canonical (GCMC) calculations
in nanoporous structures.
Here it is basic input:

```
SimulationType                MonteCarlo
NumberOfInitializationCycles  ***
NumberOfCycles                ***
PrintEvery                    ***

RestartFile                   no
RestartStyle                  Raspa

CutOff                        ***

Forcefield                    UFF-TraPPE

ChargeMethod                  ***

Framework 0
FrameworkName                 ***
UnitCells                     * * *

ExternalTemperature           ***
ExternalPressure              ***

Component 0 MoleculeName             methane
	          MoleculeDefinition       TraPPE
	          TranslationProbability   ***
	          RotationProbability      ***
	          ReinsertionProbability   ***
	          SwapProbability          ***
	          CreateNumberOfMolecules  ***
```

which is imported in AiiDA as a ParameterData object, being a python dictionary.

You should fill the input settings, replacing asterisks with meaningful values.

Consider that the force field parameters that you will be using to model the
framework-molecule interactions are on your remote computer:

* `$RASPA_DIR/share/raspa/forcefield/UFF-TraPPE/` contains the Lennard-Jones parameters
for the framework atoms, from [UFF](https://pubs.acs.org/doi/10.1021/ja00051a040),
and for methane, from [TraPPE](http://chem-siepmann.oit.umn.edu/siepmann/trappe/index.html)
* `$RASPA_DIR/share/raspa/molecules/TraPPE/` contains the file `methane.def` with
the critical T and P and acentric factor of methane (why?) and the geometry of this
gas molecule. Note that we are using a force field where methane is modelled as a single point!
