from aiida.orm import Int
from aiida.engine import WorkChain, calcfunction


@calcfunction
def addition(x, y):
    return x + y


class AddWorkChain(WorkChain):
    """WorkChain to add two integers."""

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

        # Call `addition` using the two inputs
        addition_result = addition(self.inputs.x, self.inputs.y)

        # Declaring the output
        self.out("workchain_result", addition_result)
