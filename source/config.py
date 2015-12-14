#encoding=utf-8
import MySQLdb
import sys
from DBUtils.PooledDB import PooledDB
import time
DEBUG =True

if DEBUG:
    MYSQL_DB = 'iot'
    MYSQL_USER = 'root'
    MYSQL_PASS = ''
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_CHAR ="utf8"
else:
    MYSQL_DB = 'iot'
    MYSQL_USER = 'root'
    MYSQL_PASS = 'zhoulei5014'
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_CHAR ="utf8"


DATABASES =  {
        'NAME': MYSQL_DB,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASS,
        'HOST': MYSQL_HOST,
        'PORT': MYSQL_PORT,
        'CHAR':MYSQL_CHAR
    }



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



#if __name__ == '__main__':
	# a = Mysql()
	# b = Mysql()


	# print Mysql.pool_num
	# print '---------'


	# start1 = time.time()
	# for i in range(10):
	# 	Mysql.Get_conn().cursor()
	# end1 = time.time()
	# print end1-start1

	# print Mysql.conn_num
	# print '---------'
	# print Mysql.pool_num

	# start = time.time()
	# for i in range(1000):
	# 	mysql_conn= MySQLdb.connect(
	# 		host='localhost',
	# 		port = 3306,
	# 		user='root',
	# 		passwd='',
	# 		db ='iot',
	# 		charset="utf8"
	#         )
	# 	mysql_conn.cursor()
	# end = time.time()
	# print end-start
