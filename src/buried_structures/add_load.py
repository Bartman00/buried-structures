"""
Add's multiple loads together and returns sum of effects
"""
from __future__ import annotations

from buried_structures import Point_3d
from buried_structures.load import Load

class Add_Load(Load):

    load_type = "Add Load"
    
    def __init__(self, loads: list[Load]):
        
        if len(loads) > 1:
            for load in loads[1:]:
                assert (load.down == loads[0].down), "All loads need to have the same 'down' for an Add_Load"
        self.loads = loads
        
    def sum_effect(self, f: str, point: Point_3d)-> float:
        
        ret = 0

        for load in self.loads:
            if not hasattr(load, f):
                raise ValueError(f"{load.load_type} does not have a function: {f}")
            
            effect = getattr(load, f)
            ret += effect(point)

        return ret
    
    def stress_x(self, point: Point_3d) -> float:
        return self.sum_effect("stress_x", point)
    def stress_y(self, point: Point_3d) -> float:
        return self.sum_effect("stress_y", point)
    def stress_z(self, point: Point_3d) -> float:
        return self.sum_effect("stress_z", point)

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, Add_Load):
            return False

        if len(self.loads) != len(other.loads):
            return False

        for load, other_load in zip(self.loads, other.loads):
            if load != other_load:
                return False

        return True

    def __str__(self) -> str:

        ret = f"Load type: {self.load_type}\n"
        ret += f"Loads: {len(self.loads)}\n"
        
        for i, load in enumerate(self.loads):
            ret += f"load: {i}\n"
            ret += str(load)
        
        return ret
