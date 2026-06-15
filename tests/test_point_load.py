from math import atan2, pi

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

def test_bad_poisson():
    # Poisson limits

    with pytest.raises(ValueError):
        bad_load = Point_Load(o, 1.0, 0)
        
    with pytest.raises(ValueError):
        bad_load = Point_Load(o, 1.0, 0.50001)
