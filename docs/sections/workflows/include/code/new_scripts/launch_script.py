from aiida.engine import run
from debugging_1_sintax_error import OutputInputWorkChain

result = run(OutputInputWorkChain, x=Int(4))
