import streamlit as st
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point,Polygon
from mpl_toolkits.axes_grid1 import make_axes_locatable
pd.options.display.max_rows = 999
pd.options.display.max_columns = 999

def data_load() : 
    data_1 = pd.read_excel('Rasio Angka Partisipasi Kasar (APK) Perempuan_Laki-Laki di Tingkat Perguruan Tinggi Menurut Provinsi.xlsx',engine='openpyxl')


    data_1.dropna(inplace=True)


    maps_point = pd.read_json(r'maps.json')


    data_1.drop(35,axis=0,inplace=True)
    province_name = [x for x in data_1['Provinsi']]

    maps_point['Provinsi'] = province_name


    data_1.rename(columns={'Rasio Angka Partisipasi Kasar (APK) Perempuan/Laki-Laki di Tingkat Perguruan Tinggi Menurut Provinsi':'2020',
    'Unnamed: 2':'2019','Unnamed: 3':'2018'},inplace=True)


    data_2  = pd.read_excel(r'Rasio Angka Partisipasi Kasar (APK) Perempuan_Laki-Laki di Tingkat Perguruan Tinggi Menurut Provinsi_2015.xlsx',engine='openpyxl')
    data_2.dropna(inplace=True)

    data_2.rename(columns={'Rasio Angka Partisipasi Kasar (APK) Perempuan/Laki-Laki di Tingkat Perguruan Tinggi Menurut Provinsi':'2017',
    'Unnamed: 2':'2016','Unnamed: 3':'2015'},inplace=True)


    data_merge = pd.merge(data_1,data_2,on='Provinsi')



    data_location = pd.merge(data_merge,maps_point,on='Provinsi')

    data_location.drop(['id','name', 'alt_name'],axis=1,inplace=True)


    #visualizing using matplotlib 
    loc_df = gpd.GeoDataFrame(data_location,geometry=gpd.points_from_xy(data_location.longitude,data_location.latitude))



    #reading shapely file 

    indonesia = gpd.read_file(r'INDONESIA_PROP.shp')



    crs = {'init':'epsg:4326'}
    data = gpd.GeoDataFrame(loc_df)
    indo = gpd.GeoDataFrame(indonesia)

    return data,indo
def plot(option,data,indo,size) : 

    fig,ax = plt.subplots()
    plt.title('Angka Partisipasi Kasar Laki dan Perempuan di PT tahun {}'.format(str(option)),fontfamily='oswald',fontsize=15)
    # divider = make_axes_locatable(ax)
    # cax = divider.append_axes('right', size='5%',pad=0.1,sharex=data[str(option)])
    #creating colorbar
    

    indo.boundary.plot(ax=ax,color='DarkSlateBlue')
    data_plot = data.plot(cmap='Greens',column='{}'.format(str(option)),legend=False,ax=ax,s=size,alpha=0.7)
    # cbar = ax.figure.colorbar(np.array(data[f'{option}']),ax=ax)
    array_ = np.array([x for x in data[f'{option}']])
   
    st.pyplot(fig)
if __name__ == '__main__': 
    
    '''Gender Participation in Higher Education by Year (data source : Statistics Agency of Indonesia)'''
    
    option = st.selectbox('Please Choose Year',[2020,2019,2018,2017,2016,2015])
    'you selected',option
    data,indo = data_load()
    plot_size = st.slider('Adjust the size of the cloropleth',min_value=50,max_value=2000,step=100)
    plot(option,data,indo,plot_size)


