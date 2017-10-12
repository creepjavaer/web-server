#hello-server.py
# create by pumkpin 
#in this file,i will  create a webserver to handle the request deriving from client,in response,it will send a simple html
# the Basehttprequesthandler has  build up scoket and http ,all  what we need to do is parsing  the request as well as
#figuring out what it is asking for and  format the data as html (or generate it dynamically)

from http.server import HTTPServer,BaseHTTPRequestHandler

class requesthandler(BaseHTTPRequestHandler):

	page= ''' \
<html>
<body>
<p> Hello, this my first web server!</p>
</body>
</html>
	'''

	def do_GET(self):

		self.send_response(200)
		self.send_header("Content-Type","text/html")
		self.send_header("Content-Length",str(len(self.page)))
		self.end_headers()
		self.wfile.write(self.page.encode("utf-8"))

if __name__ == '__main__':

	serverAddress=('',8080)
	server=HTTPServer(serverAddress,requesthandler)
	server.serve_forever()
