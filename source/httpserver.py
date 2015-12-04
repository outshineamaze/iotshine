#coding:utf-8
import sys
import socket 
import platform
import time
from loop import SelectLoop, EPollLoop
class HttpRequest(object):
	def __init__(self,header,body):
		(self.request_method,
			self.request_path,self.request_version)=header.splitlines()[0].rstrip('rn').split()
		self.header = header
		self.body =body
		self.header_map= {}
		try:
			for lines in self.header.splitlines():
				print lines
				if lines.find(":")!=-1:
					index  = lines.index(':')
					(key,value) = lines[:index],lines[index:]
					self.header_map[key] = value
		except:
			print 'faile generator header map'
			pass
	def method(self):
		return self.request_method
	def path(self):
		return self.request_path
	def version(self):
		return self.request_version
	def body(self):
		return self.body
	def header(self):
		return self.header
	def get(self,name):
		if self.header_map[name]:
			return self.header_map[name]

class HttpServer(object):
	"""strt httpserver"""
	def __init__(self, (host,port),timeout =10,request_size=10):
		self.clients = 0
		self.clientmap={}
		self.outputs = []
		self.timeout = timeout
		SEND_BUF_SIZE = 4096
		RECV_BUF_SIZE = 1024
		self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		#print 'defailt timeout is :%s'%self.server.gettimeout()
		#self.server.settimeout(2)
		#print "Current socket timeout: %s" %self.server.gettimeout()
		#bufsize = self.server.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
		#print "Buffer size [Before]:%d" %bufsize

		self.server.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
		#new_state = self.server.getsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR )
		#print "New sock state: %s" %new_state

		self.server.bind((host,port))
		self.server.listen(request_size)
	def add_app(self,application):
		self.application = application
	def start_response(self,status,response_headers,exc_info = None):
		self.header_set = (status,response_headers)
	def finish_response(self,result):
		try:

			status,response_headers =self.header_set
			print response_headers
			response ='HTTP1.1/ {status}\r\n'.format(status = status)
			if response_headers != []:
				for header in response_headers:
					response += '{0}: {1}\r\n'.format(*header)
			else:response+='\r\n'
			response +='\r\n'			
			response += result
			return response
		except:
			print '*****error in finish_response****** '
			return 'error  in finish_response'

	def parse_request(self,text):
		try:
			(header,body) = text.split('\r\n\r\n')
		except:
			header =text
			body =''
		return HttpRequest(header,body)

	def handle_one_request(self,data):

		print (''.join(
			'{line}'.format(line= line)
			for line in data.splitlines()
			))

		result = self.application(self.parse_request(data))
		print 'there is result ....'
		print result
		self.start_response(result[0],result[1])
		return  self.finish_response(result[2])

	def run(self):
		print '>>>>>>>>>>>>>start run server <<<<<<<<<<<<<<<'
		try:
			sysstr = platform.system()
		except:
			sysstr = "Other System"
		if sysstr== "Windows":
			print 'using SelectLoop on Windows'

			loop = SelectLoop(self.server,self.timeout,self.handle_one_request)
			loop.start()
		elif sysstr=="Linux":
			print 'using EPollLoop on Linux'
			loop =  EPollLoop(self.server,self.timeout,self.handle_one_request)
			loop.start()
		
#if __name__ == '__main__':
	# re = 'get jfls jflskajf\r\nfshflsj:hfkashhkhks\r\njfasjlkfhkls'
	# BADY='HSDLFSAHGSLAJDGSJ'
	# request = HttpRequest(re,BADY)
	# print request.get('fshflsj')
	# print request.get_request_path()
	# print request.get_body()

