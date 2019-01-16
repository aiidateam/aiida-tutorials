# Setting up remote computers and codes

AiiDA manages calculations from start to finish, submitting input files to
remote (super)computers, monitoring the job queue and getting results back
to your computer.

In order for AiiDA to take care of this for you, you'll need to tell AiiDA
once how to connect to the remote computer and how to run the simulation codes.

## Computer setup and configuration

For the tutorial, we have access to a compute cluster from the University of Amsterdam.
Let's set up passwordless access using the secure shell (SSH) protocol.

First, generate a new public/private SSH key pair.

```terminal
$ ssh-keygen -t rsa
Generating public/private rsa key pair. 
Enter file in which to save the key (/home/max/.ssh/id_rsa): <Enter> 
Enter passphrase (empty for no passphrase): <Enter> 
Enter same passphrase again: <Enter> 
Your identification has been savedin /home/max/.ssh/id_rsa. 
Your public key has been saved in /home/max/.ssh/id_rsa.pub. 
The key fingerprint is: ... 
The key's randomart image is: ... 
```
> **Note**  
> Be careful not to overwrite your own key pairs when running this
> outside Quantum Mobile.

Then, copy the public key to the compute cluster:
```terminal
$ ssh-copy-id molsim<n>@bazis-h1.science.uva.nl

/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
**********************************************************************
          Welcome to the Amsterdam/UvA FNWI research cluster.
                         Faculty of Science
                    (http://www.science.uva.nl)
              University of Amsterdam,  The Netherlands


             Only AUTHORIZED USERS may access this site.

All actions are logged. If you don't like this policy, disconnect now.

       Note: The bazis-h1 defq has access to 32 cores per node

**********************************************************************
  Faculty Expert-IT Support Group (mailto:feiog-tech-science@uva.nl)
**********************************************************************
molsim<n>@bazis-h1.science.uva.nl's password:

Number of key(s) added: 1
```

Now try logging in to the cluster with `ssh molsim<n>@bazis-h1.science.uva.nl`,
which should work without password.
Once it does, let's set up the `bazis` computer in AiiDA as follows:

```terminal
$ verdi computer setup 
At any prompt, type ? to get some help.
————————————— 
=> Computer name: bazis
Creating new computer with name 'bazis'
=> Fully-qualified hostname: bazis-h1.science.uva.nl
=> Description: bazis computer for the molsim course
=> Enabled: True 
=> Transport type: ssh 
=> Scheduler type: slurm
=> shebang line at the beginning of the submission script: #!/bin/bash
=> AiiDA work directory: /home/{username}/aiida_run/
=> mpirun command: srun -n {tot_num_mpiprocs}
=> Default number of CPUs per machine: 1 
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

At this point, the computer node has been created in the database

```terminal
$ verdi computer list -a
```

but access hasn't been configured yet.

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
=> gsshost = bazis-h1.science.uva.nl
=> load system hostkeys = True
=> key policy = AutoAddPolicy
Configuration stored for your user on computer 'bazis'.
```

Finally, let AiiDA test the computer setup we just created:

```terminal
$ verdi computer test bazis
Testing computer 'bazis' for user leopold.talirz@epfl.ch...
> Testing connection...
> Getting job list...
  `-> OK, 1 jobs found in the queue.
> Creating a temporary file in the work directory...
  `-> Getting the remote user name...
      [remote username: molsim20]
      [Checking/creating work directory: /home/molsim20/aiida_run/]
  `-> Creating the file tmpjzXXrC...
  `-> Checking if the file has been created...
      [OK]
  `-> Retrieving the file and checking its content...
      [Retrieved]
      [Content OK]
  `-> Removing the file...
  [Deleted successfully]
Test completed (all 3 tests succeeded)
```

## Code setup and configuration

Next, we need to let AiiDA know about the computer codes available on `bazis`.

We've already installed [RASPA2](https://github.com/numat/RASPA2) there,
so you can set up the code as follows:

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
> **Note**  
> Rember to include the line `export RASPA_DIR=/home/molsim20/raspa/`
> as `Text to prepend to each command execution`, otherwise RASPA won't run.

The list of codes should now include your new code `raspa@bazis`

```terminal
$ verdi code list
```

## The AiiDA daemon

The AiiDA daemon is a program running all the time in the background, checking
for new calculations that need to be submitted. The daemon also takes care of
all the necessary operations before the calculation submission, and after the
calculation has completed on the cluster. 

Let's check whether the AiiDA daemon is already running. 

```terminal
$ verdi daemon status
# Most recent daemon timestamp:0h:00m:26s ago
## Found 1 process running:
   * aiida-daemon[aiida-daemon] RUNNING    pid 15044, uptime 3 days, 15:38:41
```

If the daemon is not running, please start it

```terminal
$ verdi daemon start
```

> **Note**  
> AiiDA supports multiple profiles but for reasons of consistency
> only one profile can communicate with the daemon at a time.
> When starting the daemon, you may therefore see an error message like
> ```terminal
> You are not the daemon user! I will not start the daemon.
> (The daemon user is 'aiida@localhost', you are 'some.body@xyz.com')
>
> ** FOR ADVANCED USERS ONLY: **
> To change the current default user, use 'verdi install --only-config'
> To change the daemon user, use 'verdi daemon configureuser'
> ```
> Just follow the instructions by running
> ```terminal
> $ verdi daemon configureuser
> ```
> and provide the email address of your profile in order to allow your user to run the daemon
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
> Now start the daemon!

