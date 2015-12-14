#encoding:utf-8
from app import Application,BaseRequest
from httpserver import HttpServer


class MainHandler(BaseRequest):
    def get(self,*path_args,**path_kwargs):
    	self.set_cookie('cookie is there')

    	print '----------success----------'
        return self.Response('<h1 style="font-size:140px,font-famlily:position:relative"><a style="font-size:200px">iotshine</a></br>you can see this page </br>means the core code is running successful<h1>')

SERVER_ADDRESS = (HOST,PORT) = ('',8888)
def make_server(server_address,application):

	server = HttpServer(server_address)
	
	server.add_app(application)
	return server
if __name__ == '__main__':
	application = Application( [(r"/", MainHandler),
		(r"/favicon.ico", MainHandler)
		])
	http = make_server(SERVER_ADDRESS,application)
	print'server serving on address :{port}..n'.format(port =str(PORT))
	http.run()
