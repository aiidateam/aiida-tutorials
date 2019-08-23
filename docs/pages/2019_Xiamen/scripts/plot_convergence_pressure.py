# -*- coding: utf-8 -*-
"""Plot parabola using matplotlib."""
from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
from aiida.orm import load_node


def parabola(x, a, b, c):
    """Parabola."""
    return a * x**2 + b * x + c


def show_parabola_results(pk):  # pylint: disable=too-many-locals
    """Plot (and show) parabola using matplotlib."""
    out_p = load_node(pk).outputs.steps.get_dict()

    step0 = out_p['step0']
    steps = out_p['steps']

    import numpy as np
    import pylab as pl

    data = []
    data.append((step0['V'], step0['E']))
    for step in steps:
        data.append((step['V'], step['E']))

    data = np.array(data)
    min_V = data[:, 0].min()
    max_V = data[:, 0].max()

    min_E = data[:, 1].min()
    max_E = data[:, 1].max()

    min_V -= 10.
    max_V += 10.
    min_E -= 0.1
    max_E += 0.5

    V_range = np.linspace(min_V, max_V, 500)

    for subplot in range(2):
        pl.subplot(1, 2, 1 + subplot)

        pl.plot(data[:1, 0], data[:1, 1], 'o', color='red')
        pl.annotate('0', xy=(data[0, 0], data[0, 1]))

        pl.plot(data[1:, 0], data[1:, 1], 'o', color='blue')

        color = 0.8
        for idx, step in enumerate(steps, start=1):
            pl.plot(V_range,
                    parabola(V_range, step['a'], step['b'], step['c']),
                    color=(color, color, color))
            parabola_Vmin = -step['b'] / 2. / step['a']
            parabola_Emin = parabola(parabola_Vmin, step['a'], step['b'],
                                     step['c'])
            pl.plot([parabola_Vmin], [parabola_Emin],
                    'x',
                    color=(color, color, color))
            pl.annotate(str(idx), xy=(step['V'], step['E']))
            pl.axvline(step['V'], color=(1., 0.7, 1.), linestyle='--')
            color -= 0.25
            if color <= 0.:
                color = 0.

        pl.axis([min_V, max_V, min_E, max_E])
        if subplot == 1:
            # some zoom
            pl.xlim((41.5, 44.))
            pl.ylim((-259.47, -259.45))
        pl.xlabel('Volume (ang^3)')
        pl.ylabel('Energy (eV)')

    pl.show()


if __name__ == '__main__':
    import sys
    try:
        pk_value = int(sys.argv[1])
    except (IndexError, ValueError):
        print(
            'Pass as parameter the PK of the WorkChain calculating the pressure',
            file=sys.stderr)
        print('convergence to generate the plot.', file=sys.stderr)
        sys.exit(1)
    show_parabola_results(pk_value)
