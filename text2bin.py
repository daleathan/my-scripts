#!/usr/bin/python3

def fillZeros(seq) :
    while len(seq) < 8 :
        seq = "0" + seq
    return seq

mystr = input("Enter text: ")
output = []

for x in mystr :
    num = ord(x)
    seq = fillZeros(bin(num)[2:])
    output.append(seq)

print(''.join(output))
