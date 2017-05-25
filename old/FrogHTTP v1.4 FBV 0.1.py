#FrogHTTP server version 1.4
#FrogBoard Forum Software v0.1
#copyright 2017 DankMemeitTheFrog

#current features:
#basic HTTP request handing
#Sending of html
#multible pages (via parsing HTTP GETs)
#Unlimited get request lenght
#loading pages from external files (ex .html files)
#simple data storage for forum (uses a directory and a few sub directories)

#Todo:
#write forum software into the basic HTTP server
#make handling images work (not sure if I can)

#import required libs
import socket
import sys
import textwrap

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
html1 = """<html><body>this is page 1<br>
<a href="/forum.py">FrogBoard</a></body></html>"""
notfound = """<html><title>404</title><body><center><h1>404</h1><br>
The requested file was not found on this server</center></body></html>"""

#blog related html code
fmain = """<html><title>FrogBoard v1</title><body><h1>FrogBlog Alpha v0.3</h1><br>
Welcome to FrogBoard! Simple Forum software made with python!<br>
Click <a href="/forum.py?p=list">here</a> to view all posts<br>
Would you like to <a href="/forum.py?p=post">make a post?</a></body></html>"""

fmpost = """<html><title>FrogBlog->Post</title><body><h2>FrogBlog Alpha v0.3 -> new post</h2><br>
<form action="/mpost.py" method="post" id="post">Please enter your post in the box below. Posts can be at most 500 charcters<br>
<textarea name="p" form="post" maxlength="500">Enter post contents here</textarea><br>
<input type="submit" value="Submit"></form>
</body></html>"""

fsave = """<html><body>The post has been saved</body></html>"""

listtop = """<html><title>FrogBlog->list posts</title><body><h1>list of all posts</h1><br>"""
listbottom = """</body></html>"""
newline = """<br>"""
linkstart = """<a href="/viewpost.py?id="""
link1end = """">post id """
linkend = """</a>"""

postnotfound = """<html><title>404</title><body><center><h1>404</h1><br>
The requested post was not found in the database</center></body></html>"""

posttop = """<html><body>"""
postbottom = """</body></html>"""

#make socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#binding HTTP server to port 80
server_address = ('localhost', 80)
print >>sys.stderr, 'Starting up FrogHTTP V1.4 on %s port %s' % server_address
sock.bind(server_address)

#listen for web browser connections
sock.listen(1)

while True:
	# Wait for a connection
	print >>sys.stderr, 'waiting for a connection'
	connection, client_address = sock.accept()
	try:
		print >>sys.stderr, 'connection from', client_address
		while True:
			#accept all the crap the web browser wants to send
			raw = connection.recv(20000000)
			#remove the garbage
			raw2 = raw.split(' HTTP/1.1')[0]
			data = raw2.split('?id=')[0]
			print 'received ', data, 'request from client'
			if data:
				print 'sending basic HTTP 1.1 OK header'
				connection.sendall(head)
				#parse GETs and POSTs
				if data == 'GET /':
					print 'sending var html1'
					connection.send(html1)
					break
				elif data == 'GET /forum.py':
					print 'sending forum homepage'
					connection.sendall(fmain)
					break
				elif data == 'GET /forum.py?p=list':
					#send a basic page
					connection.sendall(listtop)
					#load the file that stores total number of posts
					with open('D:\db\pnumb.db', 'r') as total:
						fileraw = total.read()
						posts = int(fileraw)
						total.close()
					#okay, we have the total amount of posts loaded, math with it until we get to 0
					while posts > 0:
						astring = str(posts)
						listdata = linkstart + astring + link1end + astring + linkend + newline
						connection.sendall(listdata)
						posts = posts - 1
					break
				#post viewer
				elif data == 'GET /viewpost.py':
					postid = raw2.split('?id=')[-1]
					with open('D:\db\pnumb.db', 'r') as total:
						fileraw = total.read()
						posts = int(fileraw)
						rid = int(postid)
					if posts >= rid:
						with open('D:\db\post\post'+postid+'.post') as postraw:
							post = postraw.read()
							postraw.close()
						page = posttop + post + postbottom
						connection.sendall(page)
					else:
						connection.sendall(postnotfound)
					break
				elif data == 'GET /forum.py?p=post':
					#user wants to make a post? okay, send them the post making page
					connection.sendall(fmpost)
					break
				elif data == 'POST /mpost.py':
					#we need the actaul POST data, so we get it from raw
					postraw = raw.split('p=')[-1]
					post = postraw.replace('+', ' ').replace('%0D%0A', '<br>')
					#figure out the next unused post id
					with open('D:\db\pnumb.db', 'r+') as getid:
						print "finding next unused post id..."
						idraw = getid.read()
						id = int(idraw) + 1
						saveid = str(id)
						getid.close()
					#erase file
					open('D:\db\pnumb.db', 'w').close()
					#reopen file and save id
					with open('D:\db\pnumb.db', 'r+') as idfile:
						idfile.write(saveid)
						idfile.close()
					with open('D:\db\post\post'+saveid+'.post', 'w') as savepost:
						print 'saving post...'
						savepost.write(post)
						print 'post saved!'
						savepost.close()
					connection.sendall(fsave)
					break
				else:
					print 'client requested a page that doesnt exist'
					print 'sending 404 page instead'
					connection.sendall(notfound)
					break
			else:
				print >>sys.stderr, 'no more data from', client_address
				break
            
	finally:
		# Clean up the connection
		connection.close()
