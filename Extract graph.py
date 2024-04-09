# Import libraries
import numpy as np
import pandas as pd

from pytrack.graph import graph, distance
from pytrack.analytics import visualization


df = pd.read_excel("dataset.xlsx")


latitude = df["latitude"].to_list()
longitude = df["longitude"].to_list()

points = [(lat, lon) for lat, lon in zip(latitude, longitude)]


# Create BBOX
north, east = np.max(np.array([*points]), 0)
south, west = np.min(np.array([*points]), 0)

# Extract road network graph
G = graph.graph_from_bbox(*distance.enlarge_bbox(north, south, west, east, 500), simplify=True, network_type='drive')

# Show extracted graph
maps = visualization.Map(location=(np.mean(latitude), np.mean(longitude)))
maps.add_graph(G, plot_nodes=True)
maps.show_in_browser()