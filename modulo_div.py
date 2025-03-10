import math

def mod_inverse(b, m):
    if math.gcd(b, m) != 1:
        return -1
    return pow(b, m - 2, m)

def mod_divide(a, b, m):
    a %= m
    inv = mod_inverse(b, m)
    if inv == -1:
        print("division not defined")
    else:
        print("Result:", (inv * a) % m)

a = 182841384165841685416854134135
b = 135481653441354138548413384135
m = 5
mod_divide(a, b, m)
