from BigNumber import *
import abm
import text2num
import generate_prime
import mutil
import modulo_inverse

p_digit = 100

p = generate_prime.generatePrime(p_digit, False)
a = 765
alpha = 2
beta = abm.power(alpha, a, p)

print("Khoa cong khai: K' = (p, alpha, beta) = ({}, {}, {})".format(p, alpha, beta))
print("Khoa bi mat K'' = (a) = ({})".format(a))

# Prepare
k = 853
encode = text2num.text2num("NGHIA", 3)
print("Encode: ", encode)

# Encrypt
cypherCode = ()
for code in encode:
    y1 = abm.power(alpha, k, p)
    y2 = mutil.moduloMultiplication(abm.power(beta, k, p), code, p)

    cypherCode = cypherCode + ((y1, y2),)

print("Encrypt: ", cypherCode)

# Decrypt
decode = ()
for (y1, y2) in cypherCode:
    y1a = abm.power(y1, a, p)
    y1a_ = modulo_inverse.modInverse(y1a, p)
    x = mutil.moduloMultiplication(y2, y1a_, p)

    decode = decode + (x,)

print("Decrypt: ", decode)
