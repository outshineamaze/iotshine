#coding:utf-8
import platform
print platform.system()
class HttpError(object):
	def __init__(self,status_code = '500',log_message =None,header=[]):
		self.status_code = status_code
		self.header = header
		self.reason = log_message


	def __call__(self):
		message = "error ：%s: %s" % (
			self.status_code,self.reason)
		result = (self.status_code,self.header,message)
		print ' this  is result error app 208'
		return result
if __name__ == '__main__':
	#a = HttpError('404','not foound you request page')
	raise  HttpError('404','not foound you request page')