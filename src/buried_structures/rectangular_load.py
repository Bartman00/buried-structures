# Rectangular load
from __future__ import annotations

from buried_structures import Load, Point_3d
from math import pi, radians, atan2
from typing import cast


class Rectangular_Load(Load):
    load_type = "Rectangular Load"

    def __init__(
        self, center: Point_3d, magnitude: float, length: float, width: float
    ) -> None:

        super().__init__(center, magnitude)
        self.length = length
        self.width = width

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
    def stress_x(self, point: Point_3d):
        return point.x()

    def stress_y(self, point: Point_3d):
        return point.y()

    def stress_z(self, point: Point_3d):
        return point.z()
        
    def stress_corner(self, z: float, direction: str) -> float | tuple[float, float, float]:
        # Returns the stress under a corner.
        # TODO: Verify using atan2 gives the same result to avoid
        # using a hard-coded minimum z value

        
        allowable_directions = ["x", "y", "z", "shear_xz", 
                                "shear_yz", "shear_xy", "all_normal",
                                "all_shear"]
        if direction not in allowable_directions:
            raise ValueError(f"{direction} not allowed in rectangular_load.stress_corner.")
            
        # R values
        R1 = (self.length**2 + z**2)**0.5
        R2 = (self.width**2 + z**2) ** 0.5
        R3 = (self.length**2 + self.width**2 + z**2) ** 0.5

        # Front stress term
        p = self.magnitude / (2 * pi)
        l, b = self.length, self.width
        
        atan_term = (atan2(l * b, z*R3) if 
                     direction in ["x", "y", "z"] else None)


        if direction == "z":
            return p * (atan_term + l*b/R3 * (1/R1**2 + 1/R2**2))
        elif direction == "x":
            return p * (atan_term - l*b*z/(R1**2 * R3))
        elif direction == "y":
            return p * (atan_term - l*b*z/(R2**2 * R3))
        elif direction == "shear_xz":
            return p * (b/R2 - z**2 * b / (R1**2 * R3))
        elif direction == "shear_yz":
            return p * (l/R1 - z**2 * l / (R2**2 * R3))
        elif direction == "shear_xy":
            return p * (1 + z/R3 - z*(1/R1 + 1/R2))
        elif direction == "all_normal":
            sigma_x = cast(float, self.stress_corner(z, "x"))
            sigma_y = cast(float, self.stress_corner(z, "y"))
            sigma_z = cast(float, self.stress_corner(z, "z"))
            return sigma_x, sigma_y, sigma_z
        elif direction == "all_shear":
            tau_xz = cast(float, self.stress_corner(z, "shear_xz"))
            tau_yz = cast(float, self.stress_corner(z, "shear_yz"))
            tau_xy = cast(float, self.stress_corner(z, "shear_xy"))
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
