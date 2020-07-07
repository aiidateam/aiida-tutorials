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
