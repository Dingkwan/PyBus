import numpy as np
from pytrack.graph import graph, distance
from pytrack.analytics import visualization
from pytrack.matching import candidate, mpmatching_utils, mpmatching
import os

def cleanCache():
    if os.path.exists("__pycache__"):
        rmtree("__pycache__")
    if os.path.exists("SV_panoramas"):
        rmtree("SV_panoramas")
    # if os.path.exists("route_map.html"):
    #     os.remove("route_map.html")

def routeMap(data, dir):
    cleanCache()
    latitude = data["latitude"].to_list()
    longitude = data["longitude"].to_list()

    points = [(lat, lon) for lat, lon in zip(latitude[:len(latitude)], longitude[:len(longitude)])]


    # Create BBOX
    north, east = np.max(np.array([*points]), 0)
    south, west = np.min(np.array([*points]), 0)

    # Extract road graph

    G = graph.graph_from_bbox(*distance.enlarge_bbox(north, south, west, east, 500), simplify=True, network_type='drive')


    # Initialize maps
    loc = (np.mean(latitude[:len(latitude)]), np.mean(longitude[:len(longitude)]))
    maps = visualization.Map(location=loc, zoom_start=15)


    # Show extracted graph
    maps.add_graph(G, plot_nodes=True)


    # Extract candidates
    G_interp, candidates = candidate.get_candidates(G, points, interp_dist=5, closest=True, radius=30)

    # Plot results
    maps.draw_candidates(candidates, 50)

    # Extract trellis DAG graph
    trellis = mpmatching_utils.create_trellis(candidates)

    # Perform the map-matching process
    path_prob, predecessor = mpmatching.viterbi_search(G_interp, trellis, "start", "target")

    # Plot map-matching results
    maps.draw_path(G_interp, trellis, predecessor)
    savePath = os.getcwd() + dir + '\\route_map.html'
    maps.save(savePath)
