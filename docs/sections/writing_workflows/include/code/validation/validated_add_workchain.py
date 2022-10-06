from aiida.orm import Int
from aiida.engine import WorkChain, calcfunction


@calcfunction
def addition(x, y):
    return x + y


def validate_inputs(inputs, _):
    """Validate the top-level inputs."""
    if inputs["x"].value * inputs["y"].value < 0:
        return "The `x` and `y` inputs cannot be of the opposite sign."


class AddWorkChain(WorkChain):
    """WorkChain to add two integers."""

    @classmethod
    def define(cls, spec):
        """Specify inputs, outputs, and the workchain outline."""
        super().define(spec)

        spec.input("x", valid_type=Int)
        spec.input("y", valid_type=Int)
        spec.inputs.validator = validate_inputs

        spec.outline(cls.result)
        spec.output("workchain_result", valid_type=Int)

    def result(self):
        """Sum the inputs and parse the result."""

        # Call `addition` using the two inputs
        addition_result = addition(self.inputs.x, self.inputs.y)

        # Declaring the output
        self.out("workchain_result", addition_result)
