import sqlite3
import numpy as np
#connect to the airport database "airport.db"
connection = sqlite3.connect("airport.db")
cursor = connection.cursor()

#select the list of icao airport codes and save as a list "icao_codes"
sql_cmd = ("SELECT icao from airports")
cursor.execute(sql_cmd)
icao_codes = cursor.fetchall()
icao_codes = [str(x[0]) for x in icao_codes]
#sort in alphabetical order
icao_codes.sort()
num_airports = len(icao_codes)
print "There are %i airports, and they have the following codes: "%(num_airports)
print icao_codes


#pull icao_code, max_temp and cloud_ocver info from database=
sql_cmd = ("SELECT icao, max_temp,cloud_cover FROM weather")
cursor.execute(sql_cmd)
info = cursor.fetchall()
print info[0:5]

#extract data into separate lists
icao_info = [str(x[0]) for x in info]
max_temp_info = [int(x[1]) for x in info]
cloud_cover_info = [int(x[2]) for x in info]

#initialize lists of signals.  The signals contain all values of daily max_temp and cloud_cover 
#change as calculated over each day
ccover_sig_list =[]
mtemp_sig_list = []

#loop through the list of airport codes to fill the signal list
for code in icao_codes:
	#extract the max_temp and cloud color info for all entries corresponding to the
	#airport with icao code: code
	cloud_sig = np.array([cloud_cover_info[i] for i,x in enumerate(icao_info) if x==code])
	temp_sig = np.array([max_temp_info[i] for i,x in enumerate(icao_info) if x==code])

	
	#compute the daily changes
	cloud_change_sig = cloud_sig[1:]-cloud_sig[:-1]
	temp_change_sig = temp_sig[1:]-temp_sig[:-1]

	#append these signals to the appropriate lists
	ccover_sig_list.append(cloud_change_sig)
	mtemp_sig_list.append(temp_change_sig)


#compute the correlation matrices for 1,3,7 day predictions

#initialize the matrices
temp_pred_1 = np.zeros((num_airports, num_airports))
temp_pred_3 = np.zeros((num_airports, num_airports))
temp_pred_7 = np.zeros((num_airports, num_airports))
cover_pred_1 = np.zeros((num_airports, num_airports))
cover_pred_3 = np.zeros((num_airports, num_airports))
cover_pred_7 = np.zeros((num_airports, num_airports))

for i in range(num_airports):
	#compute the unshifted signals
	t_1 = mtemp_sig_list[i][:-1]
	t_3 = mtemp_sig_list[i][:-3]
	t_7 = mtemp_sig_list[i][:-7]
	c_1 = ccover_sig_list[i][:-1]
	c_3 = ccover_sig_list[i][:-3]
	c_7 = ccover_sig_list[i][:-7]

	for j in range(num_airports):
		#compute the shifted signals
		t_shift_1 = mtemp_sig_list[j][1:]
		t_shift_3 = mtemp_sig_list[j][3:]
		t_shift_7 = mtemp_sig_list[j][7:]
		c_shift_1= ccover_sig_list[j][1:]
		c_shift_3= ccover_sig_list[j][3:]
		c_shift_7= ccover_sig_list[j][7:]

		#compute the correlation between the ith signal and the jth shifted signal
		#and entry it as the (i,j) entry of the appropriate matrix
		temp_pred_1[i,j]=np.correlate(t_1,t_shift_1)[0]
		temp_pred_3[i,j]=np.correlate(t_3,t_shift_3)[0]
		temp_pred_7[i,j]=np.correlate(t_7,t_shift_7)[0]
		cover_pred_1[i,j]=np.correlate(c_1,c_shift_1)[0]
		cover_pred_3[i,j]=np.correlate(c_3,c_shift_3)[0]
		cover_pred_7[i,j]=np.correlate(c_7,c_shift_7)[0]



