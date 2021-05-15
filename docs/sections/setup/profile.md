(setup-profile)=

# Setting up a profile

After installing AiiDA, the first step is to create a "profile".
Typically, you would be using one profile per independent research project.

The easiest way of setting up a new profile is through `verdi quicksetup`.
Let's set up a new profile that we will use throughout this tutorial:

```{code-block} console

$ verdi quicksetup

```

This will prompt you for some information, such as the name of the profile, your name, etc.
The information about you as a user will be associated with all the data that you create in AiiDA
and it is important for attribution when you will later share your data with others.
After you have answered all the questions, a new profile will be created, along
with the required {ref}`database and repository.<aiida:intro:install:database>`

```{note}

`verdi quicksetup` is a user-friendly wrapper around the `verdi setup` command that provides more control over the profile setup.
As explained in [the documentation](<https://aiida.readthedocs.io/projects/aiida-core/en/latest/intro/installation.html#aiida-profile-custom-setup>), `verdi setup` expects certain external resources (such as the database and RabbitMQ) to already have been pre-configured.
`verdi quicksetup` will try to do this for you, but may not be successful in certain environments.

```

To check that a new profile has been generated (in our case, called `quicksetup`), along with any other that may have been already configured, run:

```{code-block} console

$ verdi profile list

Info: configuration folder: /home/max/.aiida
* generic
  quicksetup

```

Each line, `generic` and `quicksetup` in this example, corresponds to a profile.
The one marked with an asterisk is the "default" profile, meaning that any `verdi` command that you execute will be applied to that profile.

```{note}

The output you will get may differ.
The `generic` profile is pre-configured on the virtual machine built for the tutorial (but we are not going to use it here).

```

Let's change the default profile to the newly created `quicksetup` for the rest of the tutorial:

```{code-block} console

$ verdi profile setdefault quicksetup

```

From now on, all `verdi` commands will apply to the `quicksetup` profile.

```{note}

To quickly perform a single command on a profile that is not the default, use the `-p/--profile` option:
For example, `verdi -p generic code list` will display the codes for the `generic` profile, despite it not being the current default profile.

```
