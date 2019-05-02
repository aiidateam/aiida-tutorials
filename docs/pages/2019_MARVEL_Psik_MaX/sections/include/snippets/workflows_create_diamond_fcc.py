
def create_diamond_fcc(element):
    """Calculation function to create the crystal structure of a given element.

    For simplicity, only Si and Ge are valid elements.

    :param element: The element to create the structure with.
    :return: The structure.
    """
    from aiida import orm

    import numpy as np
    elem_alat = {
        'Si': 5.431,  # Angstrom
        'Ge': 5.658,  # Angstrom
    }

    # Validate input element
    try:
        symbol = element.value
    except AttributeError:
        symbol = str(element)

    if symbol not in elem_alat:
        raise ValueError('Valid elements are only Si and Ge')

    # Create cell starting having lattice parameter alat corresponding to the element
    alat = elem_alat[symbol]
    cell = np.array([[0., 0.5, 0.5],
                    [0.5, 0., 0.5],
                    [0.5, 0.5, 0.]]) * alat

    # Create a structure data object
    structure = orm.StructureData(cell=cell)
    structure.append_atom(position=(0., 0., 0.), symbols=symbol)
    structure.append_atom(position=(0.25 * alat, 0.25 * alat, 0.25 * alat), symbols=symbol)

    return structure
