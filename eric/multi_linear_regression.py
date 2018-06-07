import numpy as np
from scipy import stats
import pandas as pd
import os
import matplotlib.pyplot as plt
# import geoip2.database
#
plt.clf()

DATA_ROOT = '../data'
CSV_FILE_NAME = 'locn-filtered' + '.csv'
CSV_PATH = '/home/eric/Documents/ubc_workshop/pims-bcdata18-cloudpbx/data/'
CSV_FILE_PATH = os.path.join(DATA_ROOT, CSV_PATH + CSV_FILE_NAME)
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

df = pd.read_csv(CSV_FILE_PATH, parse_dates=['calldate', 'callend'],sep='\t')
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

avg_pkt_loss= (sum_pkt_loss_a + sum_pkt_loss_b)/2
# avg_pkt_loss = optional b/c 0's can be in either row for the same thing

xi = df[['delay_sum','a_maxjitter','b_maxjitter','a_mos_adapt_mult10',\
       'b_mos_adapt_mult10', 'a_mos_f1_mult10', \
       'a_mos_f2_mult10', 'b_mos_f1_mult10', 'b_mos_f2_mult10']].values
x = np.zeros((xi.shape[0], xi.shape[1]+1))
x[:,:-1] = xi
x[:,-1] = np.ones(xi.shape[0])

y = sum_pkt_loss_a.values
m= np.linalg.lstsq(x,y)
yfit = x.dot(m[0])
print (yfit.shape, y.shape, m[0].shape, x.shape)
i = range(len(y))
print(m[0])
plt.plot(i,y,'ro')
plt.plot(i,yfit,':')
plt.show()

