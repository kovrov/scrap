import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s')
indent = 0

def debug(func):
	return func  # no log
	def wrapped_func(*args, **kwargs):
		global indent
		msg = func.__name__ + " " + str(args) + str(kwargs)
		logging.debug('>>> ' + ' ' * indent + msg)
		indent += 1
		res = func(*args, **kwargs)
		indent -= 1
		return res
	return wrapped_func

def info(func):
	return func  # no log
	def wrapped_func(*args, **kwargs):
		global indent
		msg = func.__name__ + " " + str(args) + str(kwargs)
		logging.info('>>> ' + ' ' * indent + msg)
		indent += 1
		res = func(*args, **kwargs)
		indent -= 1
		return res
	return wrapped_func

def log(msg):
	logging.info(msg)
