# -*- coding: utf-8 -*-
"""
       Created on Tue Jun  5 09:21:13 2018
       @author: Conor Morrison
       @Edited by : Eric lam
"""

import numpy as np
import pandas as pd
import os
# import dask.dataframe as dd
import matplotlib.pyplot as plt
# import geoip2.database


DATA_ROOT = '../data'
# CSV_FILE_NAME = 'pims_cloudpbx_subset_201806051550_1million' + '.csv'
CSV_FILE_NAME = '127.0.0.1-2018-05-2018-3-58 PM- voipmonitor-cdr' +'.csv'
CSV_PATH = '/home/eric/Documents/ubc_workshop/pims-bcdata18-cloudpbx/data/'
# CSV_PATH = '/home/eric/Documents/'
CSV_FILE_PATH = os.path.join(CSV_PATH + CSV_FILE_NAME)
# GEOLITE_DB_PATH = os.path.join(DATA_ROOT,'GeoLite2-City.mmdb')

DESCRIBED_COLUMNS = ["ID","calldate", "callend", "duration", "connect_duration", "progress_time", 
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
df = df.loc[:, ~(df == 'sanitized').all(axis=0)]
# ## sighup was removed by the DESCRIBED_COLUMNS subsetting
# XX sighup column is entirely zeros. remove it. 
# XX df.drop(columns=['sighup'], inplace=True) 
# create a version of duration column of type timedelta
df.drop(columns=[col for col in df.columns if 'reverse' in col], inplace=True)
df['duration_td'] = df.callend - df.calldate

# a dataframe where the rows have been removed if 
# there are more than 60% NA values in those rows.
df_dens = df.dropna(axis=0, thresh = 79)

# df.dropna(subset=['a_saddr', 'b_saddr'])
df = df[ df.connect_duration > 0 ]
df = df[ df.a_saddr > 0 ] 
df = df[ df.b_saddr > 0 ]
'''
We do > 0 because of the possibility of hackers just hanging up at 0:00:00 
time of the call. Having != 0 just dirties out data because it adds
the hacker data
'''

mindurcalls=df
mindurcalls['connect_duration'].fillna(value=0, inplace=True)

mindurcalls = mindurcalls[~pd.isnull(mindurcalls['connect_duration'])]

binwidth = 5
bins_hist = range(0, 45 + binwidth, binwidth)


fig1 = plt.figure(1)

mos_a1 = mindurcalls['a_mos_f1_mult10'].fillna(0)
mos_a2 = mindurcalls['a_mos_f2_mult10'].fillna(0)
mos_adapt_a = mindurcalls['a_mos_adapt_mult10'].fillna(0)

hist_data = [mos_a1, mos_a2, mos_adapt_a]
hist_labels = ['a_mos_f1_mult10','a_mos_f2_mult10','a_mos_adapt_mult10']
plt.hist(hist_data, bins_hist, alpha=1, label= hist_labels)
plt.legend(loc='upper left')
plt.grid(True)
plt.axis([0, 45, 0, 6000],'scaled')
plt.xlabel('MOS Scores')
plt.ylabel('Frequency')
fig1.show()

##########################################################################################
fig2 = plt.figure(2)

mos_b1 = mindurcalls['b_mos_f1_mult10'].fillna(0)
mos_b2 = mindurcalls['b_mos_f2_mult10'].fillna(0)
mos_adapt_b = mindurcalls['b_mos_adapt_mult10'].fillna(0)

hist_data = [mos_b1, mos_b2, mos_adapt_b]
hist_labels = ['b_mos_f1_mult10','b_mos_f2_mult10','b_mos_adapt_mult10']
plt.hist(hist_data, bins_hist, alpha=1, label= hist_labels)
plt.legend(loc='upper left')
plt.grid(True)
plt.axis([0, 45, 0, 10000])
plt.xlabel('MOS Scores')
plt.ylabel('Frequency')
fig2.show()

plt.show()


