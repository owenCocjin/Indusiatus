from indusiatus import main
try:
	main()
except KeyboardInterrupt:
	print('\r\033[K', end='')
