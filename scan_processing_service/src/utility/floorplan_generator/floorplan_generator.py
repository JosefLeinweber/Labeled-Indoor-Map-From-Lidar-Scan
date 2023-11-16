import numpy as np
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
import shapely.geometry as sg
import sys

from src.utility.floorplan_generator.helper_functions import alpha_shape, generate_line
from src.utility.floorplan_generator.intersection_point import IntersectionPoint


class FloorplanGenerator:
    def __init__(self, point_cloud):
        self.point_cloud = point_cloud
        self.floor_edge_indexies = []
        self.sorted_edge_points = []
        self.floor_points = self.compute_two_dimensional_floor_points()
        self.polygon = self.compute_floor_plan_polygon()
        self.intersections = []

    def segment_point_cloud(self, max_plane_idx=5):
        """
        Segments the point cloud into multiple planes.
        :param max_plane_idx: The maximum number of planes to segment.
        :return: A dictionary of the segmented planes.
        """
        segment_models = {}
        segments = {}
        rest = self.point_cloud
        for i in range(max_plane_idx):
            colors = plt.get_cmap("tab20")(i)
            segment_models[i], inliers = rest.segment_plane(
                distance_threshold=0.2, ransac_n=3, num_iterations=1000
            )
            segments[i] = rest.select_by_index(inliers, invert=False)
            segments[i].paint_uniform_color(list(colors[:3]))
            rest = rest.select_by_index(inliers, invert=True)
        return segments

    def get_largest_segment(self, segments):
        """
        Returns the largest segment from a dictionary of segments.
        :param segments: A dictionary of segments.
        :return: The largest segment.
        """
        largest = 0
        for i in range(len(segments)):
            if len(segments[i].points) > len(segments[largest].points):
                largest = i
        return segments[largest]

    def extract_floor_points(self):
        """
        Extracts the floor points from the point cloud.
        - uses the segment_point_cloud() and get_largest_segment() functions.
        :return: The floor points.
        """
        segments = self.segment_point_cloud()

        return self.get_largest_segment(segments).points

    def compute_average_floor_height(self):
        """
        Computes the average floor height.
        - uses the extract_floor_points() function.
        :return: The average floor height.
        """
        floor_points = self.extract_floor_points()
        average_floor_height = 0
        for i in range(len(floor_points)):
            average_floor_height += floor_points[i][1]
        average_floor_height /= len(floor_points)
        return average_floor_height

    def compute_two_dimensional_floor_points(self):
        """
        Computes the two dimensional floor points.
        - uses the extract_floor_points() function.
        :return: The two dimensional floor points.
        """
        two_dimensinal_floor_points = []
        floor_points = self.extract_floor_points()

        for i in range(len(floor_points)):
            two_dimensinal_floor_points.append([floor_points[i][0], floor_points[i][2]])
        return np.asanyarray(two_dimensinal_floor_points)

    def compute_alpha_shape(self, alpha=0.25, only_outer=True):
        """
        Computes the alpha shape of the floor points.
        :param alpha: The alpha value.
        :param only_outer: Boolean value to specify if we keep only the outer border or also inner edges.
        """
        return alpha_shape(self.floor_points, alpha=alpha, only_outer=only_outer)

    def compute_edge_indexies(self):
        """
        Computes the edge indexies of the floor points.
        - uses the compute_alpha_shape() function.
        """
        edges = self.compute_alpha_shape()
        for i, j in edges:
            self.floor_edge_indexies.append([i, j])

    def generate_edge_dict(self):
        """
        Generates a dictionary of the floor edges. The key is the starting point and the value is the ending point of an edge.
        :return: The edge dictionary.
        """
        edge_dict = {}

        for i, j in self.floor_edge_indexies:
            edge_dict[str(self.floor_points[i])] = self.floor_points[j]

        return edge_dict

    def sort_floor_edges(self):
        """
        Uses the edge dictionary to sort the floor edges. The sorted edges are stored in the sorted_edge_points list.
        - uses the generate_edge_dict() function.
        """
        edge_dict = self.generate_edge_dict()
        key = list(edge_dict.keys())[0]
        for i in range(len(edge_dict)):
            key = str(key)
            value = edge_dict[key]
            self.sorted_edge_points.append(value)
            key = value

    def compute_floor_plan_polygon(self):
        """
        Computes the floor plan polygon.
        - uses the compute_edge_indexies() and sort_floor_edges() functions.
        :return: The floor plan polygon.
        """
        self.compute_edge_indexies()
        self.sort_floor_edges()
        return Polygon(self.sorted_edge_points)

    def compute_intersections_with_camera_views(self, frames):
        for frame in frames:
            is_intersection = self.polygon.intersection(
                sg.LineString(frame.center_of_fov)
            )
            if type(is_intersection) == sg.linestring.LineString:
                x, y = is_intersection.xy[0][-1], is_intersection.xy[1][-1]
                self.intersections.append(
                    IntersectionPoint(
                        coordinates=[x, y],
                        frame_index=frame.frame_index,
                    )
                )
            elif type(is_intersection) == sg.multilinestring.MultiLineString:
                self.intersections.append(None)
            else:
                self.intersections.append(None)

    def __repr__(self) -> str:
        return f"FloorPlan <point_cloud :{self.point_cloud} \nfloor_edge_indexies : {self.floor_edge_indexies}\nsorted_edge_points : {self.sorted_edge_points}\nfloor_points : {self.floor_points}\npolygon : {self.polygon}\nintersections : {self.intersections}>"
