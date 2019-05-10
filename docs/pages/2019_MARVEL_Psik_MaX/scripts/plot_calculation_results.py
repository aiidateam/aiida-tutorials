# -*- coding: utf-8 -*-
import sys
import numpy as np
from argparse import ArgumentParser
from matplotlib import gridspec, pyplot as plt


def plot_results(inputfname, outputfname=None, plotformat=None):
    """
    :param inputfile: the filename of the inputfile
    :param (opt) outputfile:
        The (optional) name for the outputfile.
    :param (opt) format:
        The (optional) file format, if not clear from the input file name

    Reads the input file provided by the user.
    The format should be comma separated values:
    formula, pseudo_family, smearing, smearing_units, magnetization, magnetization_units


    This order has to be respected!

    If an outputfile is provided, use matplotlib.pyplot.savefig to save the figure
    Else, calls matplotlib.pyplot.show to show in screen
    """

    # Reading the input file given to me:
    with open(inputfname) as f:
        lines = f.readlines()

    # Definining the variables I need to read the units and pseudo families
    smearing_unit_set = set()
    magnetization_unit_set = set()
    pseudo_family_set = set()

    # Storing results:
    results_dict = {}

    # Looping through results:
    for line in lines:
        try:
            (
                formula, pseudo_family, smearing,
                smearing_units, magnetization, magnetization_units
            ) = [i.strip() for i in line.split(',')]
            smearing, magnetization = map(float, (smearing, magnetization))
        except Exception as e:
            print(
                "There was an {} reading line:\n"
                "{}"
                "Exception: {}\n"
                "Skipping this line\n".format(type(e), line, e))
            continue

        # If this is a new formula, not present in results,
        # Creating the key-value pair:
        if formula not in results_dict:
            results_dict[formula] = {}

        # Storing the results:
        results_dict[formula][pseudo_family] = (smearing, magnetization)

        # Adding to the unit set:
        smearing_unit_set.add(smearing_units)
        magnetization_unit_set.add(magnetization_units)
        pseudo_family_set.add(pseudo_family)

    # Sorting by formula:
    sorted_results = sorted(results_dict.items())
    formula_list = zip(*sorted_results)[0]
    nr_of_results = len(formula_list)

    # Checks that I have not more than 3 pseudo families.
    # If more are needed, define more colors

    pseudo_list = list(pseudo_family_set)
    if len(pseudo_list) > 3:
        raise Exception('I was expecting 3 or less pseudo families')

    colors = ['b', 'r', 'g']

    # Plotting:
    gs = gridspec.GridSpec(2, 1, hspace=0.01, left=0.1, right=0.94)
    fig = plt.figure(figsize=(16, 9), facecolor='w', edgecolor=None)

    # Defining barwidth
    barwidth = 1. / (len(pseudo_list) + 1)
    offset = [-0.5 + (0.5 + n) * barwidth for n in range(len(pseudo_list))]

    # Axing labels with units:
    yaxis = (
        "Smearing energy [{}]".format(smearing_unit_set.pop()),
        "Total magnetization [{}]".format(magnetization_unit_set.pop())
    )
    # If more than one unit was specified, I will exit:
    if smearing_unit_set:
        raise Exception('Found different units for smearing')
    if magnetization_unit_set:
        raise Exception('Found different units for magnetization')

    # Making two plots, one for the smearing, the lower for magnetization
    for index in range(2):
        ax = fig.add_subplot(gs[index])
        for i, pseudo_family in enumerate(pseudo_list):
            X = np.arange(nr_of_results) + offset[i]
            Y = np.array([
                thisres[1][pseudo_family][index]
                for thisres
                in sorted_results
            ])

            ax.bar(
                X, Y, width=0.2, facecolor=colors[i], edgecolor=colors[i],
                label=pseudo_family
            )
        ax.set_ylabel(yaxis[index], fontsize=14, labelpad=15 * index + 5)
        ax.set_xlim(-0.5, nr_of_results - 0.5)
        ax.set_xticks(np.arange(nr_of_results))
        if index:
            plt.setp(ax.get_yticklabels()[-1], visible=False)
        else:
            plt.setp(ax.get_yticklabels()[0], visible=False)
            ax.xaxis.tick_top()
            ax.legend(loc=3, prop={'size': 18})
        for i in range(0, nr_of_results, 2):
            ax.axvspan(i - 0.5, i + 0.5, facecolor='y', alpha=0.2)
        ax.set_xticklabels(list(formula_list), rotation=90, size=14, ha='center')
    if outputfname is not None:
        plt.savefig(outputfname, format=plotformat)
    else:
        plt.show()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('inputfile', help='The input file with the data to plot')
    parser.add_argument('-o', '--outputfile', help='The outputfile to plot results to', default=None)
    parser.add_argument('-f', '--format', default=None,
        help='The format to plot, if outputfile is specified and no valid extension is provided')
    parsed_args = parser.parse_args(sys.argv[1:])
    plot_results(
        inputfname=parsed_args.inputfile,
        outputfname=parsed_args.outputfile,
        plotformat=parsed_args.format
    )
