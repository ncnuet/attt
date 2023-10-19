from BigNumber import *


def MOD(num, mod):
    res = 0

    for i in range(len(num)):
        res = (res * 10 + int(num[i])) % (mod - 1)
    return res


def ModExponent(a, b, m):
    if (a == 0):
        return 0
    elif (b == 0):
        return 1
    elif (b % 2):
        result = a % m
        result = result * ModExponent(a, b - 1, m)

    else:
        result = ModExponent(a, b // 2, m)
        result = ((result % m) * (result % m)) % m

    return (result % m + m) % m

# a^b % m

# Method 1
def abm(a, b, m):
    a = a % m
    b = b % m

    return ModExponent(a, b, m)

# Method 2
def power(a, b, m):
    res = 1     # Initialize result

    # Update x if it is more
    # than or equal to p
    a = a % m

    if (a == 0):
        return 0

    while (b > 0):

        # If y is odd, multiply
        # x with result
        if ((b & 1) == 1):
            res = (res * a) % m

        # y must be even now
        b = b >> 1      # y = y/2
        a = (a * a) % m

    return res
