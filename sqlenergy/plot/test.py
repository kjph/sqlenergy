import csv
import matplotlib.pyplot as plt

def load_time_series(loc):
	"""
	load time series from the output csv file
	"""
	pass

def plot_time_series(Series, **kwargs):
	"""
	plot_time_series
	"""

	#Make sure everything is ordered
	Series.fill_time_series()

	plt.figure()

	for stype in Series.all_types:
		x, y = Series.time_value_map[stype].iteritems()
		plt.plot(x,y)

	plt.show()
