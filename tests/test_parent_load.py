from buried_structures.load import Load
from buried_structures.point import Point_3d, Origin
import pytest

origin = Origin()
point_a = Point_3d(1, 2, 3)
point_b = Point_3d(10, 10, 10)

load_a = Load(point_a, 1)


def test_type():
    assert load_a.load_type == "Parent"
    
def test_center():
    assert load_a.center == point_a
    
def test_magnitude():
    assert load_a.magnitude == 1
    
def test_stress_x():
    assert load_a.stress_x(point_a) == point_a.x()
def test_stress_y():
    assert load_a.stress_y(point_a) == point_a.y()
def test_stress_z():
    assert load_a.stress_z(point_a) == point_a.z()
    
def test_not_implimented():
    
    with pytest.raises(NotImplementedError):
        print(load_a.shear_xy(point_a))
    with pytest.raises(NotImplementedError):
        print(load_a.shear_yz(point_a))
    with pytest.raises(NotImplementedError):
        print(load_a.shear_xz(point_a))
    with pytest.raises(NotImplementedError):
        print(load_a.displacement_x(point_a))
    with pytest.raises(NotImplementedError):
        print(load_a.displacement_y(point_a))
    with pytest.raises(NotImplementedError):
        print(load_a.displacement_z(point_a))
        
        
