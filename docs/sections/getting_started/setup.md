(fundamentals-setup)=

# Set up

## Set up AiiDA on your own machine

To run the tutorial material on your own machine, you need to install:

- [AiiDA](https://aiida.readthedocs.io/projects/aiida-core/en/latest/intro/get_started.html) (version 2.0.4)
- [aiida-quantumespresso](https://aiida-quantumespresso.readthedocs.io/en/latest/installation/index.html) (version 4.0.1)
- [Quantum ESPRESSO](https://www.quantum-espresso.org/) (version 7.0)

```{note} Version numbers indicate the versions with which the tutorial was tested.
```

## Using Quantum Mobile

The tutorial can be run in the Quantum Mobile virtual machine.
Simply:

1. Download the tutorial image via [this link](https://drive.google.com/file/d/1xaZ4AZuyXoJ-sLKkaZpJQwvmWpkiykMq/view?usp=sharing).
2. Install [Virtual Box](https://www.virtualbox.org/) 6.1.6 or later.
3. Import the virtual machine image into Virtualbox: `File => Import Appliance`

## Using AiiDAlab Launch

AiiDAlab Launch makes it easy to run AiiDA on your own workstation or laptop.

To use AiiDAlab launch you will have to

1. [Install Docker on your workstation or laptop](https://docs.docker.com/get-docker/) and [Manage Docker as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/).
2. Install AiiDAlab launch with [pipx](https://pipx.pypa.io/stable/installation/) (**recommended**):

   ```console
   pipx install aiidalab-launch
   ```

   _Or directly with pip (`pip install aiidalab-launch`)._

3. Create a profile for tutorial

    ```console
    aiidalab-launch profiles add tutorial
    ```

    It will ask you to edit the profile, since for the tutorial we only need the AiiDA environment, answer `Y` and let's remove the `aiidalab-widgets-base` from the `default_apps` list (or the whole `default_apps` line).

3. Start AiiDAlab for `tutorial` profile with

    ```console
    aiidalab-launch start -p tutorial
    ```
4. Follow the instructions on screen to open AiiDAlab in the browser.

See `aiidalab-launch --help` for detailed help.

:::{note} **Deploying AiiDAlab on Microsoft Azure**

For our tutorial events, we use an AiiDAlab deployment on Microsoft Azure.
Interested in having your own deployment of AiiDAlab on the Microsoft Azure Kubernetes Service?
You can find all instructions on the corresponding GitHub repository:

[https://github.com/aiidalab/aiidalab-on-azure](https://github.com/aiidalab/aiidalab-on-azure)

:::
