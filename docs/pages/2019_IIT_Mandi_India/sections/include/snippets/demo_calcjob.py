"""Run SCF calculation with Quantum ESPRESSO"""
from aiida.orm.nodes.data.upf import get_pseudos_from_structure
from aiida.engine import submit

code = Code.get_from_string("<CODE LABEL>")  # REPLACE <CODE LABEL>
builder = code.get_builder()

# Select structure
structure = load_node(<STRUCTURE PK>)  # REPLACE <STRUCTURE PK>
builder.structure = structure

# Define calculation
parameters = {
  'CONTROL': {
    'calculation': 'scf',  # self-consistent field
  },
  'SYSTEM': {
    'ecutwfc': 30.,  # wave function cutoff in Ry
    'ecutrho': 240.,  # density cutoff in Ry
  },
}  
builder.parameters = Dict(dict=parameters)

# Select pseudopotentials
builder.pseudos = get_pseudos_from_structure(structure, '<PP FAMILY>')  # REPLACE <PP FAMILY>

# Define K-point mesh in reciprocal space
KpointsData = DataFactory('array.kpoints')
kpoints = KpointsData()
kpoints.set_kpoints_mesh([4,4,4])
builder.kpoints = kpoints

# Set resources
builder.metadata.options.resources = {'num_machines': 1} 

# Submit the job
calcjob = submit(builder)
print('Submitted CalcJob with PK=' + str(calcjob.pk))
