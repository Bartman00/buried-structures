# Point load


from __future__ import annotations

from math import pi, sin, cos

from buried_structures.load import Load
from buried_structures.point import Point_3d


class Point_Load(Load):
    load_type = "Point Load"

    def __init__(
        self, center: Point_3d, magnitude: float, poisson: float = 0.30
    ) -> None:
        
        if not (0 < poisson <= 0.5):
            raise ValueError("Poisson needs to be: 0 < poisson <= 0.5")

        super().__init__(center, magnitude)
        self.poisson = poisson

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, Point_Load):
            return False

        if not super().__eq__(other):
            return False

        # Only has same properties as parent
        return True
        
    def point_geometry(self, point:Point_3d) -> tuple[float, float, float]:
        
        # Return the distance, horizontal plane distance and z
        # of another point. Used in several functions below
        R = self.center.distance(point)
        r = self.center.dr(point)
        z = self.center.dz(point, absolute=True)
        return R, r, z

    def stress_z(self, point: Point_3d) -> float:
        R = self.point_geometry(point)[0]
        return 3 * self.magnitude * (point.z() ** 3) / (2 * pi * (R**5))

    def stress_r(self, point: Point_3d) -> float:
        # Radial stress

        R, r, z = self.point_geometry(point)
        return (
            -self.magnitude
            / (2 * pi * R**2)
            * (-3 * r**2 * z / R**3 + (1 - 2 * self.poisson) * R / (R + z))
        )
        
    def stress_theta(self, point: Point_3d) -> float:
        # Tangential stress

        R = self.center.distance(point)
        z = point.z()
        
        return -(1-2*self.poisson)*self.magnitude/(2*pi*R**2)*(z/R - R/(R+z))

    def stress_x(self, point: Point_3d) -> float:
        # X direction stress

        s_r, s_t = self.stress_r(point), self.stress_theta(point)
        
        # Point raises an error for coincident points in xy plane
        # and we want radial stress only for points directly under the load
        theta = self.center.theta(point) if self.center.dr(point) > 0 else 0

        return s_r*abs(cos(theta)) + s_t*(abs(sin(theta)))

    def stress_y(self, point: Point_3d) -> float:
        # Y direction stress

        s_r, s_t = self.stress_r(point), self.stress_theta(point)
        
        # Point raises an error for coincident points in xy plane
        # and we want radial stress only for points directly under the load
        theta = self.center.theta(point) if self.center.dr(point) > 0 else 0
        return s_r*abs(sin(theta)) + s_t*(abs(cos(theta)))
    
    def shear_rz(self, point: Point_3d) -> float:
        # Shear stress in the r-z plane

        r = self.center.dr(point)
        R = self.center.distance(point)
        z = point.z()

        return 3*self.magnitude*r*z**2/(2*pi*R**5)

    def displacement_z(self, point:Point_3d) -> float:
        return 0



if __name__ == "__main__":
    print("Inside point_load.py")

    p = Point_3d(0, 0, 0)
    magnitude = 1
    point_laod = Point_Load(p, magnitude)

    print(point_laod)
