#!/usr/bin/python3

import os

mystr = input("Enter binary string: ")
output = []

for x in mystr :
    if x != '0' and x != '1' :
        print("Invalid binary string.")
        os._exit(0)

while len(mystr)%8 != 0 : mystr = '0' + mystr

c = 0
while c <= len(mystr)-8 :
    output.append(chr(int(mystr[c:c+8], 2)))
    c+=8

print(''.join(output))
