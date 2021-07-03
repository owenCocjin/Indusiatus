##
## Author:  Owen Cocjin
## Version: 0.1
## Date:    2021.06.24
## Description:    Print the bytes of the output file named "test.ind"
## Notes:
## Updates:
##  - Added error for empty files
##  - Prints packet count
with open("test.ind", 'rb') as f:
	menu=f.read(1)
	if menu==b'':
		print("[|X:printfile:main]: File empty!")
		exit(0)
	lines=0
	while menu!=b'':
		counter=0
		#Get length
		length=int(f.read(2).hex(),16)
		menu=f.read(1)

		print(f"Reading {length} bytes... (0x{hex(lines)[2:]:>04})")
		for b in range(length):
			menu=f.read(1)
			print(f"0x{menu.hex()}", end=' ')
			counter+=1
			if counter%16==0:
				print()
			elif counter%8==0:
				print(' ', end='')
		print('\n')
		lines+=1
		menu=f.read(1)
	print(f"{lines} packets read!")
