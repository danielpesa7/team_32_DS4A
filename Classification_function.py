import pandas as pd
import geopandas as gpd
import numpy as np
import timeit
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point
from shapely.ops import cascaded_union
import shapefile
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

def poly_info(poly, temp, name, conte, sub_index=''):
    sub = '_'+str(sub_index)
    temp = temp.append(pd.DataFrame([list(item) for sublist in inside(poly) for item in sublist]))
    geom = Polygon(zip(temp.loc[:,0],temp.loc[:,1]))
    conte.append([name+str(sub),geom])
    

def Ny_polyg(Ny_nta):
    conte = []
    aux = pd.DataFrame()
    for i in range(0,len(NY_nta.shapeRecords())):
        name = NY_nta.shapeRecords()[i].__geo_interface__['properties']['ntacode']
        coords = NY_nta.shapeRecords()[i].__geo_interface__['geometry']['coordinates']
        temp = pd.DataFrame()
        sub_1 = 0
        sub=0
        if len(coords)>1:
            for pol in coords:            
                if inside(pol)=='next_level':
                    for island in pol:                    
                        if inside(island)=='next_level':
                            poly_info(island[0], temp,name, conte, sub)
                        else:
                            poly_info(island, temp, name, conte, sub)
                        sub=sub+1
                else:
                    poly_info(pol, temp, name, conte, sub_1)                
                sub_1=sub_1+1
        else:
            if inside(coords)=='next_level':
                poly_info(coords[0],temp, name, conte)
            else:
                poly_info(coords, temp, name, conte)
        aux = aux.append(temp)
    return gpd.GeoDataFrame(columns=['Nombre','Geometria'], data=conte, geometry='Geometria')


def assign(transport, col_latitude, col_longitude, a, b , poly, path_export):
    NY_one = list(poly['Geometria'])
    NY_one = cascaded_union(NY_one)
    
    transport['NTA'] = np.nan
    esta_NY = [sum(poly.contains(Point(transport[col_longitude][a],transport[col_latitude][a])))!=0 for a in range(a,b)]
    
    fuera = transport[[col_longitude,col_latitude]][a:b][np.where(np.array(esta_NY)==0, True, False)]    
    outside_points = list(fuera.index)
    
    #Shortest distance from Point to NY polygon
    distances = [Point(transport[col_longitude][a],transport[col_latitude][a]).distance(NY_one) for a in outside_points]
    distances_df = pd.DataFrame(distances).rename(columns={0:'Dist'})
    
    #Drop pickup points out of NY in the middle of the sea
    sea_points = list(pd.DataFrame(outside_points)[distances_df['Dist']>=0.003][0])
    transport = transport[a:b].drop(sea_points)
        
    #Nta clasification for the outside nearest points
    close_enough = list(pd.DataFrame(outside_points)[distances_df['Dist']<0.003][0])
    close_nta = [int(pd.DataFrame([Point(transport[col_longitude][a],transport[col_latitude][a]).distance(nta) for nta in poly['Geometria']]).idxmin()) for a in close_enough]
    
    transport.loc[close_enough,'NTA'] = [a[:4] for a in list(poly.loc[close_nta,'Nombre'])]
    
    #Nta clasification for the remaining
    remaining = list(set(transport.index)-set(close_enough))
    transport.loc[remaining,'NTA'] = [list(poly[poly.contains(Point(transport[col_longitude][a],transport[col_latitude][a]))]['Nombre'])[0][:4] for a in remaining]
    
    transport.to_csv('C:\\Users\\lenovo\\Documents\\Github_Personal\\personal\\Datathon\\Dataset\Yellow2.csv')
    

path_shp = 'C:\\Users\lenovo\Documents\Github_Personal\personal\Datathon\\Neighborhood Tabulation Areas'    
NY_nta = shapefile.Reader(path_shp+'\\ny.shp')
Ny_poly = Ny_polyg(NY_nta)

path_dataset = 'C:\\Users\\lenovo\\Documents\\Github_Personal\\personal\\Datathon\Dataset'
nombre_dataset = '\\yellow_trips_new.csv'
transport = pd.read_csv(path_dataset+nombre_dataset)
col_longitude = 'pickup_longitude'
col_latitude = 'pickup_latitude'
path_export = 'C:\\Users\\lenovo\\Documents\\Github_Personal\\personal\\Datathon\\Dataset\Yellow3.csv'


assign(transport, col_latitude, col_longitude, 2000000,3000000,Ny_poly, path_export)

 


