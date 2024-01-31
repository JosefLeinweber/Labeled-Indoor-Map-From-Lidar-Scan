import functools
import sys

import matplotlib.pyplot as plt
import numpy as np
import shapely.geometry as sg
from shapely.geometry import Polygon

from src.utility.scan_processing.helper_functions import alpha_shape


def floorplan_pipeline(point_cloud):
    floor_points = extracting_floor_points(point_cloud)
    two_dimensinal_floor_points = make_floor_points_2d(floor_points)
    floor_edge_indexies = compute_edge_indexies(two_dimensinal_floor_points)
    edge_dict = generate_edge_dict(two_dimensinal_floor_points, floor_edge_indexies)
    sorted_edge_points = sort_edge_dict(edge_dict)

    return Polygon(sorted_edge_points)


def extracting_floor_points(point_cloud):
    floor_points = functools.reduce(
        lambda a, b: a if len(a.points) > len(b.points) else b, segment_helper(point_cloud).values()
    )
    return floor_points


def segment_helper(point_cloud, max_plane_idx=5, segments=None):
    if segments is None:
        segments = {}

    if max_plane_idx == 0:
        return segments

    _, inliers = point_cloud.segment_plane(distance_threshold=0.2, ransac_n=3, num_iterations=1000)

    segments[max_plane_idx - 1] = point_cloud.select_by_index(inliers, invert=False)

    rest = point_cloud.select_by_index(inliers, invert=True)

    return segment_helper(rest, max_plane_idx - 1, segments)


def make_floor_points_2d(floor_points):
    two_dimensinal_floor_points = np.array([[point[0], point[2]] for point in floor_points.points])
    return two_dimensinal_floor_points


def compute_edge_indexies(two_dimensinal_floor_points, alpha=0.25):
    return [[i, j] for i, j in alpha_shape(two_dimensinal_floor_points, alpha=alpha, only_outer=True)]


def generate_edge_dict(two_dimensinal_floor_points, floor_edge_indexies):
    return {str(two_dimensinal_floor_points[i]): two_dimensinal_floor_points[j] for i, j in floor_edge_indexies}


def sort_edge_dict(edge_dict):
    sorted_edge_points = []
    key = list(edge_dict.keys())[0]
    for i in range(len(edge_dict)):
        key = str(key)
        value = edge_dict[key]
        sorted_edge_points.append(value.tolist())
        key = value
    return sorted_edge_points
