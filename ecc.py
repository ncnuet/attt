import generate_prime
import point_count
import time

start_time = time.time()

num_bits_p = 47  # max now is 47 -> time 30s

p = generate_prime.generatePrime(num_bits_p)
a = generate_prime.generatePrime(5)
b = generate_prime.generatePrime(5)

num_point = 1
num_point_is_prime = False

while (not num_point_is_prime):
    a += 1
    num_point = point_count.count_points(p, a, b)
    if generate_prime.checkLowLevelPrime(num_point):
        if generate_prime.isMillerRabinPassed(num_point):
            num_point_is_prime = True

end_time = time.time()
elapsed_time = end_time - start_time

print("(a, b, p) = ({}, {}, {})".format(a, b, p))
print(num_point)
print("Elapsed time: ", elapsed_time

) 

print(p)