from aiida.orm import Int, Float
from aiida.engine import WorkChain


class OutputInputWorkChain(WorkChain):
    """Toy WorkChain that simply passes the input as an output."""

    @classmethod
    def define(cls, spec):
        """Specify inputs, outputs, and the workchain outline."""
        super().define(spec)

        spec.input("x", valid_type=(Int, Float))
        spec.outline(cls.result)
        spec.output("workchain_result", valid_type=Int)

    def result(self):
        """Pass the input as an output."""

        # Declaring the output
        self.out("workchain_result", self.inputs.x)
