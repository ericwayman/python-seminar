
Included are 2 Py scripts: make_weather_database.py and weather_predictor.py

make_weather_database.py
Makes a database airport.db which has two tables airports and weather
airports has the following fields for the 50 most traveled airports in the us
city, faa, iata, icao, airport, enplanements
weather has the following fields for the same airports:
icao, the_date, max_temp, mean_temp, min_temp, cloud_cover, precip_in

weather_predictor.py predicts the 10 highest correlations between max_temp change and cloud cover changes between one city and and the same change in a second city 1,3 or 7 days later.

A summary of the weather predictions:
(note: I believe the correlations are correct, but I'm not entirely
sure if I parsed the indices correctly to find the airports involved in the predictions.  Also I ran out of time to complete the graphs as I spend most of my time building the database)

The 10 highest 1 day offset temp change correlations are:
The 1 largest correlation is:
0.532490562916
when using airport KIND to predict weather in KDAL 1 day later
The 2 largest correlation is:
0.529957795361
when using airport KIND to predict weather in KBOS 1 day later
The 3 largest correlation is:
0.524734629994
when using airport KIND to predict weather in KHOU 1 day later
The 4 largest correlation is:
0.521361112712
when using airport KMDW to predict weather in KBOS 1 day later
The 5 largest correlation is:
0.516732157784
when using airport KMDW to predict weather in KHOU 1 day later
The 6 largest correlation is:
0.514944155818
when using airport KMDW to predict weather in KDAL 1 day later
The 7 largest correlation is:
0.513490580788
when using airport KMCI to predict weather in KCLT 1 day later
The 8 largest correlation is:
0.503080871196
when using airport KSTL to predict weather in KPHX 1 day later
The 9 largest correlation is:
0.501703229225
when using airport KMCI to predict weather in KIAH 1 day later
The 10 largest correlation is:
0.491398038982
when using airport KDTW to predict weather in KLAX 1 day later
The 10 highest 3 day offset temp change correlations are:
The 1 largest correlation is:
0.144302387178
when using airport KSNA to predict weather in KATL 3 days later
The 2 largest correlation is:
0.140377142764
when using airport KSNA to predict weather in KCVG 3 days later
The 3 largest correlation is:
0.137528904749
when using airport KLAX to predict weather in KATL 3 days later
The 4 largest correlation is:
0.133249463649
when using airport KSNA to predict weather in KDEN 3 days later
The 5 largest correlation is:
0.12910691896
when using airport KLAX to predict weather in KCVG 3 days later
The 6 largest correlation is:
0.124510688808
when using airport KSAN to predict weather in KATL 3 days later
The 7 largest correlation is:
0.124239394043
when using airport KSNA to predict weather in KSAN 3 days later
The 8 largest correlation is:
0.122878086535
when using airport KSLC to predict weather in KDFW 3 days later
The 9 largest correlation is:
0.12026096101
when using airport KLAX to predict weather in KDEN 3 days later
The 10 largest correlation is:
0.119288650927
when using airport KSAN to predict weather in KCVG 3 days later
The 10 highest 7 day offset temp change correlations are:
The 1 largest correlation is:
0.0815375750536
when using airport KSLC to predict  weather in KTPA 7 days later
The 2 largest correlation is:
0.0672571736639
when using airport KLAS to predict  weather in KCLE 7 days later
The 3 largest correlation is:
0.0653934301153
when using airport KPHX to predict  weather in KBNA 7 days later
The 4 largest correlation is:
0.0643772704246
when using airport TJSJ to predict  weather in KTPA 7 days later
The 5 largest correlation is:
0.0639875698221
when using airport KDTW to predict  weather in KTPA 7 days later
The 6 largest correlation is:
0.0617043818986
when using airport KMCO to predict  weather in KLAS 7 days later
The 7 largest correlation is:
0.0606120258766
when using airport KCLT to predict  weather in KDTW 7 days later
The 8 largest correlation is:
0.0598487602977
when using airport KMCO to predict  weather in KSMF 7 days later
The 9 largest correlation is:
0.0581983361845
when using airport KBOS to predict  weather in KORD 7 days later
The 10 largest correlation is:
0.057624690804
when using airport PHNL to predict  weather in KSMF 7 days later
The 10 highest 1 day offset cloud cover change correlations are:
The 1 largest correlation is:
0.432460707387
when using airport KMDW to predict  cloud cover change in KPHX 1 day later
The 2 largest correlation is:
0.404682869861
when using airport KSTL to predict  cloud cover change in KHOU 1 day later
The 3 largest correlation is:
0.401100985785
when using airport KMDW to predict  cloud cover change in KBOS 1 day later
The 4 largest correlation is:
0.400982905985
when using airport KMDW to predict  cloud cover change in KHOU 1 day later
The 5 largest correlation is:
0.398362579886
when using airport KMCI to predict  cloud cover change in KCLT 1 day later
The 6 largest correlation is:
0.397336232987
when using airport KMDW to predict  cloud cover change in KDTW 1 day later
The 7 largest correlation is:
0.39627705305
when using airport KSTL to predict  cloud cover change in KDAL 1 day later
The 8 largest correlation is:
0.395516704451
when using airport KMEM to predict  cloud cover change in KPIT 1 day later
The 9 largest correlation is:
0.394423332794
when using airport KSTL to predict  cloud cover change in KBOS 1 day later
The 10 largest correlation is:
0.393210595873
when using airport KIAH to predict  cloud cover change in TJSJ 1 day later
Erics-MacBook-Air:hw6 waymaniac$ Python weather_predictor.py 
There are 50 airports, and they have the following codes: 
['KATL', 'KAUS', 'KBNA', 'KBOS', 'KBWI', 'KCLE', 'KCLT', 'KCVG', 'KDAL', 'KDCA', 'KDEN', 'KDFW', 'KDTW', 'KEWR', 'KFLL', 'KHOU', 'KIAD', 'KIAH', 'KIND', 'KJFK', 'KLAS', 'KLAX', 'KLGA', 'KMCI', 'KMCO', 'KMDW', 'KMEM', 'KMIA', 'KMKE', 'KMSP', 'KMSY', 'KOAK', 'KORD', 'KPDX', 'KPHL', 'KPHX', 'KPIT', 'KRDU', 'KSAN', 'KSAT', 'KSEA', 'KSFO', 'KSJC', 'KSLC', 'KSMF', 'KSNA', 'KSTL', 'KTPA', 'PHNL', 'TJSJ']
[(u'KATL', 47, 1), (u'KATL', 30, 1), (u'KATL', 40, 1), (u'KATL', 47, 3), (u'KATL', 55, 6)]
The 10 highest 1 day offset temp change correlations are:
The 1 largest correlation is:
0.532490562916
when using airport KIND to predict weather in KDAL 1 day later
The 2 largest correlation is:
0.529957795361
when using airport KIND to predict weather in KBOS 1 day later
The 3 largest correlation is:
0.524734629994
when using airport KIND to predict weather in KHOU 1 day later
The 4 largest correlation is:
0.521361112712
when using airport KMDW to predict weather in KBOS 1 day later
The 5 largest correlation is:
0.516732157784
when using airport KMDW to predict weather in KHOU 1 day later
The 6 largest correlation is:
0.514944155818
when using airport KMDW to predict weather in KDAL 1 day later
The 7 largest correlation is:
0.513490580788
when using airport KMCI to predict weather in KCLT 1 day later
The 8 largest correlation is:
0.503080871196
when using airport KSTL to predict weather in KPHX 1 day later
The 9 largest correlation is:
0.501703229225
when using airport KMCI to predict weather in KIAH 1 day later
The 10 largest correlation is:
0.491398038982
when using airport KDTW to predict weather in KLAX 1 day later
The 10 highest 3 day offset temp change correlations are:
The 1 largest correlation is:
0.144302387178
when using airport KSNA to predict weather in KATL 3 days later
The 2 largest correlation is:
0.140377142764
when using airport KSNA to predict weather in KCVG 3 days later
The 3 largest correlation is:
0.137528904749
when using airport KLAX to predict weather in KATL 3 days later
The 4 largest correlation is:
0.133249463649
when using airport KSNA to predict weather in KDEN 3 days later
The 5 largest correlation is:
0.12910691896
when using airport KLAX to predict weather in KCVG 3 days later
The 6 largest correlation is:
0.124510688808
when using airport KSAN to predict weather in KATL 3 days later
The 7 largest correlation is:
0.124239394043
when using airport KSNA to predict weather in KSAN 3 days later
The 8 largest correlation is:
0.122878086535
when using airport KSLC to predict weather in KDFW 3 days later
The 9 largest correlation is:
0.12026096101
when using airport KLAX to predict weather in KDEN 3 days later
The 10 largest correlation is:
0.119288650927
when using airport KSAN to predict weather in KCVG 3 days later
The 10 highest 7 day offset temp change correlations are:
The 1 largest correlation is:
0.0815375750536
when using airport KSLC to predict  weather in KTPA 7 days later
The 2 largest correlation is:
0.0672571736639
when using airport KLAS to predict  weather in KCLE 7 days later
The 3 largest correlation is:
0.0653934301153
when using airport KPHX to predict  weather in KBNA 7 days later
The 4 largest correlation is:
0.0643772704246
when using airport TJSJ to predict  weather in KTPA 7 days later
The 5 largest correlation is:
0.0639875698221
when using airport KDTW to predict  weather in KTPA 7 days later
The 6 largest correlation is:
0.0617043818986
when using airport KMCO to predict  weather in KLAS 7 days later
The 7 largest correlation is:
0.0606120258766
when using airport KCLT to predict  weather in KDTW 7 days later
The 8 largest correlation is:
0.0598487602977
when using airport KMCO to predict  weather in KSMF 7 days later
The 9 largest correlation is:
0.0581983361845
when using airport KBOS to predict  weather in KORD 7 days later
The 10 largest correlation is:
0.057624690804
when using airport PHNL to predict  weather in KSMF 7 days later
The 10 highest 1 day offset cloud cover change correlations are:
The 1 largest correlation is:
0.432460707387
when using airport KMDW to predict  cloud cover change in KPHX 1 day later
The 2 largest correlation is:
0.404682869861
when using airport KSTL to predict  cloud cover change in KHOU 1 day later
The 3 largest correlation is:
0.401100985785
when using airport KMDW to predict  cloud cover change in KBOS 1 day later
The 4 largest correlation is:
0.400982905985
when using airport KMDW to predict  cloud cover change in KHOU 1 day later
The 5 largest correlation is:
0.398362579886
when using airport KMCI to predict  cloud cover change in KCLT 1 day later
The 6 largest correlation is:
0.397336232987
when using airport KMDW to predict  cloud cover change in KDTW 1 day later
The 7 largest correlation is:
0.39627705305
when using airport KSTL to predict  cloud cover change in KDAL 1 day later
The 8 largest correlation is:
0.395516704451
when using airport KMEM to predict  cloud cover change in KPIT 1 day later
The 9 largest correlation is:
0.394423332794
when using airport KSTL to predict  cloud cover change in KBOS 1 day later
The 10 largest correlation is:
0.393210595873
when using airport KIAH to predict  cloud cover change in TJSJ 1 day later
The 10 highest 3 day offset cloud cover change correlations are:
The 1 largest correlation is:
0.106356927197
when using airport KSFO to predict  cloud cover change in KFLL 3 days later
The 2 largest correlation is:
0.103085096078
when using airport KSFO to predict  cloud cover change in KIAD 3 days later
The 3 largest correlation is:
0.102637655271
when using airport KOAK to predict  cloud cover change in KFLL 3 days later
The 4 largest correlation is:
0.0976195307687
when using airport KOAK to predict  cloud cover change in KIAD 3 days later
The 5 largest correlation is:
0.0960983031184
when using airport KSFO to predict  cloud cover change in KATL 3 days later
The 6 largest correlation is:
0.095473172398
when using airport KLAS to predict  cloud cover change in KPIT 3 days later
The 7 largest correlation is:
0.094606914637
when using airport KSMF to predict  cloud cover change in KFLL 3 days later
The 8 largest correlation is:
0.0936576684611
when using airport KSEA to predict  cloud cover change in KSAN 3 days later
The 9 largest correlation is:
0.0919189929688
when using airport KSFO to predict  cloud cover change in KMKE 3 days later
The 10 largest correlation is:
0.0868677155523
when using airport KSMF to predict  cloud cover change in KCLE 3 days later
The 10 highest 7 day offset cloud cover change correlations are:
The 1 largest correlation is:
0.0832026746595
when using airport KFLL to predict  cloud cover change in KMEM 7 days later
The 2 largest correlation is:
0.0791672828946
when using airport KBOS to predict  cloud cover change in KIAH 7 days later
The 3 largest correlation is:
0.0767037618294
when using airport KBWI to predict  cloud cover change in KMSY 7 days later
The 4 largest correlation is:
0.07253589158
when using airport KBOS to predict  cloud cover change in KSNA 7 days later
The 5 largest correlation is:
0.0721257215583
when using airport KMEM to predict  cloud cover change in KTPA 7 days later
The 6 largest correlation is:
0.0719712552117
when using airport KDCA to predict  cloud cover change in KMSY 7 days later
The 7 largest correlation is:
0.0698158588822
when using airport TJSJ to predict  cloud cover change in PHNL 7 days later
The 8 largest correlation is:
0.0695595644805
when using airport KPIT to predict  cloud cover change in KCLT 7 days later
The 9 largest correlation is:
0.0677773249586
when using airport KFLL to predict  cloud cover change in KEWR 7 days later
The 10 largest correlation is:
0.066992755927
when using airport KBOS to predict  cloud cover change in KSEA 7 days later