from aiida.orm import Int
from aiida.engine import WorkChain


class OutputInputWorkChain(WorkChain):
    """WorkChain to multiply two numbers and add a third, for testing and demonstration purposes."""

    @classmethod
    def define(cls, spec):
        """Specify inputs, outputs, and the workchain outline."""
        super().define(spec)

        spec.input("x", valid_type=Int)
        spec.outline(cls.result)
        spec.output("workchain_result", valid_type=Int)

    def result(self):
        """Parse the result."""

        # Declaring the output
        self.out("workchain_result", self.inputs.x)
