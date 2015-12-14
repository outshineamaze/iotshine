from celery import Celery
import time
app = Celery('tasks',backend='redis://127.0.0.1:6379' ,broker='redis://127.0.0.1:6379')

@app.task
def add(x, y):
	print 'success add %d%d=%d'%(x,y,x+y)
	return x + y