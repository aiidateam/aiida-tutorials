from aiida.orm import Int, Code
from aiida.engine import WorkChain, calcfunction, ToContext
from aiida.plugins.factories import CalculationFactory

ArithmeticAddCalculation = CalculationFactory("arithmetic.add")

@calcfunction
def multiplication(x, y):
    return x * y

class MultiplyAddWorkChain(WorkChain):
    """WorkChain to multiply two numbers and add a third, for testing and demonstration purposes."""

    @classmethod
    def define(cls, spec):
        """Specify inputs and outputs."""
        super().define(spec)

        spec.input("x", valid_type=Int)
        spec.input("y", valid_type=Int)
        spec.input("z", valid_type=Int)
        spec.input("code", valid_type=Code)

        spec.outline(
            cls.multiply,
            cls.add,
            cls.gather_results
        )
        
        spec.output("product", valid_type=Int)
        spec.output("final_result", valid_type=Int)

    def multiply(self):
        """Multiply two integers."""
        
        product = multiplication(self.inputs.x, self.inputs.y)

        # Passing to context to be used by other functions
        self.ctx.product = product

    def add(self):
        """Add two numbers using the `ArithmeticAddCalculation` calculation job plugin."""
        
        # Submitting the calculation job `ArithmeticAddCalculation`
        calc_job_node = self.submit( ArithmeticAddCalculation, x=self.ctx.product, y=self.inputs.z, code=self.inputs.code )

        return ToContext(addition = calc_job_node)

    def gather_results(self):
        """Gathering and declaring the results."""

        product  = self.ctx.product
        addition = self.ctx.addition.outputs.sum

        self.out("product"     , product)
        self.out("final_result", addition)