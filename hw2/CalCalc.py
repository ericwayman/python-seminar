import re, urllib, urllib2

def calculate(input_string):
	try:
		return eval(input_string, {'__builtins__':{}})
	except (NameError, SyntaxError):
		app_id = 'UAGAWR-3X6Y8W777Q'
		f={'appid':app_id,'input': input_string}
		api_url = 'http://api.wolframalpha.com/v2/query?' + urllib.urlencode(f)
		xml_response = urllib2.urlopen(api_url).read()
		regex = re.compile('<plaintext>(.*?)</plaintext>')
		info = regex.findall(xml_response)
		return info[1]

if __name__== "__main__":
	#import sys
	#print calculate(str(sys.argv[1]))
	import argparse
	parser=argparse.ArgumentParser(description="Query the Wolfrm|Alpha API")
	parser.add_argument("query",
						nargs=1,
						help="Query for the Wolfram|Alpha API.  Don't forget to enclose query in quotes",
						metavar="QUERY")
	print calculate(" ".join(parser.parse_args().query))
