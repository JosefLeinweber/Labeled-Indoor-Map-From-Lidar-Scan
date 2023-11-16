class IntersectionPoint:
    def __init__(self, coordinates, frame_index, classification):
        self.coordinates = coordinates
        self.classification = classification
        self.frame_index = frame_index

    def __repr__(self) -> str:
        return f"IntersectionPoint <coordinates :{self.coordinates} \nclassification : {self.classification}\nframe_index : {self.frame_index}>"
