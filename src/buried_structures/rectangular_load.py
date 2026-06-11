# Rectangular load
# Always aligned so that length is in the x direction, and
# width is in the y direction.
from __future__ import annotations

# from collections.abc import Callable
from math import atan2, pi
from typing import cast

from buried_structures.load import Load
from buried_structures.point import Point_3d


class Rectangular_Load(Load):
    load_type = "Rectangular Load"

    def __init__(
        self, center: Point_3d, magnitude: float, length: float, width: float
    ) -> None:

        if length < 0:
            raise ValueError("Rectangular Load cannot have a negative length")
        if width < 0:
            raise ValueError("Rectangular Load cannot have a negative width")

        super().__init__(center, magnitude)
        self.length = length
        self.width = width
        self.center = center
        self.xrange = (center.x() - length / 2, center.x() + length / 2)
        self.yrange = (center.y() - width / 2, center.y() + width / 2)
        self.corner_points = [
            Point_3d(self.xrange[0], self.yrange[0]),
            Point_3d(self.xrange[0], self.yrange[1]),
            Point_3d(self.xrange[1], self.yrange[0]),
            Point_3d(self.xrange[1], self.yrange[1]),
        ]

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, Rectangular_Load):
            return False

        # Check if parent's more basic checks show equal
        if not super().__eq__(other):
            return False

        # These inputs should always be included in children classes
        return (self.length == other.length) and (self.width == other.width)

    def __str__(self) -> str:

        return f"""
    {self.load_type} type load:\n
    Center:\n{self.center}\n
    Magnitude: {self.magnitude}\n
    Length: {self.length}\n
    Width: {self.width}
    """

    def stress_xyz(self, point: Point_3d):
        return False

    def reference(self):
        return """Elastic Solutions for Soil and Rock Mechanics, 
Poulos and Davis, 3.4.1 Uniform vertical loading on a Rectangular Area"""

    def description(self):
        return """
Uniform vertical stress over a rectangle.

Magnitude is in a pressure such as ksi. Positive magnitude is downward.
length is in the x direction and width is in the y direction.

Uses rectangular superposition as described in the Jupyter notebook to
extend the results beyond the corners.

If stress in multiple directions are needed, it is faster use stress_xyz
than calling stress 3 times because it can recycle many of the common terms.
    """

    def markdown(self):
        return """
    # Parent Load

    Includes hard coded stresses and displacements.
    """

    # Unique stress functions
    def stress_x(self, point: Point_3d) -> float:
        return point.x()

    def stress_y(self, point: Point_3d):
        return point.y()

    def stress_z(self, point: Point_3d):
        return point.z()

    def corner_stress(
        self, z: float, direction: str
    ) -> float | tuple[float, float, float]:
        # Returns the stress under a corner.
        # TODO: Verify using atan2 gives the same result to avoid
        # using a hard-coded minimum z value

        allowable_directions = [
            "x",
            "y",
            "z",
            "shear_xz",
            "shear_yz",
            "shear_xy",
            "all_normal",
            "all_shear",
        ]
        if direction not in allowable_directions:
            raise ValueError(
                f"{direction} not allowed in rectangular_load.stress_corner."
            )
        if z < 0:
            raise ValueError("Rectangular load stresses only defined for positive z" )

        if self.length == 0 or self.width == 0 or self.magnitude == 0:
            # The length & width early exits are helpful for
            # superposition where some sub-rectangles might
            # have 0 length or width
            return 0.0

        # R values
        R1 = (self.length**2 + z**2) ** 0.5
        R2 = (self.width**2 + z**2) ** 0.5
        R3 = (self.length**2 + self.width**2 + z**2) ** 0.5

        # Front stress term
        p = self.magnitude / (2 * pi)
        l, b = self.length, self.width

        atan_term = atan2(l * b, z * R3) if direction in ["x", "y", "z"] else None

        if direction == "z":
            return p * (atan_term + l * b * z/ R3 * (1 / R1**2 + 1 / R2**2))
        elif direction == "x":
            return p * (atan_term - l * b * z / (R1**2 * R3))
        elif direction == "y":
            return p * (atan_term - l * b * z / (R2**2 * R3))
        elif direction == "shear_xz":
            return p * (b / R2 - z**2 * b / (R1**2 * R3))
        elif direction == "shear_yz":
            return p * (l / R1 - z**2 * l / (R2**2 * R3))
        elif direction == "shear_xy":
            return p * (1 + z / R3 - z * (1 / R1 + 1 / R2))
        elif direction == "all_normal":
            sigma_x = cast(float, self.corner_stress(z, "x"))
            sigma_y = cast(float, self.corner_stress(z, "y"))
            sigma_z = cast(float, self.corner_stress(z, "z"))
            return sigma_x, sigma_y, sigma_z
        elif direction == "all_shear":
            tau_xz = cast(float, self.corner_stress(z, "shear_xz"))
            tau_yz = cast(float, self.corner_stress(z, "shear_yz"))
            tau_xy = cast(float, self.corner_stress(z, "shear_xy"))
            return tau_xz, tau_yz, tau_xy
        else:
            raise ValueError("Missing case in rectangular_load.stress_corner")

    # Uniqe displacement functions
    def displacement_x(self, point: Point_3d):
        return -point.x()

    def displacement_y(self, point: Point_3d):
        return -point.y()

    def displacement_z(self, point: Point_3d):
        return -point.z()

    def within(self, p: Point_3d) -> bool:
        # Return if a point is within the x-y bounds
        if not (self.xrange[0] <= p.x() <= self.xrange[1]):
            return False

        if not (self.yrange[0] <= p.y() <= self.yrange[1]):
            return False

        return True
        
    def under_corner(self, p:Point_3d) -> bool:
        # Return true if a point is under a corner

        for corner in self.corner_points:
            if corner.dr(p) <= corner.EPS:
                return True

        return False

    def rectangular_superposition(
        self,
        point: Point_3d,
        corner_function: str,
        direction: str,
    ) -> float:
        # Returns a generalized stress or displacement for an arbritrary
        # point. Takes which stress

        if self.within(point):
            # Point is within the bounding rectangle
            return self.interior_superposition(point, corner_function, direction)

        # Point is not under the bounding rectangle
        return self.exterior_superposition(point, corner_function, direction)

    def interior_superposition(
        self, point: Point_3d, corner_function: str, direction: str
    ) -> float:
        # Uses rectangular superposition

        if not self.within(point):
            raise ValueError(f"""rectangular_point.interior superposition 
                             was passed a point outside of it.
                             {point=} is outside of the corners.
                             """)
        if not hasattr(self, corner_function):
            raise AttributeError(f"{corner_function} is not defined for rectangular_load")

        ret = 0
        for corner in self.corner_points:
            center_point = corner.midpoint(point).modified_point(z=0)
            length = 2*center_point.dx(point, absolute=True)
            width = 2*center_point.dy(point, absolute=True)
            sub_rectangle = Rectangular_Load(
                center_point, self.magnitude, length, width
            )

            ret += getattr(sub_rectangle, corner_function)(point.z(), direction)
        return ret

    def exterior_superposition(
        self, point: Point_3d, corner_function: str, direction: str
    ) -> float:
        # Superposition function for a point not under the load

        if self.within(point):
            raise ValueError(f"""Rectangular_Load.exterior_superposition
                             was passed a point inside of the load.
                             {point=} is inside the corners.
                             """)

        if not hasattr(self, corner_function):
            raise AttributeError(f"{corner_function} is not defined for rectangular_load")

        sub_results = []
        for corner in self.corner_points:
            center_point = corner.midpoint(point)
            length = 2*center_point.dx(point, absolute=True)
            width = 2*center_point.dy(point, absolute=True)
            sub_rectangle = Rectangular_Load(
                center_point, self.magnitude, length, width
            )

            sub_results.append(
                getattr(sub_rectangle, corner_function)(point.z(), direction)
            )

        within_x = self.xrange[0] <= point.x() <= self.xrange[1]
        within_y = self.yrange[0] <= point.y() <= self.yrange[1]
        is_within = within_x or within_y

        if not is_within:
            # Closest point - Middle 2 + Furthest
            distances = [corner.distance(point) for corner in self.corner_points]
            sorted_stress = [val for _, val in sorted(zip(distances, sub_results))]
            return sorted_stress[0] - sorted_stress[1] - sorted_stress[2] + sorted_stress[3]

        else:
            if within_x:
                # Point is within the xrange of the load, not inside it.
                if point.y() > self.center.y():
                    # Point is above (point.y > center.y)
                    # Add bottom 2, subtract top 2 sub-rectangle affects
                    flippers = [1, -1, 1, -1]
                else:
                    # Point is below
                    # Add top 2, subtract bottom 2 sub-rectangle affects
                    flippers = [-1, 1, -1, 1]
            else:
                if point.x() > self.center.x():
                    # Point is to right (point.x > center.x)
                    # Add left 2 points, subtract right 2
                    flippers = [1, 1, -1, -1]
                else:
                    # Point is to the left
                    # Add right 2 points, subtract left 2
                    flippers = [-1, -1, 1, 1]

            ret = 0
            for i, flip in enumerate(flippers):
                ret += flip * sub_results[i]

            return ret


if __name__ == "__main__":
    print("Inside rectangular_load.py")
    length, width = 10, 20
    magnitude = 2.0
    o = Point_3d(0, 0, 0)
    load = Rectangular_Load(o, magnitude, length, width)
    
    z = 10.0
    
    corner_pressure = load.corner_stress(z, "z")
    print(f"{corner_pressure=}")

    
    pressure_point = Point_3d(0, 0, z)
    pressure = load.interior_superposition(pressure_point, "corner_stress", "z")
    
    print(f"load under center = {pressure}")
    
    sub_center = o.midpoint(Point_3d(length/2, width/2, 0))
    sub_load = Rectangular_Load(sub_center, magnitude, length/2, width/2)
    sub_pressure = sub_load.corner_stress(pressure_point.z(), "z")

    print(f"sub-load under center = {sub_pressure}")
    
    print("-------- EXTERIOR WITHIN ---------")
    p = Point_3d(0, 20, 10)
    print(load.exterior_superposition(p, "corner_stress", "z"))

    print("Finished")
