import generate_prime
import modulo_inverse
import text2num
import abm

from BigNumber import *

num_bits = 256
# num_digits_e = 150  # ~36 digits
# num_digits_e = 332  # ~100 digits
num_digits_e = 512  # ~154 digits

p = generate_prime.generatePrime(num_bits)
q = generate_prime.generatePrime(num_bits)
e = generate_prime.generatePrime(num_digits_e)

n = p * q
phi = (q - 1) * (p - 1)
d = modulo_inverse.modInverse(e, phi)

# print(n, p, q, e, phi)

print("Khoa cong khai: K' = (n, e) = ({}, {})".format(n, e))
print("Khoa bi mat K'' = (d) = ({})".format(d))

# Prepare
encode = text2num.text2num("NGHIA", 3)
print("Encode: ", encode)

# Encrypt
cypherCode = ()
for code in encode:
    cypherCode = cypherCode + (abm.power(code, e, n),)

print("Encrypt: ", cypherCode)

# Decrypt
decode = ()
for code in cypherCode:
    # decode = decode + (abm.abm(code, d, n),)
    # Native python module
    decode = decode + (abm.power(code, d, n),)

print("Decrypt: ", decode)
