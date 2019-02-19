import socket
port = 3000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', port))
print "waiting on port:", port
while 1:
	data, addr = s.recvfrom(1024)
	print data
