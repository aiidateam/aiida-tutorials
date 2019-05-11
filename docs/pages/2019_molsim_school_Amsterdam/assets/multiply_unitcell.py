def multiply_unit_cell(cif, cutoff):
    """Returns the multiplication factors (tuple of 3 int) for the cell vectors
    that are needed to respect: min(perpendicular_width) > threshold
    """
    from math import cos, sin, sqrt, pi
    import numpy as np
    deg2rad = pi / 180.

    struct = six.itervalues(cif.values.dictionary)

    a = float(struct['_cell_length_a'])
    b = float(struct['_cell_length_b'])
    c = float(struct['_cell_length_c'])

    alpha = float(struct['_cell_angle_alpha']) * deg2rad
    beta = float(struct['_cell_angle_beta']) * deg2rad
    gamma = float(struct['_cell_angle_gamma']) * deg2rad

    # first step is computing cell parameters according to  https://en.wikipedia.org/wiki/Fractional_coordinates
    # Note: this is the algorithm implemented in Raspa (framework.c/UnitCellBox). 
    # There also is a simpler one but it is less robust.
    v = sqrt(1 - cos(alpha)**2 - cos(beta)**2 - cos(gamma)**2 +
             2 * cos(alpha) * cos(beta) * cos(gamma))
    cell = np.zeros((3, 3))
    cell[0, :] = [a, 0, 0]
    cell[1, :] = [b * cos(gamma), b * sin(gamma), 0]
    cell[2, :] = [
        c * cos(beta),
        c * (cos(alpha) - cos(beta) * cos(gamma)) / (sin(gamma)),
        c * v / sin(gamma)
    ]
    cell = np.array(cell)

    # diagonalizing the cell matrix: note that the diagonal elements are the perpendicolar widths because ay=az=bz=0
    diag = np.diag(cell)
    return tuple(int(i) for i in np.ceil(cutoff / diag * 2.))
