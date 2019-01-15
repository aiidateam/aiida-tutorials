The 502 structures of Metal Organic Frameworks (MOFs) you are asked to analyze
are coming from experimental synthesis: mainly powder or single crystal X-Ray diffraction.

These structures have been uploaded in the [Cambridge Structural Database (CSD)](https://www.ccdc.cam.ac.uk/),
and have been parsed to reject messy structures and remove the solvent molecules inside the pores.
The database was named [Computational Ready Experimental (CoRE) MOF database](http://gregchung.github.io/CoRE-MOFs/).

* In 2014 the CSD reported more than 600k structures
* About 60k structures were identified as MOFs
* About 20k MOFs structures were identified having a 3D network topology
* 5109 were identified as "not messy" and porous (i.e., having pore limiting diameter > 2.4 Angstrom)
[(Chung2014)](https://pubs.acs.org/doi/abs/10.1021/cm502594j)
* From 5109 3D MOFs, 2932 survived a DFT calculation, using Quantum Espresso, to compute DDEC point charges
[(Nazarian2016a)](https://pubs.acs.org/doi/abs/10.1021/acs.chemmater.5b03836)
* From 5109 3D MOFs, 838 survived a DFT geometry optimization in CP2K
[(Nazarian2016b)](https://pubs.acs.org/doi/abs/10.1021/acs.chemmater.6b04226)
* 502 MOFs are the intersection of the two sets,
having optimized geometry from CP2K and charges from Quantum Espresso

Do you wonder if there are duplicated in this 502? [Read here!](https://pubs.acs.org/doi/abs/10.1021/acs.cgd.7b01663)

These structures are provided with atomic partial charges.
Do you need them to evaluate the methane deliverable capacity?
