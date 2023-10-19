# modulo multiplication

from BigNumber import *

# Returns (a * b) % mod


def moduloMultiplication(a, b, mod):

    res = 0  # Initialize result

    # Update a if it is more than
    # or equal to mod
    a = a % mod

    while (b):

        # If b is odd, add a with result
        if (b & 1):
            res = (res + a) % mod

        # Here we assume that doing 2*a
        # doesn't cause overflow
        a = (2 * a) % mod

        b = b // 2  # b = b / 2

    return res
