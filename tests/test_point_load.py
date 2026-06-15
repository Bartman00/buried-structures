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

    p1 = Point_3d(0, 0, 1)

    unit_load = Point_Load(o, 1.0, 0.3)
    result = unit_load.stress_z(p1)

    expected = 3/(2*pi)

    assert result == pytest.approx(expected)
