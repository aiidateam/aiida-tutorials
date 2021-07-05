from aiida.orm import Int
from aiida.engine import WorkChain, calcfunction


@calcfunction
def multiplication(x, y):
    return x * y


@calcfunction
def add(x, y):
    return x + y


class MultiplyAddWorkChain(WorkChain):
    """WorkChain to multiply two numbers and add a third, for testing and demonstration purposes."""

    @classmethod
    def define(cls, spec):
        """Specify inputs and outputs."""
        super().define(spec)

        spec.input("x", valid_type=Int)
        spec.input("y", valid_type=Int)
        spec.input("z", valid_type=Int)

        spec.outline(cls.multiply, cls.add)

        spec.output("product", valid_type=Int)
        spec.output("final_result", valid_type=Int)

    def multiply(self):
        """Multiply two integers."""

        product = multiplication(self.inputs.x, self.inputs.y)

        # Passing to context to be used by other functions
        self.ctx.product = product

        # Declaring one of the outputs
        self.out("product", product)

    def add(self):
        """Add two integers."""

        # Call `add` using a variable from the context and one of the inputs
        result = add(self.ctx.product, self.inputs.z)

        # Parsing the output
        self.out("final_result", result)
