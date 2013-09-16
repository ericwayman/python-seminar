import urllib2

def calculate(input_string):
	try:
		return eval(input_string, {'__builtins__':{}})
	except NameError:
		

