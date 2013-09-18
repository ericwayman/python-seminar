import re, urllib, urllib2

def calculate(input_string,return_float=False):
	try:
		return eval(input_string, {'__builtins__':{}})
	except (NameError, SyntaxError):
		#app_id = 'UAGAWR-3X6Y8W777Q'
		app_id = 'WTHLUK-WR5TJQ8Y83'
		f={'appid':app_id,'input': input_string}
		api_url = 'http://api.wolframalpha.com/v2/query?' + urllib.urlencode(f)
		xml_response = urllib2.urlopen(api_url).read()
		regex = re.compile('<plaintext>(.*?)</plaintext>')
		answer = regex.findall(xml_response)
		
		#parse a float from the Wolfram answer if requested
		if return_float==True:
			l = []
			for x in answer[1].split():
				try:
					l.append(float(x))
				except ValueError:
					pass	
			if len(l)==0:
				print "There is no float to return or could not parse the correct float."
				return l
			if len(l)>1: 
				print "More than one float was parsed from the answer.  Returning the first"
				return l[0]
			else: 
				return l[0]
		else:
			return answer[1]

if __name__== "__main__":
	import argparse
	parser=argparse.ArgumentParser(description="Query the Wolfrm|Alpha API")
	parser.add_argument("query",
						nargs=1,
						help="Query for the Wolfram|Alpha API.  Don't forget to enclose query in quotes",
						metavar="QUERY")
	parser.add_argument("-f", "--is_float",
						dest = 'is_float',
						action ='store_const',
						const = True,
						default = False,
						help ='The flag -f sets return_float = True',
						)
	print calculate(" ".join(parser.parse_args().query),parser.parse_args().is_float)


def test_1():
	assert abs(9. - calculate('3*3',return_float=True))<.001

def test_2():
	query2 = "When was the Declaration of Independence signed?"
	assert type(calculate(query2,return_float=True))==float

def test_3():
	query3 = "what color is the sky"
	assert len(calculate(query3,return_float=True))==0

def test_4():
	assert calculate('3*3') == 9

def test_5():
	query5 = "How old is the world?"
	assert type(calculate(query5))==str


