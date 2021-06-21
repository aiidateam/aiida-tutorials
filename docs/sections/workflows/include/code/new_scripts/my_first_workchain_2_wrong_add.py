from aiida.orm import Int
from aiida.engine import WorkChain


class AddWorkChain(WorkChain):
    """WorkChain to multiply two numbers and add a third, for testing and demonstration purposes."""

    @classmethod
    def define(cls, spec):
        """Specify inputs, outputs, and the workchain outline."""
        super().define(spec)

        spec.input("x", valid_type=Int)
        spec.input("y", valid_type=Int)
        spec.outline(cls.result)
        spec.output("workchain_result", valid_type=Int)

    def result(self):
        """Parse the result."""

        summation = self.inputs.x + self.inputs.y

        # Declaring the output
        self.out("workchain_result", summation)


# from aiida.engine import run
# from add_workchain_3 import MultiplyAddWorkChain
# result = run(MultiplyAddWorkChain, x=Int(2), y=Int(3) )

# ValueError: Workflow<MultiplyAddWorkChain> tried returning an unstored `Data` node. This likely means new `Data` is being created inside the workflow. In order to preserve data provenance, use a `calcfunction` to create this node and return its output from the workflow
