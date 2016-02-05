#encoding=utf-8
import MySQLdb
import sys

from log import logger

from DBUtils.PooledDB import PooledDB
from config import DATABASES



class Mysql(object):
	Mysql_Pool = None
	conn_num = 0
	pool_num = 0
	instans_num = 0

	# def __init__(self,h):
	# 	 Mysql.instans_num +=1

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
			print 'dont instans mysql class'
			Mysql.Mysql_Pool = Mysql.GetConnection()
			Mysql.conn_num +=1
			return Mysql.Mysql_Pool.connection()
		else:
			Mysql.conn_num +=1
			return Mysql.Mysql_Pool.connection()
	def Get_conn_instance(self):
		if Mysql.Mysql_Pool is None:
			Mysql.Mysql_Pool = Mysql.GetConnection()
			Mysql.conn_num +=1
			return Mysql.Mysql_Pool.connection()
		else:
			Mysql.conn_num +=1
			return Mysql.Mysql_Pool.connection()





class DatabaseError(Exception):
	"""docstring for DatabaseError"""
	def __init__(self, arg):
		self.reason = arg

	def __str__(self):
		return "DatabaseError:"+str(self.reason)
		#print sys.exc_info() 

class Field(object):
	def __init__(self, name, column_type):
		self.name = name
		self.column_type = column_type

	def __str__(self):
		return '<%s:%s>' % (self.__class__.__name__, self.name)

class StringField(Field):
	def __init__(self,name,null=False,default = None):
		super(StringField,self).__init__(name,'varchar(100)')
		self.null = null
		self.default= default
class IntegerField(Field):
	def __init__(self, name,null=False,default = None):
		super(IntegerField, self).__init__(name, 'int(11)')
		self.null = null
		self.default= default


class ModelMetaclass(type):
	def __new__(cls,name,bases,attrs):
		if name=="BaseModel":
			return type.__new__(cls,name,bases,attrs)
		mappings = dict()
		for k, v in attrs.iteritems():
			if isinstance(v, Field):
				print('Found mapping: %s==>%s' % (k, v))
				mappings[k] = v
		for k in mappings.iterkeys():
			attrs.pop(k)
		attrs['table'] = name # 假设表名和类名一致
		attrs['__mappings__'] = mappings # 保存属性和列的映射关系
		return type.__new__(cls, name, bases, attrs)



# class Model(dict):
# 	__metaclass__ = ModelMetaclass

# 	def __init__(self, **kw):
# 		super(Model, self).__init__(**kw)

# 	def __getattr__(self, key):
# 		try:
# 			return self[key]
# 		except KeyError:
# 			raise AttributeError(r"'Model' object has no attribute '%s'" % key)

# 	def __setattr__(self, key, value):
# 		self[key] = value

# 	def save(self):
# 		fields = []
# 		params = []
# 		args = []
# 		for k, v in self.__mappings__.iteritems():
# 			fields.append(v.name)
# 			params.append('?')
# 			args.append(getattr(self, k, None))
# 		sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
# 		print('SQL: %s' % sql)
# 		print('ARGS: %s' % str(args))

# class Student(Model):
#     name = StringField('username')


class BaseModel(dict):
	__metaclass__ = ModelMetaclass
	"""docstring for BaseModel"""

	def __init__(self,**kw):
		super(BaseModel, self).__init__( **kw)

		print 'init BaseModel'

		self.mysql_conn =None
		result = None
		self.index =None
		print self.table

		# if len(kw)>0:
		# 	sql= self.prepare_sql('select',kw)
		# 	try:
		# 		self.cur.execute(sql)
		# 		result= self.cur.fetchone()

		# 	except MySQLdb.Error,e:
		# 		print "Mysql Error %d: %s" % (e.args[0], e.args[1])
		# 	if result!=None:
		# 		self.index= result[0]
		# 		print 'self.index = ',self.index


	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Model' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value


	def __del__(self):
		print 'start del obj'
		print self.mysql_conn

		if self.mysql_conn!=None:

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
		self.mysql_conn = Mysql.Get_conn()
		self.cur = self.mysql_conn.cursor()
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

	def findall(self,offset =None,limit =None):
		self.mysql_conn = Mysql.Get_conn()
		self.cur = self.mysql_conn.cursor()
		if offset !=None and limit !=None:
			sql = 'select * from '+self.table+" LIMIT "+str(offset)+","+str(limit)
		elif limit!=None:
			sql  = 'select * from '+self.table+" LIMIT "+str(limit)
		else :
			sql  = 'select * from '+self.table
		print sql
		result = None
		try:
			self.cur.execute(sql)
			result= self.cur.fetchall()

		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])
		rt=[]
		kwges={}
		if result !=None:
			for i in result:
				print i
				for k ,v in enumerate(self.__mappings__):
					kwges[v] = i[k]   
				print kwges
				rt.append(self.__class__(**kwges)) 


		return rt


	def get(self,**args):
		self.mysql_conn = Mysql.Get_conn()
		self.cur = self.mysql_conn.cursor()
		a = args
		sql= self.prepare_sql('select',a)
		print sql
		result = None


		try:
			self.cur.execute(sql)
			result= self.cur.fetchone()

		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])

		if result !=None:
			for k ,v in enumerate(self.__mappings__):
				self[v] = result[k]

		return self

	def update(self,**args):
		self.mysql_conn = Mysql.Get_conn()
		self.cur = self.mysql_conn.cursor()
		sql= self.prepare_sql('update',args)
		print sql
		result = None
		try:
			result = self.cur.execute(sql)

		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])
		return result
	def insert(self,**args):

		self.mysql_conn = Mysql.Get_conn()
		self.cur = self.mysql_conn.cursor()
		sql= self.prepare_sql('insert',args)
		print sql
		result = None
		try:
			result = self.cur.execute(sql)

		except MySQLdb.Error,e:
			print "Mysql Error %d: %s" % (e.args[0], e.args[1])
		return result



	def delete(self):
		self.mysql_conn = Mysql.Get_conn()
		self.cur = self.mysql_conn.cursor()
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

class test(BaseModel):
	idnum = IntegerField('id')
	name = StringField('name')
	number  = IntegerField('number')

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

	# for i in range(10000):

	# 	Mysql.Get_conn()

	# print Mysql.conn_num 
	# print Mysql.instans_num

	# for h in range(10):
	# 	a  = Mysql(h)
	# 	print a.h
	# 	print a
	# b = Mysql(4)
	# print b
	# print Mysql
	# print Mysql.instans_num


	# u = Student(name='Michael')
	# u.save()





	# x  =device_sensor(id =1)
	# b  = device_sensor(id =11)
	# a = device_sensor().find(sensor_name="Int 传感器")
	# b = device_sensor().find(data_type=1)
	# b = test().findall(5,7)
	# b = test().get(id=1)
	# print '-------'
	# print b['name']
	# print test(idnum=1,name='me',number=4).name
	# print [test().findall()[i].idnum for i  in range(4)]
	a = dict(id = '23',x='54',me='hhh')
	a['outshine']='hell'
	a['dfds']=234
	print a

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

	# logger.info("thiV是的sisi ")



