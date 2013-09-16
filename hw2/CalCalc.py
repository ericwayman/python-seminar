import re, urllib, urllib2

def calculate(input_string):
	try:
		return eval(input_string, {'__builtins__':{}})
	except (NameError, SyntaxError):
		f={'appid':'UAGAWR-3X6Y8W777Q','input': input_string}
		api_url = 'http://api.wolframalpha.com/v2/query?' + urllib.urlencode(f)
		xml_response = urllib2.urlopen(api_url).read()
		regex = re.compile('<plaintext>(.*?)</plaintext>')
		info = regex.findall(xml_response)
		return info[1]

if __name__== "__main__":
	import sys
	print calculate(str(sys.argv[1]))
