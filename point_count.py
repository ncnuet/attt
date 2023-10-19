# Counts the number of points on an elliptic curve over Z/p.

import random
from modmath import is_square_mod_p, mod_sqrt, mod_div


def get_random_point(p, a, b):
    # pick a random x value until one is found on the curve
    while True:
        x = random.randint(0, p-1)
        y_squared = (pow(x, 3, p) + ((a*x) % p) + (b % p)) % p
        if is_square_mod_p(y_squared, p):
            break

    y = mod_sqrt(y_squared, p)

    return (x, y)


def add_points(p, q, a, pr):
    if p == "inf":
        return q

    if q == "inf":
        return p

    if p == negate_point(q, pr):
        return "inf"

    # calculate slope (see http://www.mat.uniroma2.it/~schoof/ctg.pdf pg 222)
    if p == q:
        m = mod_div((3 * pow(p[0], 2, pr) + a) % pr, (2 * p[1]) % pr, pr)
    else:
        m = mod_div((q[1] - p[1]) % pr, (q[0] - p[0]) % pr, pr)

    x = (-p[0] - q[0]) % pr + pow(m, 2, pr)
    y = m * (p[0] - x) - p[1]

    return (x % pr, y % pr)


def negate_point(pt, p):
    if pt == 'inf':
        return 'inf'

    return (pt[0], -pt[1] % p)


def bsgs(p, a, b):
    P = get_random_point(p, a, b)

    # compute the values m in interval of possible #E(F_p) such that mP = 0
    # by taking baby steps then giant steps
    ms = set()

    # baby steps: calculate the first p^(-4) multiples of P
    # (stored in a dictionary for fastest lookup, with the index saved)
    baby_steps = {'inf': 0}
    s = int(p**(1/4))
    next_multiple = 'inf'

    for i in range(1, s+1):
        next_multiple = add_points(next_multiple, P, a, p)
        baby_steps[next_multiple] = i
        baby_steps[negate_point(next_multiple, p)] = -i

    # the final value of next_multiple is sP
    two_sP = add_points(next_multiple, next_multiple, a, p)
    Q = add_points(two_sP, P, a, p)  # Q = (2s + 1)P

    # compute R = (p+1)P by using the binary expansion of p+1
    bin_str = bin(p+1)[2:]
    R = 'inf'
    doubled = P
    for bit in reversed(bin_str):
        if bit == '1':
            R = add_points(R, doubled, a, p)
        doubled = add_points(doubled, doubled, a, p)

    # giant steps: compute R, R+/-Q, R+/-2Q,..., R+/-tQ to find i,j
    # such that R + iQ = jP (Theorem 2.1 in Schoof guarantees this happens)

    # num giant steps--approx p^(1/4)
    t = int(round((2 * p**(1/2)) / (2*s + 1)))

    next_Q_multiple = 'inf'

    for i in range(t+1):
        iQ = next_Q_multiple
        R_plus_iQ = add_points(R, iQ, a, p)
        if R_plus_iQ in baby_steps:  # then R + iQ = jP
            j = baby_steps[R_plus_iQ]
            m = p + 1 + (2*s+1)*i - j  # R + iQ - jP = mP = 0
            ms.add(m)

        R_minus_iQ = add_points(R, negate_point(iQ, p), a, p)
        if R_minus_iQ in baby_steps:  # then R - iQ = jP
            j = baby_steps[R_minus_iQ]
            # R-iQ-jP = (p+1)P-i(2s+1)P-jP = mP = 0
            m = p + 1 + (2*s+1)*(-i) - j
            ms.add(m)

        next_Q_multiple = add_points(next_Q_multiple, Q, a, p)

    if len(ms) == 1:
        return ms.pop()
    else:
        return -1  # failure


def count_points(p, a, b):
    num_points = bsgs(p, a, b)
    twisted = False

    # find a non-square g
    for n in range(p):
        if not is_square_mod_p(n, p):
            g = n
            break

    while num_points == -1:  # bsgs failed; try Mestre's algorithm
        # alternate between trying BSGS on E and on E's quadratic twist
        twisted = not twisted

        if twisted:
            # count #E'(F_p): E' is the quadratic twist Y^2 = X^3 + Ag^2X + Bg^3
            twist_points = bsgs(p, (a * pow(g, 2, p)) %
                                p, (b * pow(g, 3, p)) % p)

            if twist_points != -1:
                num_points = 2*(p+1) - twist_points  # E'(F_p)+#E(F_p) = 2(p+1)

        else:
            num_points = bsgs(p, a, b)

    return num_points
