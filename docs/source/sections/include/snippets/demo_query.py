from IPython.display import Image
from datetime import datetime, timedelta
import numpy as np
from matplotlib import gridspec, pyplot as plt

PwCalculation = CalculationFactory('quantumespresso.pw')
StructureData = DataFactory('structure')
KpointsData = DataFactory('array.kpoints')
Dict = DataFactory('dict')
UpfData = DataFactory('upf')


def plot_results(query_res):
    """
    :param query_res: The result of an instance of the QueryBuilder
    """
    smearing_unit_set, magnetization_unit_set, pseudo_family_set = set(), set(
    ), set()
    # Storing results:
    results_dict = {}
    for pseudo_family, formula, smearing, smearing_units, mag, mag_units in query_res:
        if formula not in results_dict:
            results_dict[formula] = {}
        # Storing the results:
        results_dict[formula][pseudo_family] = (smearing, mag)
        # Adding to the unit set:
        smearing_unit_set.add(smearing_units)
        magnetization_unit_set.add(mag_units)
        pseudo_family_set.add(pseudo_family)

    # Sorting by formula:
    sorted_results = sorted(results_dict.items())
    formula_list = next(zip(*sorted_results))
    nr_of_results = len(formula_list)

    # Checks that I have not more than 3 pseudo families.
    # If more are needed, define more colors
    #pseudo_list = list(pseudo_family_set)
    if len(pseudo_family_set) > 3:
        raise Exception('I was expecting 3 or less pseudo families')

    colors = ['b', 'r', 'g']

    # Plotting:
    plt.clf()
    fig = plt.figure(figsize=(16, 9), facecolor='w', edgecolor=None)
    gs = gridspec.GridSpec(2, 1, hspace=0.01, left=0.1, right=0.94)

    # Defining barwidth
    barwidth = 1. / (len(pseudo_family_set) + 1)
    offset = [
        -0.5 + (0.5 + n) * barwidth for n in range(len(pseudo_family_set))
    ]
    # Axing labels with units:
    yaxis = ("Smearing energy [{}]".format(smearing_unit_set.pop()),
             "Total magnetization [{}]".format(magnetization_unit_set.pop()))
    # If more than one unit was specified, I will exit:
    if smearing_unit_set:
        raise ValueError('Found different units for smearing')
    if magnetization_unit_set:
        raise ValueError('Found different units for magnetization')

    # Making two plots, the top one for the smearing, the bottom one for the magnetization
    for index in range(2):
        ax = fig.add_subplot(gs[index])
        for i, pseudo_family in enumerate(pseudo_family_set):
            X = np.arange(nr_of_results) + offset[i]
            Y = np.array([
                thisres[1][pseudo_family][index] for thisres in sorted_results
            ])
            ax.bar(X,
                   Y,
                   width=0.2,
                   facecolor=colors[i],
                   edgecolor=colors[i],
                   label=pseudo_family)
        ax.set_ylabel(yaxis[index], fontsize=14, labelpad=15 * index + 5)
        ax.set_xlim(-0.5, nr_of_results - 0.5)
        ax.set_xticks(np.arange(nr_of_results))
        if index == 0:
            plt.setp(ax.get_yticklabels()[0], visible=False)
            ax.xaxis.tick_top()
            ax.legend(loc=3, prop={'size': 18})
        else:
            plt.setp(ax.get_yticklabels()[-1], visible=False)
        for i in range(0, nr_of_results, 2):
            ax.axvspan(i - 0.5, i + 0.5, facecolor='y', alpha=0.2)
        ax.set_xticklabels(list(formula_list),
                           rotation=90,
                           size=14,
                           ha='center')
    plt.savefig('demo_query.pdf')


qb = QueryBuilder().append(
    Group,
    filters={
        'label': {
            'like': 'tutorial_%'
        }
    },
    project='label',
    tag='group').append(PwCalculation, tag='calculation',
                        with_group='group').append(
                            StructureData,
                            project=['extras.formula'],
                            tag='structure',
                            with_outgoing='calculation').append(
                                Dict,
                                tag='results',
                                project=[
                                    'attributes.energy_smearing',
                                    'attributes.energy_smearing_units',
                                    'attributes.total_magnetization',
                                    'attributes.total_magnetization_units',
                                ],
                                with_incoming='calculation')

plot_results(qb.all())
