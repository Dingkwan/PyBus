import os

import numpy as np
import pandas as pd
from natsort import natsorted

# Creation of the video
from tqdm import tqdm
import cv2

from pytrack.analytics import video
from pytrack.graph import distance

# Creation of matched path
from pytrack.graph import graph
from pytrack.matching import candidate, mpmatching_utils, mpmatching

from IPython.display import Video

def create_video(videoFolder,data):

    latitude = data["latitude"].to_list()
    longitude = data["longitude"].to_list()

    points = [(lat, lon) for lat, lon in zip(latitude[:30], longitude[:30])]

    # Create BBOX
    north, east = np.max(np.array([*points]), 0)
    south, west = np.min(np.array([*points]), 0)

    # Extract road graph
    G = graph.graph_from_bbox(*distance.enlarge_bbox(north, south, west, east, 500), simplify=True, network_type='drive')

    # Extract candidates
    G_interp, candidates = candidate.get_candidates(G, points, interp_dist=5, closest=True, radius=30)

    # Extract trellis DAG graph
    trellis = mpmatching_utils.create_trellis(candidates)

    # Perform the map-matching process
    path_prob, predecessor = mpmatching.viterbi_search(G_interp, trellis, "start", "target")

    _, path = mpmatching_utils.create_matched_path(G_interp, trellis, predecessor)  # Path expressed through a list of nodes (lat, lng)


    root_dir = "SV_panoramas"  # Directory where save Google Street View panoramas
    api_key = 'AIzaSyAgET9YdZVIR2OqQ42gZMeCSOMyPyIgOYs'

    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    for i in tqdm(range(len(path))):
        if not os.path.isdir(os.path.join(root_dir, str(i))):
            if i != 0:
                point = path[i]
                prec_point = path[i - 1]
                head = distance.get_bearing(prec_point[0], prec_point[1], point[0], point[1])
            else:
                point = path[i]
                succ_point = path[i + 1]
                head = distance.get_bearing(point[0], point[1], succ_point[0], succ_point[1])

            pic, meta = video.extract_streetview_pic(point, api_key, size="640x640", heading=head, pitch=-10)

            if pic is not None:
                video.save_streetview(pic, meta, os.path.join(root_dir, str(i)))


    images = list()
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith("pic.png"):
                images += [os.path.join(root, file)]

    images = natsorted(images)

    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    video_path = videoFolder + "/" + "my_route_video.mp4"

    video.make_video(images, video_path, fourcc, fps=16, size=(640, 640), is_color=True)


    Video(video_path, embed=True, width=640, height=640)