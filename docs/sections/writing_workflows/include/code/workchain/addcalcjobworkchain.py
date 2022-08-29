from aiida.orm import Int, Code
from aiida.engine import WorkChain, calcfunction, ToContext
from aiida.plugins.factories import CalculationFactory

ArithmeticAddCalculation = CalculationFactory("core.arithmetic.add")


class AddCalcjobWorkChain(WorkChain):
    """WorkChain to add two integers."""

    @classmethod
    def define(cls, spec):
        """Specify inputs, outputs, and the workchain outline."""
        super().define(spec)

        spec.input("x", valid_type=Int)
        spec.input("y", valid_type=Int)
        spec.input("code", valid_type=Code)
        spec.outline(cls.add, cls.result)
        spec.output("workchain_result", valid_type=Int)

    def add(self):
        """Sum the inputs."""

        # Submitting the calculation job `ArithmeticAddCalculation`
        calc_job_node = self.submit(
            ArithmeticAddCalculation,
            x=self.inputs.x,
            y=self.inputs.y,
            code=self.inputs.code,
        )

        return ToContext(add_node=calc_job_node)

    def result(self):
        """Parse the result."""

        # Declaring the output
        self.out("workchain_result", self.ctx.add_node.outputs.sum)
