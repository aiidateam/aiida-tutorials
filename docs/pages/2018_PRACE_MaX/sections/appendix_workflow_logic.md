More workflow logic: while loops and conditional statements
===========================================================

In the previous sections, you have been introduced to WorkChains, and the reason for using them over “standard” workfunctions (i.e., functions decorated with `@wf`).

However, in the example of Sec. [sec:workchainsimple], the `spec.outline` was quite simple, with a “static” sequence of two steps. Most often, however, you need dynamic workflows, where you need to decide at runtime whether to continue to compute or not (e.g. in a convergence loop, where you need to stop if convergence has been achieved). To support this scenario, the `spec.outline` can support logic: *while* loops and *if/elif/else* blocks. The simplest way to explain it is to show an example:

``` python
from aiida.work.workchain import if_, while_

spec.outline(
    cls.s1,
    if_(cls.isA)(
        cls.s2
    ).elif_(cls.isB)(
        cls.s3
    ).else_(
        cls.s4
    ),
    cls.s5,
    while_(cls.condition)(
        cls.s6
    ),
)
```

that would *roughly* correspond, in a python syntax, to:

``` python
s1()
if isA():
    s2()
elif isB():
    s3()
else:
    s4()
s5()
while condition():
    s6()
```

The only constraint is that condition functions (in the example above `isA`, `isB` and `condition`) must be class methods that returns `True` or `False` depending on whether the condition is met or not.

A suggestion on how to write new workchains: Use the outline to help you in designing the logic. First create the spec outline writing, almost if you were explaining it in words, what you expect the workflow to do. Then, define one by one the methods. For example, we have prepared a simple workfunction to optimize the lattice parameter of silicon efficiently using a Newton’s algorithm on the energy derivative, i.e. the pressure \(p=-dE/dV\). You can find it the code at `tutorial_scripts/pressure_convergence.py`. The outline looks like this:

``` python
spec.outline(
    cls.init,
    cls.put_step0_in_ctx,
    cls.move_next_step,
    while_(cls.not_converged)(
        cls.move_next_step,
     ),
    cls.report
)
```

This outline already roughly explains the algorithm: after an initialization (`init`) and putting the first step (number zero) in the ctx (`put_step0_in_ctx`), a function to move to the next step is called (`move_next_step`). This is iterated while a given convergence criterion is not met (`not_converged`). Finally, some reporting is done, including returning some output nodes (`report`).

If you are interested in the details of the algorithm, you can inspect the file. The main ideas are described here:

init  
Generate a `pw.x` calculation for the input structure (with volume \(V\)), and one for a structure where the volume is \(V+4\text{\AA}^3\) (just to get a closeby volume). Store the results in the context as `r0` and `r1`

put\_step0\_in\_ctx  
Store in the context \(V\), \(E(V)\) and \(dE/dV\) for the first calculation `r0`

move\_next\_step  
This is the most important function. Calculate \(V\), \(E(V)\) and \(dE/dV\) for `r1`. Also, estimate \(d^2E/dV^2\) from the finite difference of the first derivative of `r0` and `r1` (helper functions to achieve this are provided). Get the \(a\), \(b\) and \(c\) coefficients of a parabolic fit \(E=aV^2 + bV + c\) and estimated the expected minimum of the EOS function as the minimum of the fit \(V_0=-b/2a\). Finally, replace `r0` with `r1` in the context (i.e., get rid of the oldest point) and launch a new pw calculation at volume \(V_0\), that will be stored in the context replacing `r1`. In this way, at the next iteration `r0` and `r1` will contain the latest two simulations. Finally, at each step some relevant information (coefficients \(a\), \(b\) and \(c\), volumes, energies, energy derivatives, ...) are stored in a list called `steps`. This whole list is stored in the context because it provides quantities to be preserved between different workfunction steps.

not\_converged  
Return `True` if convergence has not been achieved yet. Convergence is achieved if the difference in volume between the two latest simulations is smaller than a given threshold (`volume_tolerance`).

report  
This is the final step. Mainly, we return the output nodes: `steps` with the list of results at each step, and `structure` with the final converged structure.

The results returned in `steps` can be used to represent the evolution of the minimisation algorithm. A possible way to visualize it is presented in Fig. [fig:convpressure], obtained with an initial lattice constant of \(a_{\text{lat}} = 5.2\text{\AA}\).

![[fig:convpressure]Example of results of the convergence algorithm presented in Sec. [sec:convpressure]. The bottom plot is a zoom near the minimum. The dots represent the (volume,energy) points obtained from Quantum ESPRESSO, and the numbers indicate at which iteration they were obtained. The parabolas represent the parabolic fits used in the algorithm; the minimum of the parabola is represented with a small cross, in correspondence of the vertical lines, used as the volume for the following step.]({{ site.baseurl}}/assets/2018_PRACE_MaX/convergence_pressure)

<span>9</span> P. Giannozzi et al., J.Phys. Cond. Matt. 29, 465901 (2017). S. R. Bahn and K. W. Jacobsen, Comput. Sci. Eng., 4, 56-66 (2002). S. Ping Ong et al., Comput. Mater. Sci. 68, 314-319 (2013). K.F. Garrity, J.W. Bennett, K.M. Rabe and D. Vanderbilt, Comput. Mater. Sci. 81, 446 (2014). G. Prandini, A. Marrazzo, I. E. Castelli, N. Mounet, N. Marzari, A Standard Solid State Pseudopotentials (SSSP) library optimized for accuracy and efficiency (Version 1.0, data download), Materials Cloud Archive (2018), [doi:10.24435/materialscloud:2018.0001/v1](http://doi.org/10.24435/materialscloud:2018.0001/v1). Crystallographic Open Database (<span>COD</span>), <http://www.crystallography.net/cod/>.

[1] The string provided to the `DataFactory` encodes both the location and the name of the required class according to some specific rules.

[2] if you set the structure incorrectly, for example with overlapping atoms, it is very likely that any DFT code will fail!

[3] We purposefully do not provide advanced commands for crystal structure manipulation in AiiDA, because python packages that accomplish such tasks already exist (such as ASE or pymatgen).

[4] <https://aiidateam.github.io/aiida-registry/>

[5] <http://www.quantum-espresso.org/wp-content/uploads/Doc/INPUT_PW.html>

[6] <http://aiida-core.readthedocs.io/en/latest/plugins/quantumespresso/pw.html>

[7] However, to avoid duplication of KpointsData, you should first learn how to query the database, therefore we will ignore this duplication issue for now.

[8] For JobCalculations (i.e., calculations that are submitted to a remote computer through a scheduler) there is an additional “Job state” (last column of the output of `verdi calculation list`) that can either be FINISHED if all went well, or one of the possible failure states (FAILED, PARSINGFAILED, SUBMISSIONFAILED, RETRIEVALFAILED). These states are represented as a Finished state (third column of `verdi calculation list`, with a zero/non-zero error code depending if they finished/did not finish correctly). This latter state is more general than just JobCalculations and also applies to workflows, as we will see later in the tutorial.

[9] In simple (or even simplified) words, a decorator is a function that modifies the behavior of another function. In python, a function can be decorated by adding a line of the form `@decorating_function_name` on the line just before the `def` line of the decorated function. If you want to know more, there are many online resources explaining python decorators.

[10] If you are curious: the two links have the same label, but are of different *link\_type*: one is a **create** link, that keeps track of the calculation that actually generated the node. Instead the other one is of type **return**, stating that the workfunction, beside creating that node, also returned it as an output. Calculation 5002 instead only returned the node but it did not generate it, therefore there is only one link between it and the final `StructureData`.
