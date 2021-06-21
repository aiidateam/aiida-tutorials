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
        spec.outline(cls.add, cls.result)
        spec.output("workchain_result", valid_type=Int)

    def add(self):
        """Sum the inputs."""

        # Call `add` using a variable from the context and one of the inputs
        summation = add(self.inputs.x, self.inputs.y)

        # Passing to context to be used by other functions
        self.ctx.summation = summation

    def result(self):
        """Parse the result."""

        # Declaring the output
        self.out("workchain_result", self.ctx.summation)


# Passing to context

# from aiida.engine import run
# from add_workchain_3 import MultiplyAddWorkChain
# result = run(MultiplyAddWorkChain, x=Int(2), y=Int(3) )
