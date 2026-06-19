from math import atan2, pi, sqrt, cos, sin

from buried_structures.point import Origin, Point_3d
from buried_structures.point_load import Point_Load
import pytest

magnitude = 2.0
poisson = 0.30
o = Origin()
load = Point_Load(o, magnitude, poisson)

def test_type():
    assert load.load_type == "Point Load"
    
def test_properties():
    assert load.magnitude == 2.0
    assert load.poisson == 0.30
    
def test_sigma_z():

    # Unit load, R = 1.0
    p1 = Point_3d(0, 0, 1)
    unit_load = Point_Load(o, 1.0, 0.3)
    result = unit_load.stress_z(p1)

    expected = 3/(2*pi)

    assert result == pytest.approx(expected)
    
    # Unit load, R = 1.0, shift both the laod and checkign point
    # should be the same result
    p2 = Point_3d(1, 1, 1)
    unit_load_shifted = Point_Load(Point_3d(1, 1, 0), 1.0, 0.3)
    
    result = unit_load_shifted.stress_z(p2)
    
    assert result == pytest.approx(expected)
    

    # INclude a magniture
    expected = 3 * magnitude / (2*pi)
    result = load.stress_z(p1)
    
    assert result == pytest.approx(expected)
    
def test_sigma_r():
    # INclude a distance
    p3 = Point_3d(2, 3, 1)
    distance = sqrt(2**2 + 3**2 + 1**2)
    r_distance = sqrt(2**2 + 3**2)
    z3 = 1

    expected = -magnitude/(2*pi*distance**2) * (
            -3*r_distance**2*z3/distance**3 + (1-2*poisson)*distance/(
                distance+z3
                ))
    result = load.stress_r(p3)
    assert result == pytest.approx(expected)
    
def test_sigma_theta():
    # INclude a distance
    p3 = Point_3d(2, 3, 1)
    distance = sqrt(2**2 + 3**2 + 1**2)
    # r_distance = sqrt(2**2 + 3**2)
    z3 = 1

    expected = -(1-2*poisson)*magnitude/(2*pi*distance**2) * (
            z3/distance - distance/(distance + z3))
    result = load.stress_theta(p3)
    assert result == pytest.approx(expected)

def test_sigma_x():
    # INclude a distance
    p1 = Point_3d(2, 0, 1)
    # distance = sqrt(2**2 + 0**2 + 1**2)
    # r_distance = sqrt(2**2 + 0**2)
    # z3 = 1

    expected = load.stress_r(p1)
    result = load.stress_x(p1)
    assert result == pytest.approx(expected)
    
    p2 = Point_3d(3, 2, 10)
    # distance = sqrt(3**2 + 2**2 + 10**2)
    # r_distance = sqrt(3**2 + 2**2)
    # z2 = 10
    
    result = load.stress_x(p2)
    print("load.point:")
    print(load.center)
    print(f"o.theta = {o.theta(p2)}")

    pr = load.stress_r(p2)
    pt = load.stress_theta(p2)

    theta = atan2(2, 3)
    print(f"theta={theta}")
    expected = pr*abs(cos(theta)) + pt*abs(sin(theta))
    
    assert result == pytest.approx(expected)

def test_sigma_y():
    # INclude a distance
    p1 = Point_3d(0, 2, 1)
    # distance = sqrt(2**2 + 0**2 + 1**2)
    # r_distance = sqrt(2**2 + 0**2)
    # z3 = 1

    expected = load.stress_r(p1)
    result = load.stress_y(p1)
    assert result == pytest.approx(expected)
    
    p2 = Point_3d(3, 2, 10)
    # distance = sqrt(3**2 + 2**2 + 10**2)
    # r_distance = sqrt(3**2 + 2**2)
    # z2 = 10
    
    result = load.stress_y(p2)
    print("load.point:")
    print(load.center)
    print(f"o.theta = {o.theta(p2)}")

    pr = load.stress_r(p2)
    pt = load.stress_theta(p2)

    theta = atan2(2, 3)
    print(f"theta={theta}")
    expected = pr*abs(sin(theta)) + pt*abs(cos(theta))
    
    assert result == pytest.approx(expected)
def test_bad_poisson():
    # Poisson limits

    with pytest.raises(ValueError):
        bad_load = Point_Load(o, 1.0, 0)
        
    with pytest.raises(ValueError):
        bad_load = Point_Load(o, 1.0, 0.50001)
        
def test_r():

    pass
