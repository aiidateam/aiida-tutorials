---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: '0.8'
    jupytext_version: 1.4.1+dev
kernelspec:
  display_name: Python 3
  name: python3
---

(setup-computer)=
# Computers

In a production environment, AiiDA would typically be running on your work station or laptop, while launching calculations on remote high-performance compute resources that you have SSH access to.
For this reason AiiDA has the concept of a `Computer` to run calculations on.

To keep things simple, Quantum ESPRESSO (together with several other *ab initio* codes) has been installed directly in your virtual machine, and you are going to launch your first calculations on the same computer where AiiDA is installed.
Nevertheless, even if it is the same computer, we need to create a new `Computer` instance in AiiDA in order to launch calculations on it:

```{code-block} console

$ verdi computer setup --config computer.yml

```

where `computer.yml` is a configuration file in the [YAML format](<https://en.wikipedia.org/wiki/YAML#Syntax>)  that you can {download}`download here <include/config/computer.yml>`. This is its content:

```{literalinclude} include/config/computer.yml
:language: yaml

```

:::{note}

When used without the `--config` option, `verdi computer setup` will prompt you for the required information, just like you have seen when {ref}`setting up a profile<2020_virtual_intro:setup_profile>`.
The configuration file should work for the virtual machine that comes with this tutorial but may need to be adapted when you are running AiiDA in a different environment, as explained in the [aiida online documentation](<https://aiida.readthedocs.io/projects/aiida-core/en/latest/howto/run_codes.html#how-to-set-up-a-computer>).

:::

The `computer setup` step informs AiiDA of the existence of the computer and of its basic settings, like the scheduler installed on it. Before being able to use the computer, you also need to provide AiiDA with information on how to access the `Computer`.
For remote computers with `ssh` transport, this would involve e.g. an SSH key, the username on the remote computer, the port to connect to, etc.
For `local` computers, this is just a "formality" (press enter to confirm the default cooldown time, that is the time between consecutive opening of a connection - for a local computer this can be safely set to zero, while when connecting via SSH it is better to leave a time of a few seconds, to avoid overloading of the remote computer):

```{code-block} console

$ verdi computer configure local localhost

```

:::{note}

For remote computers with `ssh` transport, use `verdi computer configure ssh` instead of `verdi computer configure local`.

:::

Your `localhost` computer should now show up in

```{code-block} console

$ verdi computer list

```

:::{note}

AiiDA export archives like the one we imported {ref}`in the very beginning <2020_virtual_importing_data>` can also contain computers set up by other AiiDA users (without the private *configuration* information).
Use `verdi computer list -a` to list both configured and unconfigured computers.

:::

Before proceeding, test that it works:

```{code-block} console

$ verdi computer test localhost

```
