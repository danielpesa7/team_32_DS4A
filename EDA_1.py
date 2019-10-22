#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import the libraries that we are going to use
import pandas as pd
import matplotlib.pyplot as plt
import time
#get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#Read geographic data as pandas dataframe
geographics = pd.read_csv('geographic.csv')


# In[3]:


#Initialize nta dictionary
nta_dictionary = {}
for nta in geographics.columns:
    nta_dictionary[nta] = ''


# In[4]:


#Create a dictionary for each NTA with longitude and latitude as values
for nta in nta_dictionary:
    latitude = []
    longitude = [] 
    for i in geographics.loc[:,nta].values:
        if i < 0:
            latitude.append(i)
        elif i > 0:
            longitude.append(i)
    nta_dictionary[nta] = [longitude,latitude]


# In[5]:


def nta_graph(nta):
    '''Function to graph the NTA on a scatterplot'''
    plt.scatter(nta_dictionary[nta][0],nta_dictionary[nta][1])
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()


# In[6]:


#Call nta_graph function with the desired NTA
#nta_graph('MN22')


# In[7]:


#Import shapely for polygons visualization
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


# In[8]:


#Create a dictionary with nta as key and its polygon as value
nta_dictionary_lat_lon = {}
for nta in nta_dictionary.keys():
    polygon = []
    for lat,lon in zip(nta_dictionary[nta][0],nta_dictionary[nta][1]):
        lat_lon_tuple = (lat,lon)
        polygon.append(lat_lon_tuple)
        nta_dictionary_lat_lon[nta] = polygon


# In[9]:


#Read Uber trips 2014 from csv file
uber_trips_2014 = pd.read_csv('uber_trips_2014.csv')


# In[10]:


#uber_trips_2014.head()


# In[16]:


#get_ipython().run_cell_magic('time', '', "
#Map every pickup point in every polygon to know where it fits
nta_serie = []
idx_dic = {}
i_list = [1100000,1200000,1300000,1400000,1500000]
#uber_trips_2014.shape[0]//10
for i in range(1000000,1500000):
    point = Point(uber_trips_2014['pickup_latitude'][i],uber_trips_2014['pickup_longitude'][i])
    if i in i_list:
        print('Fila {}'.format(i))
    for j in nta_dictionary_lat_lon.keys():
        polygon = Polygon(nta_dictionary_lat_lon[j])
        if polygon.contains(point):
            idx_dic[i] = j
            break
        else:
            pass


# In[17]:


#Create deep copy of Uber dataframe
df_test = uber_trips_2014.copy()


# In[18]:


#Add nta column
df_test['Nta'] = pd.Series(idx_dic)


# In[19]:


#Save the csv file
df_test.to_csv('uber_nta_1m_15m.csv')


# In[ ]:




