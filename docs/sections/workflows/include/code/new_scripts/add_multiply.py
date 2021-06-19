"""Basic calcfunction-based workflows for demonstration purposes."""
from aiida.engine import calcfunction, workfunction


@calcfunction
def add(x, y):
    return x + y


@calcfunction
def multiply(x, y):
    return x * y


@workfunction
def add_multiply(x, y, z):
    """Add two numbers and multiply it with a third."""
    addition = add(x, y)
    product = multiply(addition, z)
    return product
