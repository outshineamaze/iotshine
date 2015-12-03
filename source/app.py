#coding:utf-8
from httpserver import HttpServer,HttpRequest
import re
import types
class Application(object):
	def __init__(self,handlers):
		self.add_handler(handlers)

	def __call__(self,req):
		self.Request = Request = req
		# self.Request['Method'] = Request.method()
		# self.Request['Path'] = Request.path()
		requestrouter = RequestRouter(self.handlers,self.Request)
		return requestrouter.execute()

	def add_handler(self,host_handler):
		


		#if self.handlers and self.handlers[-1][0].pattern == '.*$':
		#	self.handlers.insert (-1,(re.compile(host_path),handlers ))
		#else :
		#	self.handlers.append((re.compile(host_path),handlers))
		self.handlers =[]
		for spec in host_handler:

			if isinstance(spec, (tuple)):
				print spec
				spec  = URLSpec(*spec)
			self.handlers.append(spec)
			print self.handlers
			if spec.name:
				if spec.name in self.named_handlers:
					print  "Multiple handlers named %s; replacing previous value"%spec.name
				self.named_handlers[spec.name]= spec

	def get_host_handlers(self):
		#hsot  = split_host_and_port(request.get('Host'))[0]
		matches= []
		for pattern ,handlers in self.handlers:
			matches.extend(handlers)
		# for pattern ,handlers in self.handlers:
		# 	if pattern.match(host):
		# 		matches.extend(handlers)

		# # Look for default host if not behind load balancer (for debugging)		
		# if not matches and "X-Real-Ip" not in headers:
		# 	for pattern, handlers in self.handlers:
		# 		if pattern.match(self.default_host):
		# 			matches.extend(handlers)
		return matches or None	



class URLSpec(object):
	def __init__(self,pattern,handler,kwargs={},name= None):
		if not pattern.endswith('$'):
			pattern+='$'
		self.regex = re.compile(pattern)
		assert len(self.regex.groupindex) in (0,self.regex.groups),\
				("groups in url regexes must either be all named or all "
				"positional: %r" % self.regex.pattern)
		if isinstance(handler,str):
			handle = import_object(handler)
		self.handler_class = handler
		self.kwargs = kwargs 
		self.name  = name
		self._path, self._group_count = self._find_groups()

	def __repr__(self):
		return '%s(%r, %s, kwargs=%r, name=%r)' % \
			(self.__class__.__name__, self.regex.pattern,
			 self.handler_class, self.kwargs, self.name)

	def _find_groups(self):
		"""Returns a tuple (reverse string, group count) for a url.

		For example: Given the url pattern /([0-9]{4})/([a-z-]+)/, this method
		would return ('/%s/%s/', 2).
		"""
		pattern = self.regex.pattern
		if pattern.startswith('^'):
			pattern = pattern[1:]
		if pattern.endswith('$'):
			pattern = pattern[:-1]

		if self.regex.groups != pattern.count('('):

			return (None, None)

		pieces = []
		for fragment in pattern.split('('):
			if ')' in fragment:
				paren_loc = fragment.index(')')
				if paren_loc >= 0:
					pieces.append('%s' + fragment[paren_loc + 1:])
			else:
				pieces.append(fragment)

		return (''.join(pieces), self.regex.groups)

class RequestRouter(object):
	def __init__(self,handlers,request):
		self.handlers =handlers
		self.request = request
		self.handler_class = None
		self.handler_kwargs = {}
		self.path_args = []
		self.path_kwargs = {}
		print self.request.path()
		self.find_handler()
	# def set_request(self,request,host_handlers):
	# 	self.request = request
	# 	self.find_handler(host_handlers)
	def find_handler(self):
		#app = self.application
		handlers = self.handlers
		if not handlers:
			self.handlers_class = RedirectHandler
			#self.handler_kwargs  = {}
			return
		for spec in handlers:
			match  = spec.regex.match(self.request.path())
			print self.request.path()
			print match
			if match:
				print spec
				self.handler_class = spec.handler_class
				self.handler_kwargs  = spec.kwargs
				if spec.regex.groups:
					if spec.regex.groupindex:
						self.path_kwargs = dict(
							(str(k), _unquote_or_none(v))
							for (k,v) in match.groupdict().item())
					else:
						self.path_kwargs = [_unquote_or_none(s)
												for s in match.groups()]
				return
	def execute(self):
		
		self.handler = self.handler_class(self.request,**self.handler_kwargs)
		print 'get handler execute ......waiting handler_execute.....'
		return self.handler._excute(*self.path_args,**self.path_kwargs)



class BaseRequest(object):
	Default_Method = ["GET","POST", "DELETE","PUT"]
	def  __init__(self,request,**kwargs):
		super(BaseRequest, self).__init__()
		self.request = request
		self.status_code ='200'
		self.header = []
	def _excute(self,*args,**kwargs):
		print 'steart _execute'
		try:
			print self.request.method
			if self.request.method() not in self.Default_Method:
				raise HttpError(405)
			print '1'
			self.path_args = [self.decode_argument(arg) for arg in args]
			self.path_kwargs = dict((k, self.decode_argument(v, name=k))
										for (k, v) in kwargs.items())
			print '1'
			method = getattr(self,self.request.method().lower())
			print 'get method ...........'
			result = method (*self.path_args,**self.path_kwargs)
			print 'this is result ------.'
			print result
			if result is not None:
				return result
		except Exception as e:
			print 'Exception in handler excute'

	def decode_argument(self, value, name=None):
		try:
			return to_unicode(value)
		except UnicodeDecodeError:
			raise HTTPError(400, "Invalid unicode in %s: %r" %
								(name or "url", value[:40]))
	def set_status_code(self,code):
		self.status_code = code
	def set_header(self,key,value):
		self.header.append((key,value))
	def set_cookie(self,value):
		self.header.append(('Cookie',value))
	def Response(self,result):
		results = (self.status_code,self.header,result)
		return results

class HttpError(Exception):
	def __init__(self,status_code = 500,log_message =None):
		self.status_code = status_code
		self.log_message = log_message
		self.reason = log_message

	def __str__(self):
		message = "HTTP %d: %s" % (
			self.status_code,self.reason)
		return message

def split_host_and_port(netloc):

	match = re.match(r'^(.+):(\d+)$', netloc)
	if match:
		host = match.group(1)
		port = int(match.group(2))
	else:
		host = netloc
		port = None
	return (host, port)

def to_unicode(value):
	if isinstance(value,(unicode,type(None))):
		return value
	if not isinstance(value, bytes):
		raise TypeError(
			"Expected bytes, unicode, or None; got %r" % type(value)
		)
	return value.decode("utf-8")
if __name__ == '__main__':

	http = make_server(SERVER_ADDRESS,application)
	print('server serving on address {address} :{port}..n'.format(*SERVER_ADDRESS))
	http.run()



