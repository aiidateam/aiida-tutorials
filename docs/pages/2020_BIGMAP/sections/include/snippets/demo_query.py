from aiida.orm import Group
from aiida.plugins import DataFactory, CalculationFactory

PwCalculation = CalculationFactory('quantumespresso.pw')
StructureData = DataFactory('structure')
Dict = DataFactory('dict')

import matplotlib.pyplot as plt

qb = QueryBuilder().append( 
    Group, filters={'label': {'like': 'tutorial_%'}}, tag='group',
    project='label'
).append( 
    PwCalculation, with_group='group', tag='pw' 
).append( 
    StructureData, with_outgoing='pw', 
    project='extras.formula' 
).append(
    Dict, with_incoming='pw', filters={'attributes.absolute_magnetization': {'>': 0.0}}, 
    project='attributes.absolute_magnetization'
)

results_dict = dict()
formulas = set()

for group_label, formula, abs_magnetization in qb.iterall():
    functional = group_label.split('_')[1].upper()
    results_dict.setdefault(functional, {})
    results_dict[functional][formula] = abs_magnetization
    formulas.add(formula)

formulas = list(formulas)

for functional, results in results_dict.items():

    abs_magnetizations = [results[formula] for formula in formulas]

    plt.plot(abs_magnetizations, 's')
    plt.xticks(range(len(formulas)), formulas, rotation=90)
    plt.ylabel('Magnetization [Bohrmag / cell]')

plt.legend(results_dict.keys())
plt.tight_layout()
plt.savefig('demo_query.pdf')
