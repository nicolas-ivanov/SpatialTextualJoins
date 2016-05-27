import numpy as np


def get_coordinates(data):
	geo_data = data['payload']['geo']
	if geo_data:
		return geo_data['coordinates']
	else:
		bbox = data['payload']['place']['bounding_box']['coordinates'][0]
		return list(np.array(bbox).mean(0)[::-1])


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