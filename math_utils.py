import math
from collections import defaultdict
from sympy import primerange

def lcm_from_array(arr):
    prime_factors = defaultdict(int)
    lcm = 1
    max_val = int(math.sqrt(max(arr))) + 1
    primes = list(primerange(1, max_val))
    for j in arr:
        num = j
        for i in primes:
            if i*i > num:
                break
            exp = 0
            while num % i == 0:
                num //= i
                exp += 1
            if exp > prime_factors[i]:
                prime_factors[i] = exp
        if num > 1:
            if prime_factors[num] < 1:
                prime_factors[num] = 1
    for prime, factor in prime_factors.items():
        lcm *= prime ** factor
    return lcm