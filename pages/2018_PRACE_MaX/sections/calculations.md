The goal of this section is to understand how to create new data in AiiDA. We will launch a total energy calculation and check its results. We will introduce intentionally some common mistakes along the process of defining and submitting a calculation and we will explain you how to recognize and correct them. While this debugging is done here ‘manually’, workflows (that we will learn later in this tutorial) can automate this procedure considerably. For computing the DFT energy of the silicon crystal (with a PBE functional) we will use Quantum ESPRESSO , in particular the PWscf code (`pw.x`). Besides the AiiDA-core package, a number of plugins exist for many different codes. These are listed in the [AiiDA plugin registry](https://aiidateam.github.io/aiida-registry/)[4]. In particular, the “aiida-quantumespresso” plugin (already installed in your machine) provides a very extensive set of plugins, covering most (if not all) the functionalities of the underlying codes.

The AiiDA daemon
----------------

First of all, check that the AiiDA daemon is actually running. The AiiDA daemon is a program running all the time in the background, checking if new calculations appear and need to be submitted to the scheduler. The daemon also takes care of all the necessary operations before the calculation submission, and after the calculation has completed on the cluster. Type in the terminal

``` terminal
verdi daemon status
```

If the daemon is running, the output should look like

``` terminal
    Profile: default
    Daemon is running as PID 1650 since 2018-05-16 16:26:04
    Active workers [1]:
      PID    MEM %    CPU %  started
    -----  -------  -------  -------------------
     1653    8.225        0  2018-05-16 16:26:04
    Use verdi daemon [incr | decr] [num] to increase / decrease the amount of workers
```

If this is not the case, type in the terminal

``` terminal
verdi daemon start
```

to start the daemon.

Creating a new calculation[sec:create<sub>c</sub>alc]
-----------------------------------------------------

To launch a calculation, you will need to interact with AiiDA mainly in the `verdi shell`. We strongly suggest you to first try the commands in the shell, and then copy them in a script “test\_pw.py” using a text editor. This will be very useful for later execution of a similar series of commands.

**The best way to run python scripts using AiiDA functionalities is to run them in a terminal by means of the command**

``` terminal
 verdi run <scriptname>
```

Every calculation sent to a cluster is linked to a code, which describes the executable file to be used. Therefore, first load the suitable code:

``` python
 code = Code.get_from_string(<codename>)
```

Here `Code` is the general AiiDA class handling all possible codes, and `code` is a class instance tagged as `<codename>` (see the first part of the tutorial for listing all codes installed in your AiiDA machine). You might also want to list only the codes that define a default calculation plugin for the pw.x code of Quantum ESPRESSO. You can do this with the following command:

``` terminal
verdi code list -p quantumespresso.pw
```

Pick the correct codename, that might look like, e.g. `qe-pw-6.2.1@localhost`.

Once run, AiiDA calculations are instances of the class `Calculation`, more precisely of one of its subclasses, each corresponding to a code specific plugin (for example, the PWscf plugin). You have already seen `Calculation` classes in the previous sections.

However, to create a new calculation, rather than manually creating a new class, the suggested way is to use a `Builder`, that helps in setting the various calculation inputs and parameters, and provides TAB-completion.

To obtain a new builder, we can use the `get_builder` method of the `code` object:

``` python
 builder = code.get_builder()
```

This returns a builder that helps in setting up the inputs for the `PwCalculation` class (associated to the `quantumespresso.pw` plugin, i.e. the default plugin for the code you chose before).

As the first step, you can assign a (short) label or a (long) description to the calculation that you are going to create, that you might find convenient in the future. This can be achieved with:

``` python
 builder.label = "PW test"
 builder.description = "My first AiiDA calc with Quantum ESPRESSO on BaTiO3"
```

This information will be saved in the database for later query or inspection. Note that you can press TAB after writing `builder.` to see all available inputs.

Now you have to specify the number of machines (a.k.a. cluster nodes) you are going to run on and the maximum time allowed for the calculation. These general calculation options, that are independent of the code or plugin, but rather mainly passed later to the scheduler that handles the queue, are all grouped under “builder.options”:

``` python
 builder.options.resources = {'num_machines': 1}
 builder.options.max_wallclock_seconds = 30*60
```

Just like the normal inputs, these builder options are also TAB-completed. Type “builder.options.” and hit the TAB button to see the list of available options.

### Preparation of inputs

Quantum ESPRESSO requires an input file containing Fortran namelists and variables, plus some cards sections (the documentation is available [online](http://www.quantum-espresso.org/wp-content/uploads/Doc/INPUT_PW.html)[5]). The Quantum ESPRESSO plugin of AiiDA requires quite a few nodes in input, which are documented [online](http://aiida-core.readthedocs.io/en/latest/plugins/quantumespresso/pw.html)[6]. Here we will instruct our calculation with a minimal configuration for computing the energy of silicon. We need:

1.  Pseudopotentials

2.  a structure

3.  the k-points

4.  the input parameters

We leave the parameters as the last thing to setup and start with structure, k-points, and pseudopotentials.

Use what you learned in the previous section and define these two kinds of objects in this script. Define in particular a silicon structure and a 2\(\times\)2\(\times\)2 mesh of k-points. Notice that if you just copy and paste the code that you executed previously, you will create duplicated information in the database (i.e. every time you will execute the script, you will create another StructureData, another KpointsData, …). In fact, you already have the opportunity to re-use an already existing structure.[7] Use therefore a combination of the bash command `verdi data structure list` and of the shell command `load_node()` to get an object representing the structure created earlier.

### Attaching the input information to the calculation

So far we have defined (or loaded) some of the input data, but we haven’t instructed the calculation to use them. To do this, let’s just set the appropriate attributes of the builder (we assume here that you created the structure and k-points AiiDA nodes before and called them `structure` and `kpoints`, respectively):

``` python
 builder.structure = structure
 builder.kpoints = kpoints
```

Note that you can set in the builder both stored and unstored nodes. AiiDA will take care of storing the unstored nodes upon submission. Otherwise, if you decide not to submit, nothing will be stored in the database.

Moreover, PWscf also needs information on the pseudopotentials, specified by UpfData objects. This is set by storing a dictionary in “builder.pseudo”, with keys being the kind names, and value being the UpfData pseudopotential nodes. To simplify the task of choosing pseudopotentials, we can however use a helper function that automatically returns this dictionary picking the pseudopotentials from a given UPF family.

You can list the preconfigured families from the command line:

``` terminal
 verdi data upf listfamilies
```

Pick the one you configured earlier or one of the `SSSP` families that we provide, and link it to the calculation using the command:

``` python
 from aiida.orm.data.upf import get_pseudos_from_structure
 builder.pseudo = get_pseudos_from_structure(structure, '<PSEUDO_FAMILY_NAME>')
```

### Preparing and debugging input parameters

The last thing we miss is a set of parameters (i.e. cutoffs, convergence thresholds, etc…) to launch the Quantum ESPRESSO calculation. This part requires acquaintance with Quantum ESPRESSO and, very often, this is the part to tune when a calculation shows a problem. Let’s therefore use this part of the tutorial to learn how to debug problems, and <span>**let’s introduce errors intentionally**</span>. Note also that some of the problems we will investigate appear the first times you launch calculations and can be systematically avoided by using workflows.

Let’s define a set of input parameters for Quantum ESPRESSO, preparing a dictionary of the form:

``` python
parameters_dict = {
    'CONTROL': {
        'calculation': 'scf',
        'tstress': True,
        'tprnfor': True,
    },
    'SYSTEM': {
        'ecutwfc': 30.,
        'ecutrho': 200.,
        'mickeymouse': 240.,
    },
    'ELECTRONS': {
        'conv_thr': 1.e-8,
    },
}
```

This dictionary is almost a valid input for the Quantum ESPRESSO plugin, except for an invalid key called “mickeymouse”. When Quantum ESPRESSO receives an unrecognized key (even when you misspell one) its behavior is to stop almost immediately. By default, the AiiDA plugin will not validate your input and simply pass it over. Therefore let’s pass this dictionary to the calculation and observe this unsuccessful behavior.

As done before, load the ParameterData class

``` python
 ParameterData = DataFactory("parameter") 
```

and create an instance of the class containing all the input parameters you just defined

``` python
 parameters = ParameterData(dict=parameters_dict)
```

Finally, set the parameters in the builder

``` python
 builder.parameters = parameters
```

### Simulate submission

At this stage, you have recreated in memory (it’s not yet stored in the database) the input of the graph shown in Fig. [fig:graph]a, whereas the outputs will be created later by the daemon.

In order to check how AiiDA creates the actual input files for the calculation, we can simulate the submission process with the (otherwise optional) command

``` python
 builder.submit_test()
```

This creates a folder of the form `submit_test/[date]-0000[x]` in the current directory. Check (in your second terminal) the input file `aiida.in` within this folder, comparing it with the content of the input data nodes you created earlier, and that the ‘pseudo’ folder contains the needed pseudopotentials. You can also check the submission script `_aiidasubmit.sh` (the scheduler that is installed on the machine is Torque, so AiiDA creates the files with the proper format for this scheduler). Note: you cannot correct the input file from the “submit\_test” folder: you have to correct the script and re-execute it; the files created by `submit_test()` are only for final inspection.

### Storing and submitting the calculation

Up to now the calculation `calc` is kept in memory and not in the database. We will now submit it, that will implicitly create a `PwCalculation` class, store it in the database, store also all its inputs parameters, k-points, structure, and properly link them. To submit it, run

``` python
    from aiida.work.launch import submit
    calc = submit(builder)
```

`calc` will now be the stored `PwCalculation`, already submitted to the daemon. The calculation has now a \`\`database primary key" or `pk` (an integer ID) to the calculation (typing `calc.pk` will print this number). Moreover, it also gets a universally-unique ID (`UUID`), visible with `calc.uuid` that does not change even upon sharing the data with collaborators (while the `pk` will change in that case).

Now that the calculation is stored, you can also attach any additional attributes of your choice, which are called “extra” and defined in as key-value pairs. For example, you can add an extra attribute called `element`, with value `Si` through

``` python
 calc.set_extra("element","Si")
```

You will see later the advantage of doing so for querying.

In the meantine, as soon as you submitted your calculation, the daemon picked it up and started to perform all the operations to do the actual submission, going through input file generation, submission to the queue, waiting for it to run and finish, retrieving the output files, parsing them, storing them in the database and setting the state of the calculation to `Finished`.

**N.B.** If the daemon is not running the calculation will remain in the `NEW` state until when you start it.

### Checking the status of the calculation

You can check the calculation status from the command line:

``` terminal
 verdi calculation list                                   
```

Note that `verdi` commands can be slow in this tutorial when the calculation is running (because you just have one CPU which is also used by the PWscf calculation).

By now, it is possible that the calculation you submitted has already finished, and therefore that you don’t see any calculation in the output. In fact, by default, the command only prints calculations that are still being handled by the daemon, i.e. those with a state that is not `FINISHED` yet[8].

To see also (your) calculations that have finished (and limit those only to the one created in the past day), use instead

``` terminal
 verdi calculation list -a -p1                                  
```

as explained in the first section.

To inspect the list of input files generated by the AiiDA (this can be done even when the calculation did not finish yet), type

``` terminal
 verdi calculation inputls <pk_number> -c
```

with `pk_number` the pk number of your calculation. This will show the contents of the input directory (`-c` prints directories in colour). Then you can also check the content of the actual input file with

``` terminal
 verdi calculation inputcat <pk_number> | less
```

Troubleshooting
---------------

After all this work the calculation should end up in a FAILED Job state (last column of `verdi calculation list`), and correspondingly the error code near the \`\`Finished" status of the State should be non-zero (400 for FAILED calculations). This was expected, since we used an invalid key in the input parameters. Situations like this happen (probably often...) in real life, so we built in AiiDA the tools to traceback the problem source and correct it.

A first way to proceed is the manual inspection of the output file of PWscf. You can visualize it with:

``` terminal
 verdi calculation outputcat <pk_number> | less
```

This can be a good primer for problem inspection. For something more compact, you can also try to inspect the calculation log (from AiiDA):

``` terminal
 verdi calculation logshow <pk_number>
```

If the calculation has encountered a mistake, this log shows a handful of warnings coming from various processes, such as the daemon, the parser of the output or the scheduler on the cluster. In production runs, errors will mostly come from an unexpected termination of the PWscf calculation. The most programmatic way to handle these errors is to inspect the warnings key by loading the calculation object, say `calc`, and the using the following method:

``` python
calc.res.warnings
```

This will print a list of strings reporting errors experienced during the execution, that can be easily read in python (and thus addressed programmatically), but are also reported in the calculation log. With any of these three methods you can understand that the problem is something like an ‘invalid input key’, which is exactly what we did.

Let’s use a parameters dictionary that actually works. Modify the script `test_pw.py` script modifying the parameter dictionary as

``` python
parameters_dict = {
    "CONTROL": {"calculation": "scf",
                },
    "SYSTEM": {"ecutwfc": 30.,
               "ecutrho": 200.,
               },
    "ELECTRONS": {"conv_thr": 1.e-6,
                  }
    }
```

If you launch the modified script by typing

``` terminal
 verdi run test_pw.py
```

you should now be able to see a calculation reaching successfully the FINISHED state. Now you can access the results as you have seen earlier. For example, note down the pk of the calculation so that you can load it in the `verdi shell` and check the total energy with the commands:

``` python
calc=load_node(<pk>)
calc.res.energy
```
