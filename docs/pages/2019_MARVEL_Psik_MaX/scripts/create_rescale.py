# -*- coding: utf-8 -*-
from aiida.engine import calcfunction


@calcfunction
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
    symbol = element.value

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


@calcfunction
def rescale(structure, scale):
    """Calculation function to rescale a structure

    :param structure: An AiiDA structure to rescale
    :param scale: The scale factor (for the lattice constant)
    :return: The rescaled structure
    """
    from aiida import orm

    ase = structure.get_ase()
    ase.set_cell(ase.get_cell() * float(scale), scale_atoms=True)

    return orm.StructureData(ase=ase)
