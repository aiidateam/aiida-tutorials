
(hackathon)=

# Hackathon

Examples to work on during the hackathon today:

- ConvergenceWorkChain: Write a work chain that automatically does a convergence test for the energy cutoff or k-points density.
  First just make a List input that specifies e.g. the energy cutoffs you want to test.
  And then try to write the step that ``submit``s all the calculation jobs with the correct inputs.
  You can use the {ref}`EquationOfState work chain <workflows-writing-workchains-eos-workchain>` as an example to start from!

- Improve the {ref}`EquationOfState work chain <workflows-writing-workchains-eos-workchain>` to have more flexibility.
  You could for example add a List input that allows the user to specify the scaling factors instead of having them hard-coded.
  Next, you could also expose the inputs as explained in the [Extending workflows how-to](https://aiida.readthedocs.io/projects/aiida-core/en/latest/howto/write_workflows.html#extending-workflows) to allow the user to specify the inputs of the PwCalculation, instead of them being generated using the ``generate_scf_input_params`` function in the utils.py script.
