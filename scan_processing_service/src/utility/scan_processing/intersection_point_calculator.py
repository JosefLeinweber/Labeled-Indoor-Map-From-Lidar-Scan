import sys

import loguru
import matplotlib.pyplot as plt
import numpy as np
import shapely.geometry as sg
from shapely.geometry import Polygon

from src.models.schemas.frame_schema import FrameInIntersectionCalculator
from src.models.schemas.intersection_point_schema import IntersectionPointOutCalculator
from src.utility.scan_processing.helper_functions import alpha_shape, generate_vector


class IntersectionPointCalculator:
    def __init__(
        self,
        sorted_edged_points: list,
        frames: list[FrameInIntersectionCalculator],
        vector_length=100,
    ):
        self.sorted_edged_points = sorted_edged_points
        self.intersections: list[IntersectionPointOutCalculator] = []
        self.polygon = Polygon(sorted_edged_points)
        self.frames = frames
        self.vector_length = vector_length

    def compute_intersections(self):
        for frame in self.frames:
            is_intersection = self.polygon.intersection(
                sg.LineString(self._compute_vector_in_camera_view_direction(frame))
            )
            if type(is_intersection) == sg.linestring.LineString:
                x, y = is_intersection.xy[0][-1], is_intersection.xy[1][-1]
                loguru.logger.debug(f"intersection point: {x}, {y}")
                self.intersections.append(
                    IntersectionPointOutCalculator(
                        coordinates=[x, y],
                        frameIndex=frame.frame_index,
                    )
                )

    def _compute_vector_in_camera_view_direction(self, frame: FrameInIntersectionCalculator):
        vector = generate_vector(frame.camera_pose_ar_frame, length=self.vector_length)

        camera_view_2d = []
        for i in range(len(vector)):
            camera_view_2d.append([vector[i][0], vector[i][2]])

        return camera_view_2d
