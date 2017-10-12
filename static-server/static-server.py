#static-server.py

import os ,sys
from http.server import HTTPServer,BaseHTTPRequestHandler

class ServerException():
 	'''for report server exception'''
 	pass
 	#print("connect exception")

class requesthandler(BaseHTTPRequestHandler):
	err_page= """\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
        """
	def do_GET(self):
		#full_path=os.getcwd()+self.path
		try:
			full_path=os.getcwd()+self.path

			if(not os.path.exists(full_path)):
				raise ServerException("'{0}' not found".format(self.path))
			elif(os.path.isfile(full_path)):
				#print(full_path)
				print("****")
				print(full_path)

				self.handle_file(full_path)
			else:
				raise ServerException("Unknown object '{0}'".format(self.path))
		except Exception as msg:
			self.handle_error(msg)
			print("#######")
			print(full_path)

	def handle_file(self,full_path):
		#print(full_path)
		try:
			with open (full_path,'rb') as reader:
				content=reader.read()
			self.send_content(content)
		except IOError as msg:
			msg = "'{0}' cannot be read: {1}".format(self.path, msg)
			self.handle_error(msg)
			

	def send_content(self,content,status=200):
		self.send_response(status)
		self.send_header("Content-type", "text/html")
		self.send_header("Content-Length",str(len(content)))
		self.end_headers()
		self.wfile.write(content.encode("utf-8"))

        


	def handle_error(self,msg):
		#print()
		content=self.err_page.format(path=self.path,msg=msg)

		self.send_content(content,404)
    	

if __name__ =="__main__":
	serverAddress=("",8080)
	server=HTTPServer(serverAddress,requesthandler)
	server.serve_forever()





