#encoding=utf-8
import sys
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
    MYSQL_PASS = '*************'
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
