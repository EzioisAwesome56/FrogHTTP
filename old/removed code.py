#this file contains code that was removed from the frogHTTP project

#Extended GET parser
#this was my way around the hard coded max GET lenght of 13 characters. Removed in the 1.2 update because I wrote a better GET parser
print "starting extended GET parser v1"
#send redirect
print 'forcing client to refresh the page'
connection.sendall(freload)
#reload the socket conection
print 'closing current connection'
connection.close()
print 'opening connection'
connection, client_address = sock.accept()
sock.listen(1)
#create the new post var, what we need to parse actions
post = connection.recv(20)
#also make the web browser happy
junk2 = connection.recv(20000000)
print "Extended GET Parser loaded!"
print 'received ', post, 'from client'

#html refresh code
#used with Extended GET parser
#made the browser refresh and resend its GET so the extended parser could read all of it.
#removed in the 1.2 update as I rewrote the GET parser
freload = """<html><head><script>location.reload();</script></head></html>"""

#old GET parser
#the old way I got GETs
#removed in 1.4 because of new GET parser
#basically this limited request lenghts, hence why I made the extended GET parser
data = connection.recv(13)
			#to make the client happy that it sent everything
junk = connection.recv(20000000)