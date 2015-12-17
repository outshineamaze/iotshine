#coding:utf-8
import sys
import os
import select
import threading
import time
import select

class SelectLoop(object):
	def __init__(self,server,timeout,callback):
		self.server= server
		self.timeout = timeout
		self.callback = callback
	def start(self):
		print '>>>>>>>>>>>>>start main select loop <<<<<<<<<<<<<<<'
		input = [self.server]
		output = []
		running = True
		while running:
			try :
				readble,writeable,exception = select.select(input,output,[])
			except select.error,e:
				break	
			for sock in readble:
				if sock is self.server:
					client ,addr  = self.server.accept()
					client.setblocking(0)
					print '>>>new connect from client %s'%str(addr)


					#self.outputs.append(client)
					#self.clientmap[client]=addr
					input.append(client)
				else :
					try:
						data = sock.recv(1024)
					except socket.error,e:
						print ">>>>>>>Error receiving data: %s"%e
						data=False
					if data:
						#print data.splitlines()[:2]
						print ">>>>>>>>this is response"
						result = self.callback(data)
						print result

						sock.sendall(result)
						print '>>>>>>>>success return response'
						#if sock in self.outputs:self.outputs.remove(sock)
						#print '>>>>>>close connection<<<<<<<<<'
						input.remove(sock)
						sock.close()
							
					else:
						#if sock in self.outputs:self.outputs.remove(sock)
						print '>>>>>>no message from client'
						input.remove(sock)
						sock.close()
						


		self.server.close()


class EPollLoop(object):
	def __init__(self,server,timeout,callback):
		self.callback= callback
		self.timeout = timeout
		self.server = server
		self.server.setblocking(0)
		self.epoll= select.epoll()
		self.epoll.register(self.server.fileno(),select.EPOLLIN)
		#message_queues ={}
		self.fd_to_socket = {self.server.fileno():self.server}
	def start(self):

		while True:
			print "waiting for connecting ........."
			events = self.epoll.poll(self.timeout)
			if not events:
				print 'there is no events for connecting...'
				continue

			for fd,event in events:

				socket  =  self.fd_to_socket[fd]
				print 'activate client socket'
				if socket and select.EPOLLIN:
					if socket == self.server:
						connection ,address = self.server.accept()
						print 'new connection ',address
						connection.setblocking(0)
						self.epoll.register(connection.fileno(),select.EPOLLIN)
						self.fd_to_socket[connection.fileno()]= connection
						#message_queues[connection] =Queue.Queue()
					else:
						try:

							data = socket.recv(1024)
						except:
							data= False
						if data :
							print 'recv data client :' ,socket.getpeername()
							#message_queues[socket].put(data)
							#self.epoll.modify(fd,select.EPOLLOUT)
							result = self.callback(data)
							socket.sendall(result)
							print 'send data:',data,'>>>client :',socket.getpeername()
							self.epoll.unregister(fd)
							self.fd_to_socket[fd].close()
							del self.fd_to_socket[fd]
						else:
							print 'close  client connection ',socket.getpeername()
							self.epoll.unregister(fd)
							self.fd_to_socket[fd].close()
							del self.fd_to_socket[fd]
							

				elif event and select.EPOLLHUB:
					self.epoll.unregister(fd)
					self.fd_to_socket[fd].close()
					del self.fd_to_socket[fd]

		self.epoll.unregister(server.fileno())
		self.epoll.close()
		self.server.close()
