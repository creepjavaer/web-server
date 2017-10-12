#response-server.py
from http.server import HTTPServer,BaseHTTPRequestHandler

class requesthandler(BaseHTTPRequestHandler):

	page= '''\
<html>
<tittle>
"hello response"
</tittle>
<body>
<table>
<tr>  <td>Header</td>         <td>Value</td>          </tr>
<tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
<tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
<tr>  <td>Client port</td>    <td>{client_port}s</td> </tr>
<tr>  <td>Command</td>        <td>{command}</td>      </tr>
<tr>  <td>Path</td>           <td>{path}</td>         </tr>
</table>
</body>
</html>
'''
	
	def do_GET(self):
		content=self.create()
		self.send_content(content)

	def create(self):
		values = {
		    'date_time'   : self.date_time_string(),
		    'client_host' : self.client_address[0],
		    'client_port' : self.client_address[1],
		    'command'     : self.command,
		    'path'        : self.path
		}

		content=self.page.format(**values)
		return content 

	def send_content(self,content):
		self.send_response(200)
		self.send_header("Content-type","text/html")
		self.send_header("Content-Length",str(len(content)))
		self.end_headers()
		self.wfile.write(content.encode("utf-8"))

if __name__ =="__main__":

	serverAddress=('',8080)
	server=HTTPServer(serverAddress,requesthandler)
	server.serve_forever()



