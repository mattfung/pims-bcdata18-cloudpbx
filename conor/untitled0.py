# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 09:21:13 2018

@author: Conor Morrison
"""

import pandas as pd
import os
import geoip2.database
import matplotlib.pyplot as plt

DATA_ROOT = '../data'
CSV_FILE_PATH = os.path.join(DATA_ROOT,'127.0.0.1-2018-05-2018-3-58 PM- voipmonitor-cdr.csv')
GEOLITE_DB_PATH = os.path.join(DATA_ROOT,'GeoLite2-City.mmdb')

DESCRIBED_COLUMNS = ["calldate", "callend", "duration", "connect_duration", "progress_time", 
                     "first_rtp_time", "caller", "caller_domain", "caller_reverse", "callername", 
                     "callername_reverse", "called", "called_domain", "called_reverse", "sipcallerip", 
                     "sipcallerport", "sipcalledip", "sipcalledport", "whohanged", "lastSIPresponse_id", 
                     "dscp", "a_payload", "b_payload", "a_saddr", "b_saddr", "a_received", "b_received", 
                     "a_lost", "b_lost", "a_ua_id", "b_ua_id", "a_avgjitter_mult10", "b_avgjitter_mult10",
                     "a_maxjitter", "b_maxjitter", "a_sl1", "a_sl2", "a_sl3", "a_sl4", "a_sl5", "a_sl6", 
                     "a_sl7", "a_sl8", "a_sl9", "a_sl10", "a_d50", "a_d70", "a_d90", "a_d120", "a_d150", 
                     "a_d200", "a_d300", "b_sl1", "b_sl2", "b_sl3", "b_sl4", "b_sl5", "b_sl6", "b_sl7", 
                     "b_sl8", "b_sl9", "b_sl10", "b_d50", "b_d70", "b_d90", "b_d120", "b_d150", "b_d200", 
                     "b_d300", "a_mos_f1_mult10", "a_mos_f2_mult10", "a_mos_adapt_mult10", 
                     "b_mos_f1_mult10", "b_mos_f2_mult10", "b_mos_adapt_mult10", "a_rtcp_loss", 
                     "a_rtcp_maxfr", "a_rtcp_avgfr_mult10", "a_rtcp_maxjitter", "a_rtcp_avgjitter_mult10", 
                     "b_rtcp_loss", "b_rtcp_maxfr", "b_rtcp_avgfr_mult10", "b_rtcp_maxjitter", 
                     "b_rtcp_avgjitter_mult10", "packet_loss_perc_mult1000", "a_packet_loss_perc_mult1000", 
                     "b_packet_loss_perc_mult1000", "delay_sum", "a_delay_sum", "b_delay_sum", 
                     "a_rtp_ptime", "b_rtp_ptime"]
                     
# read dataframe. calldate and callend are the only date columns
df = pd.read_csv(CSV_FILE_PATH, parse_dates=['calldate', 'callend'])

df = df[DESCRIBED_COLUMNS]
# remo`ve any columns that are entirely NA.
df.dropna(axis=1, how='all', inplace=True)
# some columns have "sanitized" written the whole way down:
#    remove these.
df=df.loc[:, ~(df == 'sanitized').all(axis=0)]
# ## sighup was removed by the DESCRIBED_COLUMNS subsetting
# XX sighup column is entirely zeros. remove it. 
# XX df.drop(columns=['sighup'], inplace=True) 
# create a version of duration column of type timedelta
df.drop(columns=[col for col in df.columns if 'reverse' in col], inplace=True)

df['duration_td'] = df.callend - df.calldate

# a dataframe where the rows have been removed if 
# there are more than 60% NA values in those rows.
df_dens = df.dropna(axis=0, thresh = 79)

only_ui_ids = df[pd.notnull(df['a_ua_id'])]
only_ui_ids = only_ui_ids[pd.notnull(only_ui_ids['b_ua_id'])]
only_ui_ids = only_ui_ids[only_ui_ids['a_ua_id']>0 & only_ui_ids['b_ua_id']>0]
only_ui_ids.count
df.count


#def evaluaterow(row):
#    
#    durarraya = [row['a_sl1'], row['a_sl2'], row['a_sl3'],
#                 row['a_sl4'], row['a_sl5'], row['a_sl6'],
#                 row['a_sl7'], row['a_sl8'], row['a_sl9'], row['a_sl10']]
#
#    durarrayb = [row['b_sl1'], row['b_sl2'], row['b_sl3'],
#                 row['b_sl4'], row['b_sl5'], row['b_sl6'],
#                 row['b_sl7'], row['b_sl8'], row['b_sl9'], row['b_sl10']]
#
#    sum = 0
#    
#    for n in range(1,11): #check incluseive or exclusive range want n in [0,10]
#        sum=sum+20*n*(durarraya[n]+durarrayb[n])
#    return (sum+row['delay_sum'])/(2*row['connect_duration'])
    
    
    



#a_mos_f1_mult10quals = [df[a_mos_f1_mult10]<30 30<=df[a_mos_f1_mult10]<3.5]
#print(df['a_mos_f1_mult10'])
#df['a_mos_f1_mult10'].dropna(axis=0, how='any', inplace=False)
#array1=df['a_mos_f1_mult10'].dropna(axis=0, how='any', inplace=False)
#a_mos_f1_mult10=pd.cut(array1, [0, 30, 35, 40, 45], right=True, include_lowest=True)
#print(a_mos_f1_mult10)
#mindurcalls=df
#mindurcalls['connect_duration'].fillna(value=0, inplace=True)

#mindurcalls=mindurcalls[pd.isnull(mindurcalls['connect_duration'])]
#print(mindurcalls['duration'])
#mindurcalls=mindurcalls[mindurcalls['duration']>=3]
#print(mindurcalls['duration'])
#
#
#arraya1 = mindurcalls['a_mos_f1_mult10'].fillna(0)
#
#hist=arraya1.hist(bins=[0, 1, 30, 35, 40, 45])
#
#arrayb1 = mindurcalls['b_mos_f1_mult10'].fillna(0)
#hist=arrayb1.hist(bins=[0, 1, 30, 35, 40, 45])
#
#arraya2 = mindurcalls['a_mos_f2_mult10'].fillna(0)
#hist=arraya2.hist(bins=[0, 1, 30, 35, 40, 45])
#
#arrayb2 = mindurcalls['b_mos_f2_mult10'].fillna(0)
#hist=arrayb2.hist(bins=[0, 1, 30, 35, 40, 45])  #filter out calls with duration zero
#
#
#
