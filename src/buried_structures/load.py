# Parent load class
from __future__ import annotations

from buried_structures import Point_3d


class Load:
    load_type = "Parent"

    def __init__(self, center: Point_3d, magnitude: float) -> None:

        self.center = center
        self.magnitude = magnitude

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, Load):
            return False

        # Check type first. This will avoid children comparing
        # Parameters that might not exist in other Loads
        if other.load_type != self.load_type:
            return False

        # These inputs should always be included in children classes
        return (self.magnitude == other.magnitude) and (self.center == other.center)
        
    def __str__(self) -> str:

        return f"""
    {self.load_type} type load:\n
    Center:\n{self.center}\n
    Magnitude: {self.magnitude}
    """

    # Generic stress functions
    @property
    def _stress_dispatch(self) -> dict:
        # List of defined stress directions and functions
        # This will be overridded by children classes.
        return {
            "x": self.stress_x,
            "y": self.stress_y,
            "z": self.stress_z,
        }

    def stress(self, point: Point_3d, direction="z") -> float:
        """
        Stress dispatcher. It sends the direction to
        the appropriate stress function.
        """
        if direction not in self._stress_dispatch:
            raise NotImplementedError(
                f"{direction} stress is not implemented for {self.load_type} load"
            )

        return self._stress_dispatch[direction](point)

    def stress_xyz(self, point: Point_3d):
        """
        Returns x, y, z stresses.
        """
        return self.stress(point, "x"), self.stress(point, "y"), self.stress(point, "z")

    @property
    def _displacement_dispatch(self) -> dict:
        # List of defined displacement directions and functions
        # This will be overridded by children classes.
        return {
            "x": self.displacement_x,
            "y": self.displacement_y,
            "z": self.displacement_z,
        }

    def displacement(self, point: Point_3d, direction="z") -> float:
        """
        Displacement dispatcher. It sends the direction to
        the appropriate displacement function.
        """
        if direction not in self._displacement_dispatch:
            raise NotImplementedError(
                f"{direction} displacement is not implemented for {self.load_type} load"
            )

        return self._displacement_dispatch[direction](point)

    def reference(self) -> str:
        return "No reference, made up load"

    def description(self) -> str:
        return """
    Parent load that just has hard coded loads and
    displacements.
    """

    def markdown(self) -> str:
        return """
    # Parent Load

    Includes hard coded stresses and displacements.
    """

    # Unique stress functions
    def stress_x(self, point: Point_3d) -> float:
        return point.x()

    def stress_y(self, point: Point_3d) -> float:
        return point.y()

    def stress_z(self, point: Point_3d) -> float:
        return point.z()

    # Uniqe displacement functions
    def displacement_x(self, point: Point_3d) -> float:
        return -point.x()

    def displacement_y(self, point: Point_3d) -> float:
        return -point.y()

    def displacement_z(self, point: Point_3d) -> float:
        return -point.z()
