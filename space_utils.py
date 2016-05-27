import numpy as np
from math import ceil
from geopy.distance import vincenty, VincentyDistance
import geopy


def get_coordinates(data):
	geo_data = data['payload']['geo']
	if geo_data:
		return geo_data['coordinates']
	else:
		bbox = data['payload']['place']['bounding_box']['coordinates'][0]
		return list(np.array(bbox).mean(0)[::-1])


def grid(df, epsilon):
    latMIN = df.lat.min() # bottom
    latMAX = df.lat.max() # top
    lngMIN = df.lng.min() # left
    lngMAX = df.lng.max() # right
    H = vincenty((latMIN, lngMIN), (latMAX, lngMIN)).kilometers
    m = int(ceil(H / epsilon))
    W = vincenty((latMIN, lngMIN), (latMIN, lngMAX)).kilometers
    n = int(ceil(W / epsilon))
    lats = np.zeros(m)
    lngs = np.zeros(n)
    lats[0] = latMIN
    lngs[0] = lngMIN
    for i in xrange(1, m):
        start = geopy.Point((lats[i-1], lngMIN))
        d = geopy.distance.VincentyDistance(kilometers = epsilon)
        lats[i] = d.destination(point=start, bearing=0).latitude
        
    for i in xrange(1, n):
        start = geopy.Point((latMIN, lngs[i-1]))
        d = geopy.distance.VincentyDistance(kilometers = epsilon)
        lngs[i] = d.destination(point=start, bearing=1).longitude
    return lats, lngs


def construct_grid(df, epsilon):
    lats, lngs = grid(df, epsilon)
    m = lats.shape[0]
    n = lngs.shape[0]
    grid_dict = {}
    for i in xrange(m-1):
        latMIN = lats[i]
        latMAX = lats[i+1]
        for j in xrange(n-1):
            k = i*n + j
            lngMIN = lngs[j]
            lngMAX = lngs[j+1]
            ids = df.loc[(df.lat >= latMIN) & (df.lat < latMAX) & (df.lng >= lngMIN) & (df.lng < lngMAX)].index.values
            ids = list(ids)
            grid_dict[k] = ids
        k = n*(i+1)-1
        ids = df.loc[(df.lat >= latMIN) & (df.lat < latMAX) & (df.lng >= lngMIN)].index.values
        ids = list(ids)
        grid_dict[k] = ids
    latMIN = lats[m-1]
    for j in xrange(n-1):
        k = (m-1)*n + j
        lngMIN = lngs[j]
        lngMAX = lngs[j+1]
        ids = df.loc[(df.lat >= latMIN) & (df.lng >= lngMIN) & (df.lng < lngMAX)].index.values
        ids = list(ids)
        grid_dict[k] = ids
    k = n*m - 1
    lngMIN = lngs[n-1]
    ids = df.loc[(df.lat >= latMIN) & (df.lng >= lngMIN)].index.values
    ids = list(ids)
    grid_dict[k] = ids
    
    return grid_dict, (m, n)

# -----------------------------------------------------------------------------------------------------------------------
def find_neighbors(cell_id, grid_cols):
    neighbor_cells = []
    row = cell_id / grid_cols
    col = cell_id % grid_cols

    if row > 0:
        neighbor_cells.append(cell_id - grid_cols)
        neighbor_cells.append(cell_id - grid_cols + 1)

    if col > 0:
        neighbor_cells.append(cell_id-1)
        if row > 0:
            neighbor_cells.append(cell_id - grid_cols - 1)

    return neighbor_cells