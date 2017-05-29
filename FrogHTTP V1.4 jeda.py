#FrogHTTP server version 1.4
#This version has all frogboard code removed
#copyright 2017 DankMemeitTheFrog

#import required libs
import socket
import sys
import textwrap
import thread

#functions


#load any external pages
#with open('aaaaaaa\page3.html', 'r') as file1:
#	html3 = file1.read().replace('\n', '')
#	file1.close()
	
#HTTP response headers, required before you send anything
head = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Connection: close

"""


#web pages that you want to store as vars
html1 = """<html><body>this is page 1</body></html>"""
notfound = """<html><title>404</title><body><center><h1>404</h1><br>
The requested file was not found on this server</center></body></html>"""


#create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#binding HTTP server to port 80
server_address = ('localhost', 80)
print >>sys.stderr, 'Starting up FrogHTTP V1.4 on %s port %s' % server_address
sock.bind(server_address)

#listen for web browser connections
sock.listen(1)

def handleconn(conn, addr):
	try:
		while True:
			#accept all the crap the web browser wants to send
			raw = conn.recv(20000000)
			#remove the garbage
			raw2 = raw.split(' HTTP/1.1')[0]
			data = raw2.split('?id=')[0]
			print 'received ', data, 'request from client'
			if data:
				print 'sending basic HTTP 1.1 OK header'
				conn.sendall(head)
				#parse GETs and POSTs
				if data == 'GET /':
					print 'sending var html1'
					conn.send(html1)
					break
				else:
					print 'client requested a page that doesnt exist'
					print 'sending 404 page instead'
					conn.sendall(notfound)
					break
			else:
				print >>sys.stderr, 'no more data from', addr
				break
	finally:
		try:
			conn.close()
		except: # already closed?
			pass

def main():
	while True:
		# Wait for a connection
		print >>sys.stderr, 'waiting for another connection'
		connection, client_address = sock.accept()
		print >>sys.stderr, 'connection from', client_address
      	      	thread.start_new_thread(handleconn, (connection, client_address))
	sock.close()

if __name__ == "__main__":
	main()
