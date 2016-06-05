#!/usr/bin/python3

mystr = input("Enter binary string: ")
output = []

while len(mystr)%8 != 0 : mystr = '0' + mystr

c = 0
while c <= len(mystr)-8 :
    output.append(chr(int(mystr[c:c+8], 2)))
    c+=8

print(''.join(output))
