import pandas as pd
import sqlite3, urllib2
from bs4 import BeautifulSoup

#import the first data frame
df1 = pd.read_csv("./hw_6_data/top_airports.csv")

#connect to sqlite to make a database for the aiport data
connection = sqlite3.connect("airport.db")
cursor = connection.cursor()

sql_cmd = """CREATE TABLE airports1 (id INTEGER PRIMARY KEY AUTOINCREMENT,
	city TEXT, faa TEXT, iata TEXT, icao TEXT, airport TEXT, enplanements INT)"""
cursor.execute(sql_cmd)

#loop through each airport in the data frame to fill the table
for i in range(len(df1.index)):
	#select the airport
	airport = df1.iloc[i]
	if (airport["City"] and airport["FAA"] and airport["ICAO"] and airport["Airport"] 
		and airport["Enplanements"] and airport["IATA"]):
		airport_city = airport["City"]
		airport_faa = airport["FAA"]
		airport_iata = airport["IATA"]
		airport_icao = airport["ICAO"]
		airport_name = airport["Airport"]
		airport_enplanements = airport["Enplanements"]

		data = (airport_city,airport_faa, airport_iata, airport_icao, airport_name,airport_enplanements)
		sql_cmd = ("INSERT INTO airports1 (city, faa, iata, icao, airport, enplanements) VALUES " + str(data))
		cursor.execute(sql_cmd)

#import the second data frame
df2 = pd.read_csv('./hw_6_data/ICAO_airports.csv')

#at some point need to convert some of these values to INT
sql_cmd = """CREATE TABLE airports2 (id INTEGER PRIMARY KEY AUTOINCREMENT,
	iata_code TEXT, latitude TEXT, longitude TEXT, elevation TEXT)"""
cursor.execute(sql_cmd)

#loop through each airport in the second data frame to fill the table
for i in range(len(df2.index)):
	#select the airport
	airport = df2.iloc[i]
	if(airport["iata_code"]==airport["iata_code"] 
		and airport["latitude_deg"]==airport["latitude_deg"]
		and airport["latitude_deg"]==airport["latitude_deg"]
		and airport["elevation_ft"]==airport["elevation_ft"]):
		airport_iata = airport["iata_code"]
		airport_lat = airport["latitude_deg"]
		airport_long = airport["longitude_deg"]
		airport_ele = airport["elevation_ft"]
		data = (airport_iata,airport_lat,airport_long,airport_ele)
		sql_cmd = ("INSERT INTO airports2 (iata_code, latitude, longitude, elevation) VALUES" + str(data))
		cursor.execute(sql_cmd)

#join data bases to add info to the main 50 airports
sql_cmd = """CREATE TABLE airports AS SELECT airports1.city, airports1.faa, airports1.iata, airports1.icao, airports1.airport, airports1.enplanements,
		airports2.latitude, airports2.longitude, airports2.latitude, airports2.elevation
		FROM airports1 LEFT JOIN airports2 ON
		airports1.iata = airports2.iata_code
		"""
cursor.execute(sql_cmd)


#extract list of icao_codes.
sql_cmd = ("SELECT icao from airports")
cursor.execute(sql_cmd)
icao_codes = cursor.fetchall()
icao_codes = [x[0] for x in icao_codes]
print icao_codes


#create the initial weather database
sql_cmd = """CREATE TABLE weather (id INTEGER PRIMARY KEY AUTOINCREMENT,
icao TEXT, the_date TEXT, max_temp INTEGER, mean_temp INTEGER, min_temp INTEGER,
cloud_cover INTEGER, precip_in INTEGER)
"""
cursor.execute(sql_cmd)

#make the iterates to loop through to grab the data from each url
years = ['2008','2009','2010','2011','2012','2013']
months = ['1','2','3','4','5','6','7','8','9','10','11','12']
pairs = [(x,y) for x in years for y in months]
pairs.remove(('2013','11'))
pairs.remove(('2013','12'))
iterates = [(x,y[0],y[1]) for x in icao_codes for y in pairs ]


#fill the weather database
for x in iterates:
	#pull the weather information from the web for the url for the given airport month and year
	response = urllib2.urlopen(
			"http://www.wunderground.com/history/airport/%s/%s/%s/1/MonthlyHistory.html?format=1"
			%(x[0],x[1],x[2]))
	html = response.read()
	response.close()
	soup = BeautifulSoup(html)
	text = soup.get_text()

	file_name = 'weather_%s_%s_%s.csv'%(x[0],x[1],x[2])
	#write the text string to a csv file to be read into a pandas data frame
	with open('./csv_files/'+file_name,'w') as f:
		f.write(text)
	#output = file("weather.csv", "w")
	#output.write(text)
	#output.close()

	print "making the weather table"
	print "adding: "+file_name
	#save the table as a pandas dataframe
	df = pd.read_csv('./csv_files/'+file_name, delimiter=',')

	#save the current icao_code to add to the table.  Need to convert to str from unicode string
	icao_code=str(x[0])
	#print "icao_code:"
	#print icao_code
	#print type(icao_code)
	#print len(icao_code)
	#loop through the days of the given month for the given airport
	for i in range(len(df.index)):
		#select the day
		day = df.iloc[i]
		#remember to use the keys from the .csv file, not keys from the .db file
		if(day["Max TemperatureF"]==day["Max TemperatureF"]
			and day["Mean TemperatureF"]==day["Mean TemperatureF"]
			and day["Min TemperatureF"]==day["Min TemperatureF"]
			and day[" CloudCover"]==day[" CloudCover"]
			and day["PrecipitationIn"]==day["PrecipitationIn"]				
			):
			day_date = day[df.keys()[0]]
			day_max_temp = day["Max TemperatureF"]
			day_mean_temp = day["Mean TemperatureF"]
			day_min_temp = day["Min TemperatureF"]
			day_cloud_cover = day[" CloudCover"]
			day_precip_in = day["PrecipitationIn"]
			data = (icao_code, day_date, day_max_temp,day_mean_temp, day_min_temp, day_cloud_cover, day_precip_in)
			sql_cmd = ("INSERT INTO weather (icao, the_date, max_temp, mean_temp, min_temp, cloud_cover, precip_in) VALUES" + str(data))
			cursor.execute(sql_cmd)

connection.commit()
connection.close()


