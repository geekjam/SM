import sys
import os
import time

def Rc4File(inputfilename, outfilename, key):
	file_object = open(inputfilename)
	try:
		byte_data = file_object.read()
		byte_data = [ord(i) for i in byte_data]
	finally:
  		file_object.close()
		
	file_object = open(outfilename, 'wb')
	byte_write = byte_data[:]
	keyLength = len(key)
	key = [ord(i) for i in key]
	i = 0
	j = 0
	k = []
	tmp = 0
	s = [ i for i in range(256)]
	k = [ key[i % keyLength] for i in range(256)]
	for i in range(256):
  		j = (j + s[i] + k[i]) % 256
  		tmp = s[i]
  		s[i] = s[j]
  		s[j] = tmp

	x = 0
	y = 0
	t = 0
	i = 0
	tmp = 0
	dataLength = len(byte_data)

	while i < dataLength:
  		x = (x + 1) % 256
  		y = (y + s[x]) % 256
  		tmp = s[x]
  		s[x] = s[y]
  		s[y] = tmp
  		t = (s[x] + s[y])%256
  		byte_data[i] = byte_data[i] ^ s[t]
  		i += 1

	out_bytes = ''
	i = 0

	while i < dataLength:
  		out_bytes+=chr(byte_data[i])
  		i += 1
 
 
	try:
  		file_object.write(out_bytes)
	finally:
  		file_object.close()

def Init():
	pass
