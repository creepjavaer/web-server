#server-index-page.py
import sys,os
from http.server import BaseHTTPRequestHandler,HTTPServer

class ServerException(Exception):
	pass

class case_no_file(object):

	def text(self,handler):
		return not os.path.exists(handler.full_path)
	def act(self,hadler):
		raise ServerException("'{0}' not found".format(handler.path))

class case_existing_file(object):

	def  test (self,handler):
		return not os.path.exists(handler.full_path)

	def act(self,handler):
		handler.handle_file(handler.full_path)

class case_directory_index_file(object):

	def index_path(self,handler):
		return os.path.join(handler.full_path,"index.html")

	def test(self,handler):
		return os.path.isdir(handler.full_path)and \
		os.path.isfile(self.index_path(handler))

	def act(self,handler):
		handler.handle_file(self.index_path(handler))


class case_directory_no_index_file(object):
    '''Serve listing for a directory without an index.html page.'''

    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    def test(self, handler):
        return os.path.isdir(handler.full_path) and \
               not os.path.isfile(self.index_path(handler))

    def act(self, handler):
        handler.list_dir(handler.full_path)



class case_always_fail(object):

	def test(self,handler):
		return True

	def act(self,handler):
		raise ServerException ("unknown object '{0}' ".format(handler.path))


class requesthandler (BaseHTTPRequestHandler):

	Cases=[case_no_file(),case_existing_file(),case_directory_index_file(),
	case_directory_no_index_file(),
	case_always_fail()]

	error_page= """\
		<html>
		<body>
		<hl>error accessing {path}</hl>
		<p>{msg}</p>
		</body>
		</html>
		"""

	Listing_Page = '''\
        <html>
        <body>
        <ul>
        {0}
        </ul>
        </body>
        </html>
        '''

	def do_GET(self):

		try:

			self.full_path=os.getcwd()+self.path

			for case in self.Cases:
				if case.test(self):
					case.act(self)
					break
		except Exception as msg:
			self.handle_error(msg)

	def handle_file(self,full_path):
		try:

			with open(full_path,'rb') as reader:
				content=reader.read()
			self.send_content(content)

		except  IOError as msg:
			msg ="'{0}' cannot be read : {1}".format(self.path,msg)

			self.handle_error(msg)
	def handle_error(self,msg):
		content=self.error_page.format(path=self.path,msg=msg)

		self.send_content(content,404)

	def list_dir(self, full_path):
		try:
            entries = os.listdir(full_path)
            bullets = ['<li>{0}</li>'.format(e) for e in entries if not e.startswith('.')]
            page = self.Listing_Page.format('\n'.join(bullets))
            self.send_content(page)
        except OSError as msg:
            msg = "'{0}' cannot be listed: {1}".format(self.path, msg)
            self.handle_error(msg)



	def send_content(self,content,status=200):
		self.send_response(status)
		self.send_header("Content-type","text/html")
		self.send_header("Content-Length",str(len(content)))
		self.end_headers()
		self.wfile.write(content.encode("utf-8"))

if __name__== "__main__":
	serverAddress=('',8080)
	server=HTTPServer(serverAddress,requesthandler)
	server.serve_forever()



