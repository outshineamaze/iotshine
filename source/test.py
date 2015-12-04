#coding:utf-8
# -*- coding: utf-8 -*-
import urllib2
import urllib
import requests
import json
import threading

#http://120.26.197.101/admin/
url4="http://127.0.0.1:8000/device/adddevice/"
data4 = {"device_user":12,"device_type":0,"device_name":"测试device","is_active":1}

url1 = "http://127.0.0.1:8000/device/1/addsensor/"
data1 = {'sensor_name':'ds188b20','data_type':0,'slug':1111}

url = "http://120.26.197.101/device/1/sensor/3/datapoint/add/"
data = {"data_type":2,"data":12,'apikey':'GuRlcdjtSaxWhogmHsDB'}

urls = "http://127.0.0.1:8000/device/1/sensor/4/datapoint/get/"

url4="http://127.0.0.1:8000/device/1/put/"
data4 = {"device_type":2,"device_name":"一个测试device","is_active":1}

url3="http://127.0.0.1:8000/device/1/sensor/1/put/"
data3 = {"data_type":2,"sensor_name":"有一个温度传感器","is_active":0,'sensor_slug':12131}

def postbyjson(url,data):
    apiheaders = {'apikey':'GuRlcdjtSaxWhogmHsDB', 'content-type': 'application/json'}   
    data_encode = json.dumps(data)
    print(type(data_encode))
    req = urllib2.Request(url=url,headers=apiheaders,data=data_encode)
    print(url)
    print("---------------------------")
    res_data = urllib2.urlopen(req)
    res= res_data.read()
    print (res)

url5 = "http://115.159.57.15:8888/"
data5= {'sensor-name':'a sensor by test','data_type':0,'slug':0001}
def post(url,data):
    data_encode = urllib.urlencode(data)
    print data
    req = urllib2.Request(url=url,data = data_encode)
    print url
    res_data =urllib2.urlopen(req)
    res= res_data.read()
    print(res)
    
def get(urls):
    req =urllib2.Request(urls)

    print("---------------------------")
    res_data = urllib2.urlopen(req)
    res = res_data.read()
    
#urls(url1,data1)

def func(th):
	for i in range(1000):
		print str(i)+'number of loop ---- : thread :'+str(th)
		get("http://115.159.57.15:8888/")
def MultiThread(th_num):
	thlist = []
	for i in range(0,th_num):
		thread_name  = "thread_%d"%(i)
		thlist.append(threading.Thread(target = func,name = thread_name,args=(i,)))
	for thread in thlist:
		thread.start()
	for thread in thlist:
		thread.join()


if __name__=='__main__':
	a = MultiThread(5)
	print 'over'


#post(url5,data5)
