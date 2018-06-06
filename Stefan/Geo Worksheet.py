
# coding: utf-8

# In[4]:


import numpy as np
import pandas as pd
import geoip2.database
import ipaddress
import os


# In[20]:


CSV_FILE_PATH = os.path.join('locn-filtered.csv')
GEOLITE_ASN_PATH = os.path.join('GeoLite2-ASN.mmdb')
GEOLITE_CITY_PATH = os.path.join('GeoLite2-City.mmdb')


# In[27]:


# read dataframe
df = pd.read_csv(CSV_FILE_PATH)


# ## Link IP addresses to ASN

# In[34]:


# initiate geoip client
readerASN = geoip2.database.Reader(GEOLITE_ASN_PATH)
readerCITY = geoip2.database.Reader(GEOLITE_CITY_PATH)


# In[35]:


# functions to get AS info
def getASobject(x):
    return readerASN.asn(str(ipaddress.ip_address(x)))
def getCityobject(x):
    return readerASN.asn(str(ipaddress.ip_address(x)))
def getASN(x):
    return x.autonomous_system_number
def getASorg(x):
    return x.autonomous_system_organization
def getInt(x):
    return int(x)


# In[36]:


# making a vector of AS objects for sipcaller
V = df['sipcallerip'].apply(getASobject)
# adding columns to the data frame
df['sipcallerasn'] = V.apply(getASN)
df['sipcallerasorg'] = V.apply(getASorg)


# In[54]:


# making a vector of AS objects for sipcalled
V = df['sipcalledip'].apply(getASobject)
# adding columns to the data frame
df['sipcalledasn'] = V.apply(getASN)
df['sipcalledasorg'] = V.apply(getASorg)


# In[55]:


# making a vector of AS objects for a_saddr
V = df['a_saddr'].apply(getInt).apply(getASobject)
# adding columns to the data frame
df['a_saddr_asn'] = V.apply(getASN)
df['a_saddr_asorg'] = V.apply(getASorg)


# In[56]:


# making a vector of AS objects for b_saddr
V = df['b_saddr'].apply(getInt).apply(getASobject)
# adding columns to the data frame
df['b_saddr_asn'] = V.apply(getASN)
df['b_saddr_asorg'] = V.apply(getASorg)


# In[58]:


df.to_csv('locn-filtered.csv')

