import pandas as pd
import geopandas as gpd
import numpy as np
import timeit
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
import json
# =============================================================================
# Functions
# =============================================================================
def inside(lista):
    try:
        if len(lista[0])==2 and str(lista[0][0])[:3] in set(['-73', '-74']):
            return [lista]
        else:
            return 'next_level'            
    except:
        return 'next_level'

def poly_info(poly, temp, geom, conte, sub_index=''):
    sub = '_'+str(sub_index)
    temp = temp.append(pd.DataFrame([list(item) for sublist in inside(poly) for item in sublist]))
    temp['Cod']=name+'_'+str(sub)
    temp['Bor']=boro
    geom = Polygon(zip(temp.loc[:,0],temp.loc[:,1]))
    conte.append([name+str(sub),geom])
    boroname.append(boro)
# =============================================================================
# Data
# =============================================================================
path = "C:\\Users\HP\Desktop\DS4A_workspace\Semana 1\Dataset\Dataset\\"

geografia = pd.read_csv(path+'geographic.csv')
demogr = pd.read_csv(path+'\\demographics.csv')
weather = pd.read_csv(path+'\\weather.csv')
zones = pd.read_csv(path+'\\zones.csv')

subway = pd.read_csv(path+'\\mta_trips.csv')
green = pd.read_csv(path+'\\green_trips_new_2.csv')
yellow = pd.read_csv(path+'\\yellow_trips_new.csv')
uber_2015 = pd.read_csv(path+'\\uber_trips_2015.csv')
uber_2014 = pd.read_csv(path+'\\uber_trips_2014.csv')

# =============================================================================
# NY map
# =============================================================================
conte = []
boroname = []
aux = pd.DataFrame()
for i in range(0,len(NY_nta.shapeRecords())):
    name = NY_nta.shapeRecords()[i].__geo_interface__['properties']['NTACode']
    boro = NY_nta.shapeRecords()[i].__geo_interface__['properties']['BoroName']
    coords = NY_nta.shapeRecords()[i].__geo_interface__['geometry']['coordinates']
    temp = pd.DataFrame()
    sub_1 = 0
    sub=0
    if len(coords)>1:
        for pol in coords:            
            if inside(pol)=='next_level':
                for island in pol:                    
                    if inside(island)=='next_level':
                        poly_info(island[0], temp, geom, conte, sub)
                    else:
                        poly_info(island, temp, geom, conte, sub)
                    sub=sub+1
            else:
                poly_info(pol, temp, geom, conte, sub_1)                
            sub_1=sub_1+1
    else:
        if inside(coords)=='next_level':
            poly_info(coords[0],temp, geom, conte)
        else:
            poly_info(coords, temp, geom, conte)
    aux = aux.append(temp)

NY_poly = gpd.GeoDataFrame(columns=['Nombre','Geometria'], data=conte, geometry='Geometria')
NY_poly.plot()
plt.scatter(yellow['pickup_longitude'][0],yellow['pickup_latitude'][0], color='red')
plt.scatter(yellow['pickup_longitude'][2],yellow['pickup_latitude'][2], color='red')

# =============================================================================
# Finding outside pick up points
# =============================================================================
start = timeit.timeit()
esta_NY = [sum(NY_poly.contains(Point(yellow['pickup_longitude'][a],yellow['pickup_latitude'][a])))!=0 for a in range(0,100000)]
end = timeit.timeit()
print(end - start)

fuera = yellow[['pickup_longitude','pickup_latitude']][0:100000][np.where(np.array(esta_NY)==0, True, False)]
NY_poly.plot()
plt.scatter(fuera['pickup_longitude'],fuera['pickup_latitude'], color='red')
