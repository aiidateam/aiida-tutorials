(plugins-from_scratch)=

# Developing a workflow plugin and publish it from scratch - Example

**Task:** From scratch, build an AiiDA plugin development environment. 
By using AiiDA plugin cookie-cutter, create an AiiDA plugin consists of work chain based on the pwscf calculations plugins from [`aiida-quantumespresso`](https://github.com/aiidateam/aiida-quantumespresso). 
Publishing the plugin to [AiiDA plugins registry](https://aiidateam.github.io/aiida-registry/).

**Result:** Having an AiiDA plugin registried on AiiDA plugins registry which contain a workflow to run cohesive energy evaluation workflow based on chainning the processes from `aiida-quantumespresso`.

**Time:** This should be easily doable in the available 1h.

## Create a developing environment

To start, we need a developing environment where the AiiDA and its related infrastructures (e.g. PostgreSQL and RabbitMQ) are installed and running.
As shown in xx (aiidalab-launch), the aiidalab-launch will create and launch a docker container where the PostgreSQL, RabbitMQ and aiida-core are ready to use. 
All you need to do are:

1. Install Docker on your workstation or laptop.
2. Install AiiDAlab launch with pipx or directly with pip (pip install aiidalab-launch)
3. Start AiiDAlab with 

```
aiidalab-launch start
```
4. Follow the instructions on screen to open AiiDAlab in the browser.

In the browser it will connect to the Jupyter interface of AiiDAlab which consist of a terminal you can run all the AiiDA verdi commands, and a filesystem interface where you can manipulate with files.

The vscode support to configure and [developing project inside a container](https://code.visualstudio.com/docs/remote/containers).
This enable all the functionalities of vscode as developing in the localhost. 

First open the vscode and [attach to the running AiiDAlab container](https://code.visualstudio.com/docs/remote/attach-container) you just launched.

[image..]

The container mounted in vscode will have `root` as the default user, you need to change the user to `aiida` in attached container configuration files, either can be the configure file on image-level (default) or the configuration file tied to a container name (if you have multiple containers from the same image.). 
Set the value `remoteUser` to `aiida` as:

```json
{
    "remoteUser": "aiida",
}
```

Reopen the container in vscode to load the new configuration.
Now if you [open the integrated terminal of vscode](https://code.visualstudio.com/docs/terminal/basics#:~:text=To%20open%20the%20terminal%3A,the%20View%3A%20Toggle%20Terminal%20command.) from inside the attached container in your workspace, you'll find that you are the user `aiida`. 
It not only change the user to `aiida` in vscode but will map the GitHub credential from your localhost so you don't need to reset the GitHub configuration in vscode.

### [Option: intall the vscode extensions for vscode container environment]

We recommend to install `Python Extension Pack` extension pack for the python developing and `Better TOML` for the syntax highlight for the package setup `toml` file. 

## Create a plugin package from cookie-cutter.

In the vscode terminal run:

```
cookiecutter https://github.com/aiidateam/aiida-plugin-cutter.git
```

Just follow the instructions and answer the prompted questions.
This will produce the files and folder structure for your plugin, already adjusted for the name of your plugin.
Please check [aiida-plugin-cutter](https://github.com/aiidateam/aiida-plugin-cutter) for more details of how to use the cutter.
You will want to install your plugin in `editable` mode, so that changes to the source code of your plugin are immediately visible to other packages:

```
cd aiida_<name>
pip install -e .  # install in editable mode
```

Open the folder of the package you just create to start working the project.
You are now ready to start development!
If you have `Python Extension Pack` installed as shown in .., you can [select python interpreter for your project](https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment) to load the interpreter and have all modules of dependencies tractable by the vscode IDE.
It will allow you to see that the modules are synax highlight and able to go to the definition of the modules and functions to [quick navigate the code](https://code.visualstudio.com/docs/editor/editingevolved#_go-to-definition), which accelarate your development a lot.


## Write workflow to calculate cohesive energy using process from aiida-quantumespresso

### Install Quantum ESPRESSO and aiida-quantumespresso in container

Our target plugin will container a workflow which running Quantum Espresso `pw.x` from using the `PwBaseWorkChain` of `aiida-quantumespresso`.
The Quantum Espresso in this purpose is mostly for developing and testing purpose, it can be easily installed from conda forge:

```
$ conda create --yes --override-channels --channel conda-forge --prefix ~/.conda/envs/quantum-espresso-7.0-custom qe=7.0
```

The excutable `pw.x` can be then found from `~/.conda/envs/quantum-espresso-7.0-custom/bin/pw.x`.
Typically, to running a MPI `pw.x` calculation just in the working directory which pwscf inputs located, run:

```
$ ~/.conda/envs/quantum-espresso-7.0-custom/bin/mpirun -np 2 ~/.conda/envs/quantum-espresso-7.0-custom/bin/pw.x < pw.inp > pw.out
```

or activate the correspond conda environment first and run:

```
$ conda activate quantum-espresso-7.0-custom
$ mpirun -np 2 pw.x
```

Install the `aiida-quantumespresso` by just running:

```
$ pip install aiida-quantumespresso
```

and SSSP pseudopotential library by:

```
$ aiida-pseudo install sssp
```

You can then configure an aiida code for the `pw.x`:

```
$ verdi code setup --non-interactive --label pw-7.0 --description "pw.x (7.0)" --input-plugin quantumespresso.pw --computer localhost --prepend-text "conda activate quantum-espresso-7.0-custom" --remote-abs-path "/home/aiida/.conda/envs/quantum-espresso-7.0-custom/bin/pw.x"
```

### Writing workflow

Ref to 'writing_workflows-workchain' to create a EOS workflow.

Download `utils.py` and create `rescale.py` with the content from section in to `aiida_wf_demo`

Create a 'workflows.py' with the content of the WorkChain 'EquationOfState'.

Import the module:

```python
from aiida_wf_demo.rescale import rescale
from aiida_wf_demo.utils import generate_scf_input_params
```

### Adapt the package setup

- Registry the entry points.
- Specify the dependencies.
