"""
A simple 3D point object
"""

from __future__ import annotations  # Stops the linter from complaining

import math

import numpy as np
from numpy.typing import ArrayLike


class Point_3d:
    EPS = 1e-6

    def __init__(
        self,
        x: float | None = None,
        y: float | None = None,
        z: float | None = None,
        coordinates: ArrayLike | None = None,
    ) -> None:
        # Input can take x, y, z coordinates or list/tuple of 2 or 3 dimensions.
        # z is always optional, and will assume 0 if omitted.

        if (coordinates is not None) and (
            x is not None or y is not None or z is not None
        ):
            raise ValueError(
                "Can only specify coordinates or x, y, z values. Not both!"
            )

        if coordinates is None:
            # Use x, y, z coordinates
            if x is None:
                raise ValueError("Need x coordinate if coordinates list input is None")
            if y is None:
                raise ValueError("Need y coordinate if coordinates list input is None")

            # Assign to numpy.array for speed
            z = 0.0 if z is None else z
            self.coordinates = np.array([x, y, z], dtype=np.float64)
        else:
            # Check for the correct size:
            coordinates = np.asarray(coordinates, dtype=np.float64)
            shape = coordinates.shape

            if len(shape) != 1:
                raise ValueError("Coordinates need to be a 1 dimensional array")
            elif shape[0] not in [2, 3]:
                raise ValueError("Coordinates need to be 2 or 3 dimensions")

            self.coordinates = (
                coordinates if shape[0] == 3 else np.array([*coordinates, 0.0])
            )

    def x(self) -> float:
        return self.coordinates[0]

    def y(self) -> float:
        return self.coordinates[1]

    def z(self) -> float:
        return self.coordinates[2]

    def distance(self, other: Point_3d) -> float:
        # Return distance to another point
        return math.dist(self.coordinates, other.coordinates)

    def coincident(self, other: Point_3d) -> bool:
        return self.distance(other) < self.EPS

    def dx(
        self, other: Point_3d, reverse: bool = False, absolute: bool = True
    ) -> float:
        # Distance in x direction
        # other.x - self.x if reverse is false.
        if not absolute:
            flip = -1 if reverse else 1
            return flip * (other.x() - self.x())
        else:
            return abs(self.x() - other.x())

    def dy(
        self, other: Point_3d, reverse: bool = False, absolute: bool = True
    ) -> float:
        # Distance in y direction
        # other.y - self.y if reverse is false.
        if not absolute:
            flip = -1 if reverse else 1
            return flip * (other.y() - self.y())
        else:
            return abs(self.y() - other.y())

    def dz(
        self, other: Point_3d, reverse: bool = False, absolute: bool = True
    ) -> float:
        # Distance in z direction
        # other.z - self.z if reverse is false.
        if not absolute:
            flip = -1 if reverse else 1
            return flip * (other.z() - self.z())
        else:
            return abs(self.z() - other.z())

    def dr(self, other: Point_3d) -> float:
        # Distance projected onto the horizontal plane
        return math.sqrt(
            (self.coordinates[0] - other.coordinates[0]) ** 2
            + (self.coordinates[1] - other.coordinates[1]) ** 2
        )
        
    def theta(self, other: Point_3d) -> float:
        # Return cylindrical angle starting from this point
        if self.dr(other) < self.EPS:
            raise ValueError("Point.theta points can't have the same x & y values")

        return math.atan2(self.dy(other), self.dx(other))

    def midpoint(self, other: Point_3d) -> Point_3d:
        # Return the midpoint between this and another point

        return Point_3d((self.coordinates[0]+ other.coordinates[0])/2,
                         (self.coordinates[1] + other.coordinates[1])/2,
                         (self.coordinates[2] + other.coordinates[2])/2,
                         )
                         
    def shifted_point(self, dx: float=0,
                      dy: float=0,
                      dz: float=0) -> Point_3d:
        return Point_3d(self.x() + dx, self.y() + dy, self.z() + dz)
        
    def modified_point(self,
                       x: float|None = None,
                       y: float|None = None,
                       z: float|None = None) -> Point_3d:
        # Returns a copy of point with input coordinates modified
        new_x, new_y, new_z = self.x(), self.y(), self.z()
        
        new_x = new_x if x is None else x
        new_y = new_y if y is None else y
        new_z = new_z if z is None else z
        
        return Point_3d(new_x, new_y, new_z)
        
    def coordinates_string(self) -> str:
        # Compact (x, y, z) string
        return f"({self.x():.2f},{self.y():.2f},{self.z():.2f})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Point_3d):
            return NotImplemented
        return self.coincident(other)

    def __str__(self) -> str:
        return (
            f"x={self.coordinates[0]}, y={self.coordinates[1]}, z={self.coordinates[2]}"
        )


class Origin(Point_3d):
    # Special point at origin

    def __init__(self) -> None:
        super().__init__(coordinates=(0, 0, 0))
        
if __name__ == "__main__":
    print("Inside point.py")
    
    print("Origin: ")
    o = Origin()
    print(o)
    print(o.x())
    
    print("-------")
    print(Point_3d(0, 0))
    
    print("Finished")
