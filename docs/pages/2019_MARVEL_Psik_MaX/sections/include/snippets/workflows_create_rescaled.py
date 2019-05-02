from aiida.engine import workfunction


@workfunction
def create_rescaled(element, scale):
    """Workfunction to create and immediately rescale a crystal structure of a given element."""
    structure = create_diamond_fcc(element)
    rescaled = rescale(structure, scale)

    return rescaled
