The 502 structures of Metal Organic Frameworks (MOFs) you are asked to analyze
are coming from experimental synthesis: mainly powder or single crystal X-Ray diffraction.

These structures have been uploaded in the [Cambridge Structural Database (CSD)](https://www.ccdc.cam.ac.uk/),
and have been parsed to reject messy structures and remove the solvent molecules inside the pores.
The database was named [Computational Ready Experimental (CoRE) MOF database](http://gregchung.github.io/CoRE-MOFs/).

* from a total of >600k structure in the CSD,
* >60k were identified as MOF
* >20k having a 3D network
* 5109 were identified as "not messy" and porous (i.e., having pore limiting diameter > 2.4 Angstrom)
* from 5109, 2932 survived a DFT calculation, using Quantum Espresso, to compute DDEC point charges
* from 5109, 838 survived a DFT geometry optimization in CP2K
* 502 are the intersection of the two, having an optimized geometry from CP2K and charges from Quantum Espresso

Do you wonder if there are duplicated in this 502? [Read here!](https://pubs.acs.org/doi/abs/10.1021/acs.cgd.7b01663)

These structures are provided with atomic partial charges, do you need them?
