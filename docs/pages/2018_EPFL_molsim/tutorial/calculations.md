Submit, monitor and debug calculations
======================================

The goal of this section is to understand how to create new data in
AiiDA. We will launch a Grand Canonical Monte Carlo simulation and check
its results. While for now we will do it ‘manually', workflows (that we
will learn later in this tutorial) can automate this procedure
considerably.

Computer setup and configuration
--------------------------------

For the tutorial, we've created a “virtual supercomputer” on the Amazon
elastic cloud, where you can submit your calculations.

Please set up the computer as follows:

```terminal
$ verdi computer setup 
At any prompt, type ? to get some help.
————————————— 
=> Computer name: aws Creating new computer with name 'aws' 
=> Fully-qualified hostname: 34.244.10.104 
=> Description: AWS instance for tutorial 
=> Enabled: True 
=> Transport type: ssh 
=> Scheduler type: torque 
=> shebang line at the beginning of the submission script: \#!/bin/console 
=> AiiDA work directory: /tmp/{username}/aiida~r~un/ 
=> mpirun command: mpirun -np {tot_num_mpiprocs}
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
Computer 'aws' successfully stored in DB.
```

At this point, the computer node has been created in the database, see

```terminal
$ verdi computer list -a
```

but it hasn't yet been configured.

In order to access the computer, download the SSH key

```terminal
$ wget https://www.dropbox.com/s/.../aiida_tutorial_aiidaaccount?dl=1 -O /home/max/.ssh/aws.pem
```

and use it to configure the `aws` computer:

```terminal
$ verdi computer configure aws 
Configuring computer 'aws' for the AiiDA user 'aiida@localhost' 
Computer aws has transport of type ssh

Note: to leave a field unconfigured, leave it empty and press [Enter]

=> username = aiida 
=> port = 22 
=> look for keys = True 
=> key filename = /home/max/.ssh/aws.pem 
=> timeout = 60 
=> allow agent = 
=> proxy command = 
=> compress = True 
=> gssauth = no 
=> gsskex = no 
=> gssdelegcreds = no 
=> gsshost = 34.244.10.104
=> load system hostkeys = True 
=> key policy = AutoAddPolicy
Configuration stored for your user on computer 'aws'.
```

Finally, let aiida test the computer:

```terminal
$ verdi computer test aws
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
=> Description: Raspa code for molsim course
=> Local: False 
=> Default input plugin: raspa 
=> Remote computer name: aws 
=> Remote absolute path: /home/aiida/.local/bin/simulate 
=> Text to prepend to each command execution 
FOR INSTANCE, MODULES TO BE LOADED FOR THIS CODE: 
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
Code 'raspa' successfully stored in DB.
```

The list of codes should now include your new code `raspa@aws`

```terminal
$ verdi computer test aws
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

Creating a new calculation
--------------------------

To start please [download the AiiDA submission script](/assets/2018_EPFL_molsim/raspa_submission.zip). To
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
machine). For this example use codename `raspa@aws`.

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
