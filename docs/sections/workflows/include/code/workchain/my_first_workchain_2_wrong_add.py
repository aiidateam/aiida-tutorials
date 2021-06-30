from aiida.orm import Int
from aiida.engine import WorkChain


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
        """Parse the result."""

        summation = self.inputs.x + self.inputs.y
        # Declaring the output
        self.out("workchain_result", summation)
