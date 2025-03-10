n = 37
g = 13
print("public key:", n, g)
print("for sender:")
x = int(input("enter x:"))
print("for receiver:")
y = int(input("enter y:"))
k1 = (g**x) % n
k2 = (g**y) % n

while k1 != k2:
    a=k1
    b=k2
    k2 = (a**y) % n
    k1 = (b**x) % n
same_key = k1
print("same key:", same_key)
