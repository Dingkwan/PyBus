import numpy as np
from pytrack.graph import graph, distance
from pytrack.analytics import visualization
from pytrack.matching import candidate, mpmatching_utils, mpmatching

def routeMap(data):

    latitude = data["latitude"].to_list()
    longitude = data["longitude"].to_list()

    points = [(lat, lon) for lat, lon in zip(latitude[:50], longitude[:50])]


    # Create BBOX
    north, east = np.max(np.array([*points]), 0)
    south, west = np.min(np.array([*points]), 0)

    # Extract road graph
    G = graph.graph_from_bbox(*distance.enlarge_bbox(north, south, west, east, 500), simplify=True, network_type='drive')


    # Initialize maps
    loc = (np.mean(latitude[:50]), np.mean(longitude[:50]))
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
    maps.save("route_map.html")
