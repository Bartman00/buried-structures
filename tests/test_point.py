from buried_structures.point import Point_3d, Origin
import math
import pytest

origin = Point_3d(0, 0, 0)
point_a = Point_3d(1, 0, 0)
point_b = Point_3d(1, 2, 3)
point_z = Point_3d(1, 0)
origin_2 = Origin()

def test_coincident():
    assert (origin.coincident(origin))
    assert point_a.coincident(point_a)
    assert not origin.coincident(point_a)

def test_distance():
    assert origin.distance(point_a) == 1.0
    assert abs(point_a.distance(point_b) - math.sqrt(2**2 + 3**2)) < 1e-6

def test_r():
    assert abs(point_a.dr(point_b) - 2.0) < 1e-6
    assert abs(origin.dr(point_b) - math.sqrt(1**2 + 2**2)) < 1e-6

def test_dx():
    assert abs(origin.dx(point_a) - 1.0) < 1e-6
    assert abs(point_a.dx(origin, reverse=True) - 1.0) < 1e-6
    assert abs(point_a.dx(origin, absolute=True) - 1.0) < 1e-6

def test_dy():
    assert abs(origin.dy(point_b) - 2.0) < 1e-6
    assert abs(point_b.dy(origin, reverse=True) - 2.0) < 1e-6
    assert abs(point_b.dy(origin, absolute=True) - 2.0) < 1e-6

def test_dz():
    assert abs(origin.dz(point_b) - 3.0) < 1e-6
    assert abs(point_b.dz(origin, reverse=True) - 3.0) < 1e-6
    assert abs(point_b.dz(origin, absolute=True) - 3.0) < 1e-6
    
def test_origin_coordinates():
    assert origin_2.x() == 0
    assert origin_2.y() == 0
    assert origin_2.z() == 0
    
def test_missing_z():
    assert point_z.z() == 0
    
    point_z_coordinates = Point_3d(coordinates=(12, 13))
    assert point_z_coordinates.z() == 0
    
def test_origin_coincident():
    assert origin == origin_2
    
def test_nonumeric_inputs():
    with pytest.raises(ValueError):
        point_c = Point_3d(x=1, y="a")

def test_missing_inputs():
    with pytest.raises(ValueError):
        point_c = Point_3d(x=1)
    with pytest.raises(ValueError):
        point_c = Point_3d(x=1, z=5.0)

def test_overloaded_inputs():

    with pytest.raises(ValueError):
        point_c = Point_3d(x=1, y=1, z=1, coordinates=(1, 1, 1))
        
def test_bad_coordinates():

    with pytest.raises(ValueError):
        point_c = Point_3d(coordinates=(0))
        
    with pytest.raises(ValueError):
        point_c = Point_3d(coordinates=(0, 0, 0, 0))
    with pytest.raises(ValueError):
        point_c = Point_3d(coordinates=((0, 0, 0), (0, 0, 0)))

