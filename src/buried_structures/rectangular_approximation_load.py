from __future__ import annotations

from buried_structures import Point_3d
from buried_structures import Add_Load
from buried_structures import Point_Load
from buried_structures import Rectangular_Load
from buried_structures.load import Load

class Rectangular_Approximation(Add_Load):

    load_type = "Rectangular Load approximated with Point Loads"
    
    def __init__(self, rectangular_load: Rectangular_Load,
                 x_n_points: int, y_n_points: int,
                 poisson: float = 0.30):
        
        self.rectangular_load = rectangular_load
        
        self.x_n_points, self.y_n_points = x_n_points, y_n_points
        self.x_points = divide_along(rectangular_load.corner_points[0].x(),
                                     rectangular_load.corner_points[2].x(),
                                     x_n_points)
        self.y_points = divide_along(rectangular_load.corner_points[0].y(),
                                     rectangular_load.corner_points[1].y(),
                                     y_n_points)
        z = rectangular_load.center.z()                             
        self.points = []
        for ix in self.x_points:
            for iy in self.y_points:
                self.points.append(Point_3d(ix, iy, z))
        self.n_points = len(self.points)
        self.down = rectangular_load.down
        self.point_magnitude = self.rectangular_load.load() / self.n_points
        
        self.loads = [Point_Load(ip, self.point_magnitude, 
                                 poisson, self.down) for ip in self.points]
        
        
        

def divide_along(min_val: float, max_val: float, 
                 divisions: int) -> list[float]:
    # Returns a list of evenly spaced values between
    # min_val and max_val.
    # First and last are 1/2 spacing from min_val & max_val

    assert (divisions > 0), "Need positive divisions"
    assert (max_val > min_val), "divide_along: max_val > min_val"
    spacing = (max_val - min_val) / divisions
    ret = [min_val + i*spacing + spacing/2.0 for i in range(divisions)]
    
    return ret
