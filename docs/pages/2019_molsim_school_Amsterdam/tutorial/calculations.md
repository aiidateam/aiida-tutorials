Submit, monitor and debug calculations
======================================

The goal of this section is to understand how to create new data in
AiiDA. We will launch a Grand Canonical Monte Carlo simulation and check
its results. While for now we will do it ‘manually', workflows (that we
will learn later in this tutorial) can automate this procedure
considerably.

Computer setup and configuration
--------------------------------

For the tutorial, we've created a have access to a supercomputer from the University of Amsterdam

Please set up the computer as follows:

```terminal
$ verdi computer setup 
At any prompt, type ? to get some help.
————————————— 
=> Computer name: bazis
bazis computer for the molsim courseCreating new computer with name 'bazis'
=> Fully-qualified hostname: bazis-h1.science.uva.nl
=> Description: bazis computer for the molsim course
=> Enabled: True 
=> Transport type: ssh 
=> Scheduler type: slurm
=> shebang line at the beginning of the submission script: #!/bin/bash
=> AiiDA work directory: /home/{username}/aiida_run/
=> mpirun command: srun -n {tot_num_mpiprocs}
=> Default number of CPUs per machine: 2 
=> Text to prepend to each command execution: 
# This is a multiline input, press CTRL+D on a 
# empty line when you finish 
# ——————————————
# End of old input. You can keep adding 
# lines, or press CTRL+D to store this value 
# —————————————— 
=> Text to append to each command execution: 
# This is a multiline input, press CTRL+D on a 
# empty line when you finish 
# —————————————— 
# End of old input. You can keep adding 
# lines, or press CTRL+D to store this value 
# ——————————————
Computer 'bazis' successfully stored in DB.
```

At this point, the computer node has been created in the database, see

```terminal
$ verdi computer list -a
```

but it hasn't yet been configured.

In order to access the computer, download the SSH key

```terminal
$ wget https://www.dropbox.com/s/.../aiida_tutorial_aiidaaccount?dl=1 -O /home/max/.ssh/bazis.pem
```

and use it to configure the `bazis` computer:

```terminal
$ verdi computer configure bazis
Configuring computer 'bazis' for the AiiDA user 'aiida@localhost'
Computer bazis has transport of type ssh

Note: to leave a field unconfigured, leave it empty and press [Enter]

=> username = molsim<n>
=> port = 22
=> look for keys = True
=> key filename = /home/max/.ssh/bazis.pem
=> timeout = 60
=> allow agent =
=> proxy command =
=> compress = True
=> gssauth = no
=> gsskex = no
=> gssdelegcreds = no
=> gsshost = bazis.science.uva.nl
=> load system hostkeys = True
=> key policy = AutoAddPolicy
Configuration stored for your user on computer 'bazis'.
```

Finally, let aiida test the computer:

```terminal
$ verdi computer test bazis
```

Code setup and configuration
----------------------------

Next, we need to let AiiDA know about the computer codes available on
our “virtual supercomputer”.

Let's set up the [RASPA2](https://github.com/numat/RASPA2) code as follows:


```terminal
$ verdi code setup
At any prompt, type ? to get some help.
—————————————
=> Label: raspa
=> Description: Raspa code for the molsim course
=> Local: False
=> Default input plugin: raspa
=> Remote computer name: bazis
=> Remote absolute path: /home/molsim20/raspa/bin/simulate
=> Text to prepend to each command execution
FOR INSTANCE, MODULES TO BE LOADED FOR THIS CODE:
# This is a multiline input, press CTRL+D on a
# empty line when you finish
# —————————————— 
# End of old input. You can keep adding 
# lines, or press CTRL+D to store this value 
# —————————————— 
export RASPA_DIR=/home/molsim20/raspa/
=> Text to append to each command execution: 
# This is a multiline input, press CTRL+D on a 
# empty line when you finish 
# —————————————— 
# End of old input. You can keep adding 
# lines, or press CTRL+D to store this value 
# —————————————— 
Code 'raspa' successfully stored in DB.
```

The list of codes should now include your new code `raspa@bazis`

```terminal
$ verdi code list
```

The AiiDA daemon
----------------

First of all check that the AiiDA daemon is actually running. The AiiDA
daemon is a program running all the time in the background, checking if
new calculations appear and need to be submitted to the scheduler. The
daemon also takes care of all the necessary operations before the
calculation submission, and after the calculation has completed on the
cluster. Type in the terminal

```terminal
$ verdi daemon status
```

If the daemon is running, the output should look like

    # Most recent daemon timestamp:0h:00m:26s ago
    ## Found 1 process running:
       * aiida-daemon[aiida-daemon] RUNNING    pid 15044, uptime 3 days, 15:38:41

If this is not the case, type in the terminal

```terminal
$ verdi daemon start
```

to start the daemon.

> **Note**
> In case the daemon did not start and error message was printed
> ```terminal
> You are not the daemon user! I will not start the daemon.
> (The daemon user is 'aiida@localhost', you are 'some.body@xyz.com')
>
> ** FOR ADVANCED USERS ONLY: **
> To change the current default user, use 'verdi install --only-config'
> To change the daemon user, use 'verdi daemon configureuser'
> ```
> You should follow the instructions and run
> ```terminal
> $ verdi daemon configureuser
> ```
> And allow your user to run the daemon
>
> ```terminal
> > Current default user: some.body@xyz.com
> > Currently configured user who can run the daemon: aiida@localhost
>   (therefore, you cannot run the daemon, at the moment)
> ****************************************************************************
> * WARNING! Change this setting only if you are sure of what you are doing. *
> * Moreover, make sure that the daemon is stopped.                          *
> ****************************************************************************
> Are you really sure that you want to change the daemon user? [y/N] y
>
> Enter below the email of the new user who can run the daemon.
> New daemon user: some.body@xyz.com
> The new user that can run the daemon is now Some Body.
> ```


Creating a new calculation
--------------------------

To start please [download the AiiDA submission script]({{ site.baseurl}}/assets/2019_molsim_school_Amsterdam/test_raspa.py). To
launch a calculation, you will need to interact with AiiDA mainly in the
<span>`verdi shell`</span>. We strongly suggest you to first try the
commands in the shell, and then copy them in a script “test\_pw.py”
using a text editor. This will be very useful for later execution of a
similar series of commands.

**The best way to run python scripts using AiiDA functionalities is to
run them in a terminal by means of the command**

```terminal
$ verdi run <scriptname>
```

Every calculation sent to a cluster is linked to a code, which describes
the executable file to be used. Therefore, first load the suitable code:

```python
from aiida.common.example_helpers import test_and_get_code 
code = test_and_get_code(codename, expected_code_type='raspa')
```

Here `test_and_get_code` is an AiiDA function handling all possible
codes, and `code` is a class instance provided as `codename` (see the
first part of the tutorial for listing all codes installed in your AiiDA
machine). For this example use codename `raspa@bazis`.

AiiDA calculations are instances of the class `Calculation`, more
precisely of one of its subclasses, each corresponding to a code
specific plugin (for example, the Raspa plugin). We create a new
calculation using the `new_calc` method of the `code` object:

```python
calc = code.new_calc()
```

This creates and initializes an instance of the `RaspaCalculation`
class, the subclass associated with the `raspa` plugin. Sometimes, you might find convenient to annotate
information assigning a (short) label or a (long) description, like:

```python
calc.label='Raspa test'
calc.description='My first AiiDA calc with Raspa'
```

This information will be saved in the database for later query or
inspection.

Now you have to specify the number of machines (a.k.a. cluster nodes)
you are going to run on and the maximum time allowed for the calculation
— this information is passed to the scheduler that handles the queue:

```python
calc.set_resources('num_machines': 1, 'num_mpiprocs_per_machine':1)
calc.set_max_wallclock_seconds(30*60)
```
