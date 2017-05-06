#FrogHTTP server version 1
#copyright 2017 DankMemeitTheFrog

#current features:
#basic HTTP request handing
#Sending of html
#multible pages (via parsing HTTP GETs)
#loading pages from external files (ex .html files)
#Todo:
#parse some form of POST (maybe using GET?)
#write forum software into the basic HTTP server
#make handling images work (not sure if I can)
#write database storage code for forum software

#import required libs
import socket
import sys

#load any external pages
with open('C:\users\mynamexd\Desktop\page3.html', 'r') as file1:
	html3 = file1.read().replace('\n', '')
	file1.close()
	
#HTTP response headers, required before you send anything
head = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Connection: close

"""

#web pages that you want to store as vars
html1 = """<html><body>
this is page 1 <a href="page2.py">page 2</a></body></html>"""
html2 = """<html><body>this is page 2 <a href="/">page 1</a></body></html>"""

#make socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#binding HTTP server to port 80
server_address = ('localhost', 80)
print >>sys.stderr, 'Starting up FrogHTTP V1 on %s port %s' % server_address
sock.bind(server_address)

#listen for web browser connections
sock.listen(1)

while True:
	# Wait for a connection
	print >>sys.stderr, 'waiting for a connection'
	connection, client_address = sock.accept()
	try:
		print >>sys.stderr, 'connection from', client_address

		# Receive whatever the heck is sent, usually boring web browser crap
		while True:
			data = connection.recv(13)
			#to make the client happy that it sent everything
			junk = connection.recv(20000000)
			print 'received ', data, 'request from client'
			if data:
				print 'sending basic HTTP 1.1 OK header'
				connection.sendall(head)
				#parse the GET, if there is one
				if data == 'GET /page2.py':
					print 'sending var html2'
					connection.sendall(html2)
					break
				elif data == 'GET /page3.py':
					print 'sending var html3'
					connection.sendall(html3)
					break
				else:
					print 'sending var html1'
					connection.sendall(html1)
					break
			else:
				print >>sys.stderr, 'no more data from', client_address
				break
            
	finally:
		# Clean up the connection
		connection.close()