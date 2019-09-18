"""Compute a band structure with Quantum ESPRESSO

Uses the PwBandStructureWorkChain provided by aiida-quantumespresso.
"""
from aiida.engine import submit
PwBandStructureWorkChain = WorkflowFactory('quantumespresso.pw.band_structure')

results = submit(
    PwBandStructureWorkChain,
    code=Code.get_from_string("qe-6.4.1-pw@localhost"),
    structure=load_node(<PK>),  # REPLACE <PK>
)
