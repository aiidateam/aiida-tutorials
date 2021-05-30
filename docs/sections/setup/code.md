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

# Codes

Now that we have our localhost set up, let's configure the `Code`, namely the `pw.x` executable.
As with the computer, we have prepared a configuration file for you to {download}`download <include/config/code.yml>`.
This is its content:

```{literalinclude} include/config/code.yml
:language: yaml

```

Once you have the configuration file in your local working environment, set up the code:

```{code-block} console

$ verdi code setup --config code.yml

```

Try to understand the various parameters in the YAML file.
In particular, we note that this code needs the `quantumespresso.pw` plugin, and we are specifying the fact that the code is already present on the computer, the absolute path to this code, the name of the AiiDA computer (`localhost`) on which it is, and some text to prepend before each execution (in this case `ulimit -s unlimited`, but in other cases it could e.g. be a `module load`).

:::{warning}

The configuration should work for the virtual machine that comes with this tutorial.
If you are following this tutorial in a different environment, you will need to install Quantum ESPRESSO and adapt the configuration to your needs, as explained in the [aiida online documentation](<https://aiida.readthedocs.io/projects/aiida-core/en/latest/howto/run_codes.html#how-to-setup-a-code>).

:::

Similar to the computers, you can list all the configured codes with:

```{code-block} console

$ verdi code list

```

Verify that it now contains a code named `qe-6.5-pw` that we just configured.
You can always check the configuration details of an existing code using:

```{code-block} console

$ verdi code show qe-6.5-pw

```

:::{note}

The `generic` profile has already a number of other codes configured.
See `verdi -p generic code list`.

In order to also show codes created by other users (e.g. from imported archives), use `verdi code list -A`.

:::
