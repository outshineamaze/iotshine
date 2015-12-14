#coding:utf-8
from celerytest import add
from database import device_sensor
from log import logger, log_path
import time



print log_path()

#a = [add.apply_async((i, i), queue='lopri', countdown=1) for i in range(100)]
#r = [add.delay(i, i) for i in xrange(1,1000)]
# print r.ready()
# print r.status
# print r.result
# print r.status
# result =  add.delay(5,4)
# print result.state
# print result.ready()
# print result.wait()
#print a
# start = time.time()


# end = time.time()
# print end - start

# start1 = time.time()

# end2 = time.time()
# print end2-start1

# for i in range(10):
# 	logger.info("hsdaghkjsahgfwioeugjhsjakgklsadjioguiowjgiosjalkghjsagoiwrgio")
logger.info("execute")
a = device_sensor().find(sensor_name="Int 传感器")

logger.info(a)
