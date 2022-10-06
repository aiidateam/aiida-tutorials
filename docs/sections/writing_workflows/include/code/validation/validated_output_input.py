from aiida.orm import Int
from aiida.engine import WorkChain


def validate_x(node, _):
    """Validate the ``x`` input, making sure it is positive."""
    if not node.value > 0:
        return "the `x` input must be a positive integer."


class OutputInputWorkChain(WorkChain):
    """Toy WorkChain that simply passes the input as an output."""

    @classmethod
    def define(cls, spec):
        """Specify inputs, outputs, and the workchain outline."""
        super().define(spec)

        spec.input("x", valid_type=Int, validator=validate_x)
        spec.outline(cls.result)
        spec.output("workchain_result", valid_type=Int)

    def result(self):
        """Pass the input as an output."""

        # Declaring the output
        self.out("workchain_result", self.inputs.x)
