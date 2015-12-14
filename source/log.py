#encoding=utf-8
import logging
import logging.handlers
import platform
# 创建一个logger

def log_path():
	
	try:
		sysstr = platform.system()
	except:
		sysstr = "Other System"
	if sysstr== "Windows":
		
		return "iot.log"

	elif sysstr=="Linux":
		return "/var/log/iot.log"

logger = logging.getLogger('log')
logging.basicConfig(level=logging.INFO,  
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', 
                    filemode='w') 
# 创建一个handler，用于写入日志文件
#fh = logging.FileHandler('iot.log')
fh =logging.handlers.RotatingFileHandler( log_path(),'w', 10737418240,10)
#fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('file:%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
#formatter1 = logging.Formatter('cons:%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)





