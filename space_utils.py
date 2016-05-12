import numpy as np


def get_coordinates(data):
	geo_data = data['payload']['geo']
	if geo_data:
		return geo_data['coordinates']
	else:
		bbox = data['payload']['place']['bounding_box']['coordinates'][0]
		return list(np.array(bbox).mean(0)[::-1])

