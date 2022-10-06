from aiida.orm import Int, Float
from aiida.engine import WorkChain, calcfunction


@calcfunction
def addition(x, y):
    return x + y


@calcfunction
def multiplication(x, y):
    return x * y


def validate_z(node, _):
    """Validate the `z` input."""
    if node.value == 0:
        return "The value of `z` can not be zero."


def validate_inputs(inputs, _):
    """Validate the top-level inputs."""
    if inputs["x"] + inputs["y"] == 0:
        return "The sum of `x` and `y` can not be zero."


class MultiplyAddWorkChain(WorkChain):
    """WorkChain to multiply two integers and add a third."""

    @classmethod
    def define(cls, spec):
        """Specify inputs, outputs, and the workchain outline."""
        super().define(spec)

        spec.input("x", valid_type=(Int, Float))
        spec.input("y", valid_type=(Int, Float))
        spec.input("z", valid_type=Int, validator=validate_z)
        spec.inputs.validator = validate_inputs

        spec.outline(cls.multiply, cls.add, cls.result)
        spec.output("workchain_result", valid_type=(Int, Float))
        spec.output("product", valid_type=(Int, Float))

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
