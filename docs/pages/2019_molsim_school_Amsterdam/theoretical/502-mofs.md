# Origin of the MOF database

The structures of the 502 Metal Organic Frameworks (MOFs) you are asked to analyze
come mainly from powder or single crystal X-Ray diffraction.

These structures have been uploaded to the
[Cambridge Structural Database (CSD)](https://www.ccdc.cam.ac.uk/solutions/csd-system/components/csd/),
and have been parsed to reject messy structures and remove the solvent molecules inside the pores.
This database was named [Computational Ready Experimental (CoRE) MOF database](http://gregchung.github.io/CoRE-MOFs/).

* In 2014 the CSD reported more than 600k structures
* About 60k structures were identified as MOFs
* About 20k MOFs structures were identified having a 3D network topology
* 5109 were identified as "not messy" and porous (i.e., having pore limiting diameter > 2.4 Angstrom) [(Chung2014)](https://pubs.acs.org/doi/abs/10.1021/cm502594j)
* From 5109 3D MOFs, 2932 survived a DFT calculation, using Quantum Espresso, to compute DDEC point charges [(Nazarian2016a)](https://pubs.acs.org/doi/abs/10.1021/acs.chemmater.5b03836)
* From 5109 3D MOFs, 838 survived a DFT geometry optimization in CP2K [(Nazarian2016b)](https://pubs.acs.org/doi/abs/10.1021/acs.chemmater.6b04226)
* 502 MOFs are the intersection of the two sets, having optimized geometry from CP2K and charges from Quantum Espresso

Don't pay much attention of the names of these structures. They are just strings
with random combinations of six letters.

In case you you wonder if there are duplicates in the 502,
see [(Barthel2018)](https://pubs.acs.org/doi/abs/10.1021/acs.cgd.7b01663)

---

## Exercise

The 502 structures are provided with atomic partial charges.

Do you need them to evaluate the methane deliverable capacity?
How are the interactions between molecule and framework described?
