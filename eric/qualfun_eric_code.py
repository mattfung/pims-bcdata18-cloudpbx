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
from sklearn.metrics import *

# import geoip2.database

def evaluaterow(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, delay_sum, connect_duration):

    calc_sum = get_sum(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10)

    final_sum = (delay_sum + calc_sum)/(connect_duration*1000)

    return final_sum


def get_sum(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10):
    top_sum = 0
    n = 1
    w1 = 1
    w2 = 2
    w3 = 3
    w4 = 4
    w5 = 5
    w6 = 6
    w7 = 7
    w8 = 8
    w9 = 9
    w10 = 10

    top_sum += 20 * n * (a1) * (w1 - 1)
    n += 1
    top_sum += 20 * n * (a2) * (w2 - 1)
    n += 1
    top_sum += 20 * n * (a3) * (w3 - 1)
    n += 1
    top_sum += 20 * n * (a4) * (w4 - 1)
    n += 1
    top_sum += 20 * n * (a5) * (w5 - 1)
    n += 1
    top_sum += 20 * n * (a6) * (w6 - 1)
    n += 1
    top_sum += 20 * n * (a7) * (w7 - 1)
    n += 1
    top_sum += 20 * n * (a8) * (w8 - 1)
    n += 1
    top_sum += 20 * n * (a9) * (w9 - 1)
    n += 1
    top_sum += 20 * n * (a10) * (w10 - 1)

    return (top_sum)


#df = df.assign(qualfun=df_qualfun)
#df.compute()
#dfqf = df_qualfun.compute()

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

df.dropna(axis=1, how='all', inplace=True)
df = df.loc[:, ~(df == 'sanitized').all(axis=0)]
df.drop(columns=[col for col in df.columns if 'reverse' in col], inplace=True)
df['duration_td'] = df.callend - df.calldate
df_dens = df.dropna(axis=0, thresh = 79)
df = df[ df.connect_duration > 0 ]
df = df[ df.a_saddr > 0 ] 
df = df[ df.b_saddr > 0 ]

sum_pkt_loss_a =  df['a_sl1'] + df['a_sl2'] + df['a_sl3'] +\
      df['a_sl4'] + df['a_sl5'] + df['a_sl6'] + df['a_sl7'] + \
      df['a_sl8'] + df['a_sl9'] + df['a_sl10'] 

sum_pkt_loss_b =  df['b_sl1'] + df['b_sl2'] + df['b_sl3'] +\
      df['b_sl4'] + df['b_sl5'] + df['b_sl6'] + df['b_sl7'] + \
      df['b_sl8'] + df['b_sl9'] + df['b_sl10'] 

##qualfun for a
df['qualfun_a'] = df.apply(lambda df2: pd.Series(evaluaterow(df2['a_sl1'],df2['a_sl2'],df2['a_sl3'],df2['a_sl4'],df2['a_sl5'],df2['a_sl6'],df2['a_sl7'],df2['a_sl8'],df2['a_sl9'],df2['a_sl10'],df2['a_delay_sum'],df2['connect_duration'])),axis=1)
 #qualfun for a
df['qualfun_b'] = df.apply(lambda df2: pd.Series(evaluaterow(df2['b_sl1'],df2['b_sl2'],df2['b_sl3'],df2['b_sl4'],df2['b_sl5'],df2['b_sl6'],df2['b_sl7'],df2['b_sl8'],df2['b_sl9'],df2['b_sl10'],df2['b_delay_sum'],df2['connect_duration'])),axis=1)


####### Multi-Linear Regression W/ Packet Loss & Qualfun Version (A)

xi2_a = df[['delay_sum','a_maxjitter', 'qualfun_a']].values
x2_a = np.zeros((xi2_a.shape[0], xi2_a.shape[1]+1))
x2_a[:,:-1] = xi2_a
x2_a[:,-1] = np.ones(xi2_a.shape[0])

fig4 = plt.figure(4)
y2 = sum_pkt_loss_a.values
m2 = np.linalg.lstsq(x2_a,y2)
yfit2 = x2_a.dot(m2[0])
print (yfit2.shape, y2.shape, m2[0].shape, x2_a.shape)
i = range(len(y2))
print(m2[0])
plt.plot(i,y2,'ro')
plt.plot(i,yfit2,':')
plt.xlabel('Data Points Numbers')
plt.ylabel('Regression')
plt.title('Multi-Linear Regression w/ packet loss, MaxJitter A & Qualfun Version (A)')
reg_score = np.corrcoef(y2, yfit2)[0, 1]**2
print('Regression Score for MaxJitter A, Packet Loss & Qualfun Version A',reg_score)
fig4.show()
# plt.show()

####### Multi-Linear Regression W/ Packet Loss & Qualfun Version (B)

xi2_b = df[['delay_sum','b_maxjitter', 'qualfun_b']].values
x2_b = np.zeros((xi2_b.shape[0], xi2_b.shape[1]+1))
x2_b[:,:-1] = xi2_b
x2_b[:,-1] = np.ones(xi2_b.shape[0])


fig5 = plt.figure(5)
y3 = sum_pkt_loss_b.values
m3 = np.linalg.lstsq(x2_b,y3)
yfit3 = x2_b.dot(m3[0])
print (yfit3.shape, y3.shape, m3[0].shape, x2_b.shape)
i0 = range(len(y3))
print(m3[0])
plt.plot(i, y3, 'ro')
plt.plot(i,yfit3,':')
plt.title('Multi-Linear Regression w/ packet loss, MaxJitter B & Qualfun Version (B)')
plt.xlabel('Data Points Numbers')
plt.ylabel('Regression')
reg_score = np.corrcoef(y3, yfit3)[0, 1]**2
print('Regression Score for MaxJitter A, Packet Loss & Qualfun Version A',reg_score)
fig5.show()
# plt.show()

###### Histogram part A
fig6 = plt.figure(6)

qual_a = [ df['qualfun_a'] ]
# qualbins_hist_a = np.arange(df['b_maxjitter'].min(),df['b_maxjitter'].idxmax())

hist_labels = ['qualfun_a']
plt.hist(qual_a, alpha=1, label= hist_labels)
plt.legend(loc='upper left')
plt.grid(True)


plt.xlabel('MOS Scores')
plt.ylabel('Frequency')
plt.title('Histogram w/ Qualfun A')
fig6.show()
 

fig7 = plt.figure(7)
qual_b = [ df['qualfun_b'] ]
# qualbins_hist_b = np.arange(df['b_maxjitter'].min(),df['delay_sum'].idxmax())

hist_labels = ['b_maxjitter']
plt.hist(qual_a, alpha=1, label= hist_labels)
plt.legend(loc='upper left')
plt.grid(True)

plt.xlabel('Qualfun Scores')
plt.ylabel('Frequency')
plt.title('Histogram w/ Qualfun B')
fig7.show()

plt.show()
