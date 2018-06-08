"""
       Created on Jun 7 2018
       @author: Eric Lam
       @Collaborated histogram w/ Conor Morrison
"""

import numpy as np
from scipy import stats
import pandas as pd
import os
import matplotlib.pyplot as plt
import julians_algorithm
from sklearn.metrics import *

# import geoip2.database
#
plt.clf()

# CSV_FILE_NAME = 'pims_cloudpbx_subset_201806051550_1million' + '.csv'
CSV_FILE_NAME = '127.0.0.1-2018-05-2018-3-58 PM- voipmonitor-cdr' +'.csv'
CSV_PATH = '/home/eric/Documents/ubc_workshop/pims-bcdata18-cloudpbx/data/'
# CSV_PATH = '/home/eric/Documents/'
CSV_FILE_PATH = os.path.join(CSV_PATH + CSV_FILE_NAME)
# GEOLITE_DB_PATH = os.path.join(DATA_ROOT,'GeoLite2-City.mmdb')

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

'''
       We do > 0 because of the possibility of hackers just hanging up at 0:00:00 
       time of the call. Having != 0 just dirties out data because it adds
       the hacker data
'''
'''
       # multi-linear regression
       # 
       # flatten packetloss into 1 number (Predictan)
       # decide on predictors ( delay_sum, jitter, mos)
       # mos -> could get a better predictor later from better results
'''

#### procure data -> Delay_Sum, Jitter, MOS
sum_pkt_loss_a =  df['a_sl1'] + df['a_sl2'] + df['a_sl3'] +\
      df['a_sl4'] + df['a_sl5'] + df['a_sl6'] + df['a_sl7'] + \
      df['a_sl8'] + df['a_sl9'] + df['a_sl10'] 

sum_pkt_loss_b =  df['b_sl1'] + df['b_sl2'] + df['b_sl3'] +\
      df['b_sl4'] + df['b_sl5'] + df['b_sl6'] + df['b_sl7'] + \
      df['b_sl8'] + df['b_sl9'] + df['b_sl10'] 
# avg_pkt_loss = optional b/c 0's can be in either row for the same thing

xi_a = df[['delay_sum','a_maxjitter','a_mos_adapt_mult10','a_mos_f1_mult10', 'a_mos_f2_mult10']].values
x_a = np.zeros((xi_a.shape[0], xi_a.shape[1]+1))
x_a[:,:-1] = xi_a
x_a[:,-1] = np.ones(xi_a.shape[0])

xi_b = df[['delay_sum','b_maxjitter','b_mos_adapt_mult10','b_mos_f1_mult10', 'b_mos_f2_mult10']].values
x_b = np.zeros((xi_b.shape[0], xi_b.shape[1]+1))
x_b[:,:-1] = xi_b
x_b[:,-1] = np.ones(xi_b.shape[0])

####### Multi-Linear Regression W/ Packet Loss (A) & MOS

fig1 = plt.figure(1)
y = sum_pkt_loss_a.values
m = np.linalg.lstsq(x_a,y)
yfit = x_a.dot(m[0])
# print (yfit.shape, y.shape, m[0].shape, x_a.shape)
i = range(len(y))
print(m[0])
plt.plot(i,y,'ro')
plt.plot(i,yfit,':')
plt.title('Multi-Linear Regression w/ Packet Loss & MOS Version (A)')
plt.xlabel('Data Points Numbers')
plt.ylabel('Regression')
fig1.show()
# print('x_a ',x_a,'\n y \n', y)
reg_score = np.corrcoef(y, yfit)[0, 1]**2
print('Regression Score of Packet Loss & Mos Version A', reg_score)

# plt.show()

####### Multi-Linear Regression W/ Packet Loss (B) & MOS
fig2 = plt.figure(2)
y0 = sum_pkt_loss_b.values
m0 = np.linalg.lstsq(x_b,y0)
yfit0 = x_b.dot(m0[0])
# print (yfit0.shape, y0.shape, m0[0].shape, x_b.shape)
i0 = range(len(y0))
print(m0[0])
plt.plot(i, y0, 'ro')
plt.plot(i,yfit0,':')
plt.title('Multi-Linear Regression w/ Packet Loss & MOS Version (B)')
plt.xlabel('Data Points Numbers')
plt.ylabel('Regression')
fig2.show()
reg_score0 = np.corrcoef(y0, yfit0)[0, 1]**2
print('Regression Score of Packet Loss & Mos Version B', reg_score0)
# plt.show()

#######################################################################

mindurcalls=df
mindurcalls['connect_duration'].fillna(value=0, inplace=True)
mindurcalls = mindurcalls[~pd.isnull(mindurcalls['connect_duration'])]
binwidth = 5
bins_hist = range(0, 45 + binwidth, binwidth)

###### Histogram part A
fig3 = plt.figure(3)

mos_a1 = mindurcalls['a_mos_f1_mult10'].fillna(0)
mos_a2 = mindurcalls['a_mos_f2_mult10'].fillna(0)
mos_adapt_a = mindurcalls['a_mos_adapt_mult10'].fillna(0)

hist_dataA = [mos_a1, mos_a2, mos_adapt_a]
hist_labels = ['a_mos_f1_mult10','a_mos_f2_mult10','a_mos_adapt_mult10']
plt.hist(hist_dataA, bins = bins_hist , alpha=1, label= hist_labels)
plt.legend(loc='upper left')
plt.grid(True)
plt.axis([0, 45, 0, 6000],'scaled')
plt.xlabel('MOS Scores')
plt.ylabel('Frequency')
plt.title('Histogram w/ MOS (A)')
fig3.show()


###### Histogram part B
fig4 = plt.figure(4)

mos_b1 = mindurcalls['b_mos_f1_mult10'].fillna(0)
mos_b2 = mindurcalls['b_mos_f2_mult10'].fillna(0)
mos_adapt_b = mindurcalls['b_mos_adapt_mult10'].fillna(0)

hist_dataB = [mos_b1, mos_b2, mos_adapt_b]
hist_labels = ['b_mos_f1_mult10','b_mos_f2_mult10','b_mos_adapt_mult10']
plt.hist(hist_dataB, bins_hist, alpha=1, label= hist_labels)
plt.legend(loc='upper left')
plt.grid(True)
plt.axis([0, 45, 0, 6000],'scaled')
plt.xlabel('MOS Scores')
plt.ylabel('Frequency')
plt.title('Histogram w/ MOS (B)')
fig4.show()

plt.show()

