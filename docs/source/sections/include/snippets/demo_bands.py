"""Compute a band structure with Quantum ESPRESSO

Uses the PwBandStructureWorkChain provided by aiida-quantumespresso.
"""
from aiida.engine import submit
PwBandStructureWorkChain = WorkflowFactory('quantumespresso.pw.band_structure')

results = submit(
    PwBandStructureWorkChain,
    code=Code.get_from_string("<CODE LABEL>"), # REPLACE <CODE LABEL>
    structure=load_node(<PK>),  # REPLACE <PK>
)
