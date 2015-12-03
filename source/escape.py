#coding:utf-8


# Escaping/unescaping methods for HTML, JSON, URLs, and others.

import re 
import sys
import json
try :
	from urllib.parse import parse_qs 
except ImportError:
	from urlparse import parse_qs
try:
	import htmlentitydefs  # py2
except ImportError:
	import html.entities as htmlentitydefs  # py3

try:
	import urllib.parse as urllib_parse  # py3
except ImportError:
	import urllib as urllib_parse  # py2

unicode_type = unicode  # noqa
basestring_type = basestring  # noqa
UTF8_TYPES = (bytes, type(None))
TO_UNICODE_TYPES = (unicode_type, type(None))
BASESTRING_TYPE = (basestring_type,type(None))


def utf8(value):
	if isinstance(value,UTF8_TYPES):
		#print 'convert to utf-8'
		return value
	if not isinstance (value,unicode_type):
		raise TypeError(
			"except bytes,unicode ,or None;instead of get %s"%type(value))
	return value.encode("utf-8")

def to_unicode(value):
	if isinstance(value, TO_UNICODE_TYPES):
		return value
	if not isinstance(value, bytes):
		raise TypeError(
			"Expected bytes, unicode, or None; got %r" % type(value)
		)
	return value.decode("utf-8")
def json_encode(value):
	return json.dumps(value).replace("</","<\\/")
def json_decode(value):
	return json.loads(to_basestring(value))
def to_basestring(value):
	if isinstance(value,BASESTRING_TYPE):
		return value
	if not isinstance(value,bytes):
		raise TypeError("except bytes ,unicode or None")
	return value.decode("utf-8")


if __name__ == '__main__':
	#print to_basestring()
	# a =json_decode('{ "firstName":"John" , "lastName":"Doe" }')
	
	# print type(a)
	# b = { "firstName":"John" , "lastName":"Doe" }
	# print type(json_encode(b))
	# print utf8('hfs')
	# print to_unicode(None)


