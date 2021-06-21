from aiida.orm import Int
from aiida.engine import WorkChain, calcfunction


@calcfunction
def add(x, y):
    return x + y


@calcfunction
def multiplication(x, y):
    return x * y


class MultiplyAddWorkChain(WorkChain):
    """WorkChain to multiply two numbers and add a third, for testing and demonstration purposes."""

    @classmethod
    def define(cls, spec):
        """Specify inputs, outputs, and the workchain outline."""
        super().define(spec)

        spec.input("x", valid_type=Int)
        spec.input("y", valid_type=Int)
        spec.input("z", valid_type=Int)
        spec.outline(cls.multiply, cls.add, cls.result)
        spec.output("workchain_result", valid_type=Int)

    def multiply(self):
        """Multiply two integers."""

        product = multiplication(self.inputs.x, self.inputs.y)

        # Passing to context to be used by other functions
        self.ctx.product = product

    def add(self):
        """Sum the inputs."""

        # Call `add` using a variable from the context and one of the inputs
        summation = add(self.ctx.product, self.inputs.z)

        # Passing to context to be used by other functions
        self.ctx.summation = summation

    def result(self):
        """Parse the result."""

        # Declaring the output
        self.out("workchain_result", self.ctx.summation)


# Add another calcfunction and another input


# from aiida.engine import run
# from add_workchain_3 import MultiplyAddWorkChain
# result = run(MultiplyAddWorkChain, x=Int(2), y=Int(3), z=Int(7) )

# Do verdi process show
# One of the outputs in going to be the same node as the input, the other is going to be a new node
