from aiida.orm import Int
from aiida.engine import WorkChain, calcfunction


@calcfunction
def addition(x, y):
    return x + y


@calcfunction
def multiplication(x, y):
    return x * y


class MultiplyAddWorkChain(WorkChain):
    """WorkChain to multiply two integers and add a third."""

    @classmethod
    def define(cls, spec):
        """Specify inputs, outputs, and the workchain outline."""
        super().define(spec)

        spec.input("x", valid_type=Int)
        spec.input("y", valid_type=Int)
        spec.input("z", valid_type=Int)
        spec.outline(cls.multiply, cls.add, cls.result)
        spec.output("workchain_result", valid_type=Int)
        spec.output("product", valid_type=Int)

    def multiply(self):
        """Multiply two integers."""

        multiplication_result = multiplication(self.inputs.x, self.inputs.y)

        # Passing to context to be used by other functions
        self.ctx.product = multiplication_result

    def add(self):
        """Add two numbers."""

        # Call `addition` using a variable from the context and one of the inputs
        addition_result = addition(self.ctx.product, self.inputs.z)

        # Passing to context to be used by other functions
        self.ctx.summation = addition_result

    def result(self):
        """Parse the result."""

        # Declaring the output
        self.out("workchain_result", self.ctx.summation)
        self.out("product", self.ctx.product)
