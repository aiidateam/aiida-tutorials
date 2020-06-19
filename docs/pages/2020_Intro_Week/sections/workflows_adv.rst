.. _2020_virtual_intro:workflow_adv:

******************
Advanced Workflows
******************

In this hands-on we'll be looking at some more advanced concepts related to workflows.


Exit Codes
==========


  Exit codes are used to clearly communicate known failure modes of the work chain to the user.
  The first and second arguments define the ``exit_status`` of the work chain in case of failure (``400``) and the string that the developer can use to reference the exit code (``ERROR_NEGATIVE_NUMBER``).
  A descriptive exit message can be provided using the ``message`` keyword argument.
  For the ``MultiplyAddWorkChain``, we demand that the final result is not a negative number, which is checked in the ``validate_result`` step of the outline.


.. literalinclude:: include/snippets/workflows_multiply_add.py
    :language: python
    :pyobject: MultiplyAddWorkChain.validate_result
    :dedent: 4

Once the ``ArithmeticAddCalculation`` calculation job is finished, the next step in the work chain is to validate the result, i.e. verify that the result is not a negative number.
After the ``addition`` node has been extracted from the context, we take the ``sum`` node from the ``ArithmeticAddCalculation`` outputs and store it in the ``result`` variable.
In case the value of this ``Int`` node is negative, the ``ERROR_NEGATIVE_NUMBER`` exit code - defined in the ``define()`` method - is returned.
Note that once an exit code is returned during any step in the outline, the work chain will be terminated and no further steps will be executed.