Getting set up
===============

Download and install the [Quantum Mobile virtual machine](https://github.com/marvel-nccr/quantum-mobile/releases/tag/18.06.0),
which comes both with AiiDA already preconfigured and with a number of useful
codes and tools for computational materials science.

Start the virtual machine, open a terminal window and
type

```terminal
$ workon aiida
```

This activates the virtual environment, in which AiiDA is installed.

Since Quantum Mobile focuses on *ab initio* calculations, it is missing
some aiida plugins we are going to need. Let’s install them (this can
take 3 minutes):

```terminal
$ pip install aiidalab==19.01.1
```

Furthermore, you are currently using the `default` AiiDA profile.

```terminal
$ verdi profile list
```

At the end of the tutorial, we'll ask you to submit the data you computed, 
so let's create a new profile in order to associate this data with you:

```terminal
$ verdi quicksetup
Profile name [quicksetup]: molsim2019
Email Address (identifies your data when sharing): leopold.talirz@epfl.ch
First Name: Leopold
Last Name: Talirz
Institution: EPFL
Executing now a migrate command...
...for Django backend
Operations to perform:
  Apply all migrations: contenttypes, db, sites, auth, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying db.0001_initial... OK
  Applying db.0002_db_state_change... OK
  Applying db.0003_add_link_type... OK
  Applying db.0004_add_daemon_and_uuid_indices... OK
  Applying db.0005_add_cmtime_indices... OK
  Applying db.0006_delete_dbpath... OK
  Applying db.0007_update_linktypes... OK
  Applying db.0008_code_hidden_to_extra... OK
  Applying sessions.0001_initial... OK
  Applying sites.0001_initial... OK
Database was created successfully
Loading new environment...
Installing default AiiDA user...
Starting user configuration for leopold.talirz@epfl.ch...
Configuring a new user with email 'leopold.talirz@epfl.ch'
>> User Leopold Talirz saved. <<
** NOTE: no password set for this user, 
         so he/she will not be able to login
         via the REST API and the Web Interface.
Setup finished.
The default profile for the 'verdi' process is set to 'default': do you want to set the newly created 'molsim2019' as the new default? (can be reverted later) [y/N]: y
The default profile for the 'daemon' process is set to 'default': do you want to set the newly created 'molsim2019' as the new default? (can be reverted later) [y/N]: y
```

Use `verdi profile list` to verify that you've switched to your new personal AiiDA profile.

If you encounter any issues throughout the tutorial, please consider

 * consulting the extensive [AiiDA documentation](https://aiida-core.readthedocs.io/en/stable/)
 * opening a new issue on the [tutorial issue tracker](https://github.com/ltalirz/aiida-tutorials/issues)
 * asking your neighbor 
 * asking a tutor

