#imports
import pandas as pd
import sqlite3
import pandas.io.sql as sql
from datetime import datetime
from pytz import timezone




#connect to sqlite to make a database for the bus arrival database
connection = sqlite3.connect("bus_arrival.db")
#connection = sqlite3.connect(':memory:')
cursor=connection.cursor()

#import scheduledArrivalDataNew.json as a a dataframe
sched_arrival_df = pd.read_json('./bus_data/scheduledArrivalDataNew.json')

#rename the 'arrival_time' column to 'sched_arrival_time' so it doesn't overlap
#with the actual 'arrival_time' column from the actual arrival database
sched_arrival_df.rename(columns={'arrival_time': 'sched_arrival_time'}, inplace=True)

#import arrivalDataNew.json as a dataframe
actual_arrival_df= pd.read_json('./bus_data/arrivalDataNew.json')
#convert unix time to datetime objects
sansebastianTimeZone = timezone('Europe/Amsterdam')
actual_arrival_df['arrival_time'] = actual_arrival_df['arrival_time'].apply(lambda x: datetime.fromtimestamp(int(x/1000), sansebastianTimeZone))
actual_arrival_df['departure_time'] = actual_arrival_df['departure_time'].apply(lambda x: datetime.fromtimestamp(int(x/1000), sansebastianTimeZone))


#write the data frames to a .db sql database
sql.write_frame(frame=sched_arrival_df,name='sched_arrival',con=connection)
sql.write_frame(frame=actual_arrival_df,name='actual_arrival',con=connection)

