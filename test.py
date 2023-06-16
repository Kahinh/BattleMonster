from copy import deepcopy

class MaClass:
    def __init__(self, var):
        self.var = var

a = MaClass(1)
b = MaClass(2)
c = MaClass(3)
d = MaClass(4)

maliste1 = [a, b, c]

maliste2 = [cObject for cObject in maliste1]



print("var : ", maliste1[0].var)
print("len : ", len(maliste1))
maliste2.append(d)
maliste2[0].var = 2
print("var : ", maliste1[0].var)
print("len : ", len(maliste1))