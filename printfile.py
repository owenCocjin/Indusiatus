##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2021.06.24
## Description:    Print the bytes of the output file named "test.ind"
with open("test.ind", 'rb') as f:
	menu=f.read(1)
	while menu!=b'':
		counter=0
		#Get length
		length=int(f.read(2).hex(),16)
		menu=f.read(1)

		print(f"Reading {length} bytes...")
		for b in range(length):
			menu=f.read(1)
			print(f"0x{menu.hex()}", end=' ')
			counter+=1
			if counter%16==0:
				print()
			elif counter%8==0:
				print(' ', end='')
		print('\n')
		menu=f.read(1)
