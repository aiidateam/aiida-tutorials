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
        spec.outline(cls.add, cls.result)
        spec.output("workchain_result", valid_type=Int)

    def add(self):
        """Sum the inputs."""

        # Call `addition` using a variable from the context and one of the inputs
        addition_result = addition(self.inputs.x, self.inputs.y)

        # Passing to context to be used by other functions
        self.ctx.summation = addition_result

    def result(self):
        """Parse the result."""

        # Declaring the output
        self.out("workchain_result", self.ctx.summation)
