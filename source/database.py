#encoding=utf-8
import MySQLdb
import sys
import logging

from DBUtils.PooledDB import PooledDB
from config import DATABASES



class Mysql(object):
	Mysql_Pool = None
	conn_num = 0
	pool_num = 0

	def __init__(self):
		Mysql.Mysql_Pool = Mysql.GetConnection()
	@staticmethod
	def GetConnection():

		if Mysql.Mysql_Pool is None:
			Mysql.pool_num+=1
			Mysql_Pool = PooledDB(creator=MySQLdb,mincached =1,maxcached =200,
				host = DATABASES["HOST"],port = DATABASES["PORT"],user = DATABASES["USER"],
				db = DATABASES["NAME"],use_unicode=False,charset=DATABASES["CHAR"])
			return Mysql_Pool
	@staticmethod
	def Get_conn():
		if Mysql.Mysql_Pool is None:
			Mysql()
			Mysql.conn_num +=1
			return Mysql.Mysql_Pool.connection()
		else:
			Mysql.conn_num +=1
			return Mysql.Mysql_Pool.connection()


#创建数据表
#cur.execute("create table student(id int ,name varchar(20),class varchar(30),age varchar(10))")

#插入一条数据
#cur.execute("insert into student values('4532w56532','To67m','male',14,'fgs','sdgdf','fasgsf',)".strip(","))
#print "insert into student values('4532w56532','To67m','male',14,'fgs','sdgdf','fasgsf',)".strip(",")

#修改查询条件的数据
#a = cur.execute("select * from %s",'student')

# b = cur.execute("select * from student")
# print cur.fetchall()
#删除查询条件的数据
#cur.execute("delete from student where age='9'")


class DatabaseError(Exception):
	"""docstring for DatabaseError"""
	def __init__(self, arg):
		self.reason = arg

	def __str__(self):
		return "DatabaseError:"+str(self.reason)
		#print sys.exc_info() 

class BaseModel(object):
	"""docstring for BaseModel"""
	def __init__(self,name,args={}):
		print 'init BaseModel',name
		self.table = name
		result = None
		self.index =None
		print self.table
		self.mysql_conn = Mysql.Get_conn()
		self.cur = self.mysql_conn.cursor()
		if len(args)>0:
			sql= self.prepare_sql('select',args)
			try:
				self.cur.execute(sql)
				result= self.cur.fetchone()

			except MySQLdb.Error,e:
				print "Mysql Error %d: %s" % (e.args[0], e.args[1])
			if result!=None:
				self.index= result[0]
				print 'self.index = ',self.index
	def __del__(self):
		print 'eciting'
		self.cur.close()
		self.mysql_conn.commit()
		self.mysql_conn.close()




	def prepare_sql(self,method,args={}):
		avalible_method = ['insert','select','update','delete']
		exe_method = None
		if method in avalible_method:
			exe_method = method
		else:
			return "there is invalide method ,avalible_method in ['insert','select','update','delete']"

		if exe_method =="select":
			sql_str ="select * from "+self.table+" where "

			if len(args)>0:
				for key in args:
					if isinstance(args[key],str):
						sql_str+= str(key)+ " = '" +str(args[key])+"' and "
					else:
						sql_str+= str(key)+ " = " +str(args[key])+" and "

			return sql_str.strip(" and ")

		elif exe_method == "insert":
			key= " ("

			key += "".join([i+"," for i in args]).strip(",")
			print key
			value=""
			for i in args:
				if isinstance(args[i],str):
					value+="'"+args[i]+"',"
				else:
					value+= str(args[i])+","
			print value
			sql_str = "insert into "+self.table+key+") values("+value.strip(",")+")"
			return sql_str


		elif exe_method =="update":
			strings=""
			for i in args:
				if isinstance(args[i],str):

					strings += " "+i+"='"+args[i]+"',"
				else:
					strings += " "+i+"="+str(args[i])+","
			if self.index==None:
				raise DatabaseError("please instance the BaseModel")
			sql_str = "update "+self.table+" set "+strings.strip(",")+" where id="+ str(self.index)
			return sql_str


		elif exe_method=="delete":
			if self.index ==None:
				raise DatabaseError("please instance the BaseModel")
			sql_str = "delete from "+self.table+" where id = "+str(self.index)
			return sql_str

	# using tuiple as argurment 	
	#
	#	
	# def prepare_sql_turple(self,method,args):
	# 	avalible_method = ['insert','select','update','delete']
	# 	if  method in avalible_method:
	# 		exe_method = method
	# 	else :
	# 		return "there is invalide method ,avalible_method in ['insert','select','update','delete']"
	# 	if method =="select":
	# 		sql_str ="select * from "+self.table+" where "+str(args[0][0])+ " = '" +str(args[0][1])+"'"
	# 		if len(args) > 1:
	# 			for i in range(1,len(args)):
	# 				sql_str+= " and "+str(args[i][0])+ " = '" +str(args[i][1])+"'"
	# 		return sql_str	
	# 	elif method == "insert":
	# 		key = " (".join([i[0]+"," for i in args]).strip(",")
	# 		value ="".join([i[1]+"," for i in args]).strip(",")
	# 		sql_str = "insert into "+self.table+key+") values("+value+")"
	# 		return sql_str
	# 	elif method =="update":
	# 		for i in args:
	# 			strings += " ".join(i[0]).join("=").join(i[1])
	# 		sql_str = "update "+self.table+" set "+strings+" where id="+ str(self.index)
	# 		return sql_str
	# 	elif method=="delete":
	# 		sql_str = "delete form "+self.table+" where id = "+str(self.index)
	# 		return sql_str





	def find(self,**args):

		sql= self.prepare_sql('select',args)
		print sql
		result = None
		try:
			self.cur.execute(sql)
			result= self.cur.fetchall()
		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])
		#print isinstance(result[1][2],unicode)
		print result 
		return result
	def get(self,**args):
		a = args
		sql= self.prepare_sql('select',a)
		print sql
		result = None


		try:
			self.cur.execute(sql)
			result= self.cur.fetchone()

		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])
		# if result!=None:
		# 	self.index= result[0]
		# 	print 'self.index = ',self.index

		#print result
		return result

	def update(self,**args):

		sql= self.prepare_sql('update',args)
		print sql
		result = None
		try:
			result = self.cur.execute(sql)

		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])
		return result
	def insert(self,**args):
		sql= self.prepare_sql('insert',args)
		print sql
		result = None
		try:
			result = self.cur.execute(sql)

		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])
		return result



	def delete(self):
		sql= self.prepare_sql('delete')
		print sql
		result = None
		try:
			result = self.cur.execute(sql)

		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])
		return result

	def save(self):
		pass



class device_sensor(BaseModel):
	"""docstring for sensor"""
	def __init__(self,**args):
		super(device_sensor, self).__init__(self.__class__.__name__,args)
		print self.table

if __name__ == '__main__':

	# mysql_conn= MySQLdb.connect(
	# 	host='localhost',
	# 	port = 3306,
	# 	user='root',
	# 	passwd='',
	# 	db ='iot',
	# 	charset="utf8"
 #        )
	# cur = mysql_conn.cursor()

	# mysql_conn = Mysql.Get_conn()
	# cur = mysql_conn.cursor()


	#x  =device_sensor(id =1)
	#b  = device_sensor(id =11)
	#a = device_sensor().find(sensor_name="Int 传感器")
	#b = device_sensor().find(data_type=1)
	
	#c = device_sensor().insert(sensor_name='outshin53',sensor_slug=234,is_active=1,sensor_device_id=1,data_type=1)
	#x.update(data_type=1,sensor_slug=233)
	#b.update(data_type=1,sensor_slug=233)
	

	# try:
	# 	b = device_sensor().delete()
	# except DatabaseError as e: 

	# 	print e
	
	#b = device_sensor().delete()

	# cur.close()
	# mysql_conn.commit()
	# mysql_conn.close()
	logging.debug('This is debug message')



