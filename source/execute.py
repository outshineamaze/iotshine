from celerytest import add
import time
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
start = time.time()

a = ''.join([str(i) for i in range(10000)])

end = time.time()
print end - start

start1 = time.time()
b = ''
for i in range(10000):
	b +=str(i)
end2 = time.time()
print end2-start1
