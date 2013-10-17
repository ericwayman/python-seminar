import sqlite3
import numpy as np
from scipy.stats import pearsonr
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
		
		#some signals have shorter length.  Only compute correlation if the length is the same
		if (len(t_1)==len(t_shift_1)):
			temp_pred_1[i,j]=pearsonr(t_1,t_shift_1)[0]
		else:
			temp_pred_1[i,j]=0

		if (len(t_3)==len(t_shift_3)):
			temp_pred_3[i,j]=pearsonr(t_3,t_shift_3)[0]
		else:
			temp_pred_7[i,j]=0
		if (len(t_7)==len(t_shift_7)):
			temp_pred_7[i,j]=pearsonr(t_7,t_shift_7)[0]
		else:
			temp_pred_7[i,j]=0	
	
		if (len(c_1)==len(c_shift_1)):
			cover_pred_1[i,j]=pearsonr(c_1,c_shift_1)[0]
		else:
			cover_pred_1[i,j]=0
		if (len(c_3)==len(c_shift_3)):
			cover_pred_3[i,j]=pearsonr(c_3,c_shift_3)[0]
		else:
			cover_pred_3[i,j]=0
		if (len(c_7)==len(c_shift_7)):
			cover_pred_7[i,j]=pearsonr(c_7,c_shift_7)[0]
		else:
			cover_pred_7[i,j]=0

#print summary of predictions

n=num_airports

#temp change predicitions

#computes the top 10 1 dimensional indices.  Need to convert to two dim using mods
flat_idxs_t1 = (temp_pred_1.flatten()).argsort()[-10:][::-1]
#convert a flat index back to a 2d index
idxs_t1 = [(i/n,i%n-1) for i in flat_idxs_t1]
print "The 10 highest 1 day offset temp change correlations are:"
for i in range(len(idxs_t1)):
	print "The %i largest correlation is:" %(i+1)
	print temp_pred_1.flatten()[flat_idxs_t1[i]]
	print "when using airport %s to predict weather in %s 1 day later" %(icao_codes[idxs_t1[i][0]],icao_codes[idxs_t1[i][1]])

#computes the top 10 1 dimensional indices.  Need to convert to two dim using mods
flat_idxs_t3 = (temp_pred_3.flatten()).argsort()[-10:][::-1]
#convert a flat index back to a 2d index
idxs_t3 = [(i/n,i%n-1) for i in flat_idxs_t3]
print "The 10 highest 3 day offset temp change correlations are:"
for i in range(len(idxs_t3)):
	print "The %i largest correlation is:" %(i+1)
	print temp_pred_3.flatten()[flat_idxs_t3[i]]
	print "when using airport %s to predict weather in %s 3 days later" %(icao_codes[idxs_t3[i][0]],icao_codes[idxs_t3[i][1]])

#computes the top 10 1 dimensional indices.  Need to convert to two dim using mods
flat_idxs_t7 = (temp_pred_7.flatten()).argsort()[-10:][::-1]
#convert a flat index back to a 2d index
idxs_t7 = [(i/n,i%n-1) for i in flat_idxs_t7]
print "The 10 highest 7 day offset temp change correlations are:"
for i in range(len(idxs_t7)):
	print "The %i largest correlation is:" %(i+1)
	print temp_pred_7.flatten()[flat_idxs_t7[i]]
	print "when using airport %s to predict  weather in %s 7 days later" %(icao_codes[idxs_t7[i][0]],icao_codes[idxs_t7[i][1]])

#cloud cover change predicitions

#computes the top 10 1 dimensional indices.  Need to convert to two dim using mods
flat_idxs_c1 = (cover_pred_1.flatten()).argsort()[-10:][::-1]
#convert a flat index back to a 2d index
idxs_c1 = [(i/n,i%n-1) for i in flat_idxs_c1]
print "The 10 highest 1 day offset cloud cover change correlations are:"
for i in range(len(idxs_c1)):
	print "The %i largest correlation is:" %(i+1)
	print cover_pred_1.flatten()[flat_idxs_c1[i]]
	print "when using airport %s to predict  cloud cover change in %s 1 day later" %(icao_codes[idxs_c1[i][0]],icao_codes[idxs_c1[i][1]])

#computes the top 10 1 dimensional indices.  Need to convert to two dim using mods
flat_idxs_c3 = (cover_pred_3.flatten()).argsort()[-10:][::-1]
#convert a flat index back to a 2d index
idxs_c3 = [(i/n,i%n-1) for i in flat_idxs_c3]
print "The 10 highest 3 day offset cloud cover change correlations are:"
for i in range(len(idxs_c3)):
	print "The %i largest correlation is:" %(i+1)
	print cover_pred_3.flatten()[flat_idxs_c3[i]]
	print "when using airport %s to predict  cloud cover change in %s 3 days later" %(icao_codes[idxs_c3[i][0]],icao_codes[idxs_c3[i][1]])

#computes the top 10 1 dimensional indices.  Need to convert to two dim using mods
flat_idxs_c7 = (cover_pred_7.flatten()).argsort()[-10:][::-1]
#convert a flat index back to a 2d index
idxs_c7 = [(i/n,i%n-1) for i in flat_idxs_c7]
print "The 10 highest 7 day offset cloud cover change correlations are:"
for i in range(len(idxs_c7)):
	print "The %i largest correlation is:" %(i+1)
	print cover_pred_7.flatten()[flat_idxs_c7[i]]
	print "when using airport %s to predict  cloud cover change in %s 7 days later" %(icao_codes[idxs_c7[i][0]],icao_codes[idxs_c7[i][1]])
