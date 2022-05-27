#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 06:50:19 2022

@author: fagundlu
"""
import cartopy.crs as crs
import proplot as pplt
import salem
import xarray as xr
from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader

# Abertura do arquivo NetCDF.
ds = xr.open_dataset("C:/Users/User/Downloads/WRF_cpt_05KM_2022041300_2022041612.nc")

# Abertura do arquivo shapefile. O arquivo "BR_UF_2021.shp" será
# utilizado para mascarar os dados.
shp = salem.read_shapefile("C:/Users/User/Downloads/BR_UF_2021/BR_UF_2021.shp")

print(shp)  # Visualiza as informações do shapefile.

# O nome 'Santa Carina' que veio do comando "print(shp)".

# O estado a ser utilizado para mascarar o dado.
shp_SC = shp.loc[
    (shp["NM_UF"] == "Santa Catarina")]

fig, ax = pplt.subplots(proj="pcarree")

# Formatação do mapa.
ax.format(
    coast=False,
    borders=False,
    grid=False,
    latlim=(-30, -25.5),
    lonlim=(-54, -48),
    linewidth=0,
)

# Na linha abaixo o trecho "salem.roi(shape=shp_amazonia)" é
# responsável por aplicar a máscara no dado, isto é, mascara
# o dado apenas no domínio solicitado. A variável a
# ser utilizada para manipulação futura ou plot é a "prec_mask".
prec_mask = ds.TMP_2maboveground.salem.roi(shape=shp_SC)

# Plot da figura. Plota apenas o primeiro tempo.
ax.pcolormesh(ds.longitude, ds.latitude, prec_mask[0, :, :], cmap="Crest")

# Nome do arquivo shapefile que será utilizado para desenhar o contorno no mapa.
shape_SC = ShapelyFeature(
    Reader("C:/Users/User/Downloads/BR_UF_2021/BR_UF_2021.shp").geometries(),
    crs.PlateCarree(),
    facecolor="none",
)

# Adiciona o contorno do shapefile ao mapa de precipitação.
ax.add_feature(shape_SC, linewidth=1, edgecolor="black")

# Salva a figura.
fig.save("SC_temperatura.jpg", transparent=True, dpi=300, bbox_inches="tight", pad_inches=0.1)