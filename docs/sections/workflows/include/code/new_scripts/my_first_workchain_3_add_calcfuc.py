from aiida.orm import Int
from aiida.engine import WorkChain, calcfunction


@calcfunction
def add(x, y):
    return x + y


class AddWorkChain(WorkChain):
    """WorkChain to multiply two numbers and add a third, for testing and demonstration purposes."""

    @classmethod
    def define(cls, spec):
        """Specify inputs, outputs, and the workchain outline."""
        super().define(spec)

        spec.input("x", valid_type=Int)
        spec.input("y", valid_type=Int)
        spec.outline(cls.result)
        spec.output("workchain_result", valid_type=Int)

    def result(self):
        """Sum the inputs and parse the result."""

        # Call `add` using a variable from the context and one of the inputs
        summation = add(self.inputs.x, self.inputs.y)

        # Declaring the output
        self.out("workchain_result", summation)


# The output this time has a new id, it is a new node

# from aiida.engine import run
# from add_workchain_3 import MultiplyAddWorkChain
# result = run(MultiplyAddWorkChain, x=Int(2), y=Int(3) )
