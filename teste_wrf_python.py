#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 18:23:16 2019

@author: lucas
"""

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

dataset = Dataset('/home/lucas/Downloads/wrf_ensemble_m1_d02_2019070718.nc')

lats = dataset.variables['lat'][:]  # extract/copy the data
lons = dataset.variables['lon'][:]
time = dataset.variables['time'][:]
air = dataset.variables['t2'][:]  # shape is time, lat, lon as shown above

#quanod longitude for maior que 180 devemos diminuir 360! if (lons > 180):
lons = lons-360

print(time.shape)# mostra quantas rodadas tem. Vai aparecer 49 para esse file!

arr = air[int(time[0])] # 0 para o tempo/rodada inicial! se for a rodada depois da inicial poem 1 e assim por diante

arr = arr[0,:,:] #Aqui vai zero simplesmente pq o python pede :)

margin = 2 # buffer to add to the range
lat_min = -29.5#min(lat) - margin
lat_max = -25.8#max(lat) + margin
lon_min = -54.5#min(lon) - margin
lon_max = -48#max(lon) + margin

# create map using BASEMAP
m = Basemap(llcrnrlon=lon_min,
            llcrnrlat=lat_min,
            urcrnrlon=lon_max,
            urcrnrlat=lat_max,
            lat_0=(lat_max - lat_min)/2,
            lon_0=(lon_max-lon_min)/2,
            projection='merc',
            resolution = 'h')
m.drawcoastlines()
m.drawcountries()
m.drawstates()
m.drawmapboundary(fill_color='#46bcec') #comentar linha caso queira apenas os dados do continente 
#m.fillcontinents(color = 'white',lake_color='#46bcec')
# Because our lon and lat variables are 1D,
# use meshgrid to create 2D arrays
# Not necessary if coordinates are already in 2D arrays.
lon, lat = np.meshgrid(lons, lats)
xi, yi = m(lon, lat)

# Plot Data
cs = m.pcolor(xi,yi,np.squeeze(arr))
cbar = m.colorbar(cs, location='bottom', pad="10%")
cbar.set_label('$ºC$')

# Add Title
plt.title('Temperature')
plt.savefig('/home/lucas/teste.jpg',dpi=300) # mudar local de save para funcionar no teu.
plt.show()