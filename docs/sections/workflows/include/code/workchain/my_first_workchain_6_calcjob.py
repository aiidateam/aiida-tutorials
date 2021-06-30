from aiida.orm import Int, Code
from aiida.engine import WorkChain, calcfunction, ToContext
from aiida.plugins.factories import CalculationFactory

ArithmeticAddCalculation = CalculationFactory("arithmetic.add")


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
        spec.input("code", valid_type=Code)
        spec.outline(cls.multiply, cls.add, cls.result)
        spec.output("workchain_result", valid_type=Int)
        spec.output("product", valid_type=Int)

    def multiply(self):
        """Multiply two integers."""

        multiplication_result = multiplication(self.inputs.x, self.inputs.y)

        # Passing to context to be used by other functions
        self.ctx.product = multiplication_result

    def add(self):
        """Add two numbers using the `ArithmeticAddCalculation` calculation job plugin."""

        # Submitting the calculation job `ArithmeticAddCalculation`
        calc_job_node = self.submit(
            ArithmeticAddCalculation,
            x=self.ctx.product,
            y=self.inputs.z,
            code=self.inputs.code,
        )

        return ToContext(summation_calc_job=calc_job_node)

    def result(self):
        """Parse the result."""

        # Declaring the output
        self.out("workchain_result", self.ctx.summation_calc_job.outputs.sum)
        self.out("product", self.ctx.product)
