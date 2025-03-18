import random as rd
total = 0

for i in range(1000):
    total += max(rd.randint(1, 6), 3)

print(total/500)