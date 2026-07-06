from math import atan2, pi, sqrt, cos, sin

from buried_structures.point import Origin, Point_3d
from buried_structures.add_load import Add_Load
from buried_structures.point_load import Point_Load
from buried_structures.rectangular_load import Rectangular_Load
import pytest

magnitude = 14.0
poisson = 0.30
o = Origin()
p = Point_3d(12, 0, 0)
load = Point_Load(o, magnitude, poisson)
empty_add = Add_Load([])

single_add = Add_Load([load])

point = Point_3d(0, 0, 12)

double_add = Add_Load([load, load])

length, width = 16, 32
distributed_magnitude = magnitude / (length * width)
rectangular_load = Rectangular_Load(o, 
                                   distributed_magnitude,
                                   length, width)
rectangular_load_2 = Rectangular_Load(p, 
                                   distributed_magnitude,
                                   length, width)
multi_add = Add_Load([load, rectangular_load, rectangular_load_2])

def test_type():
    assert empty_add.load_type == "Add Load"
    assert single_add.load_type == "Add Load"
    
    for load in single_add.loads:
        assert load.load_type == "Point Load"
    
def test_simple():

    result = single_add.stress_x(point)
    expected = load.stress_x(point)
    assert result == expected
    
    result = single_add.stress_y(point)
    expected = load.stress_y(point)
    assert result == expected
    
    result = single_add.stress_z(point)
    expected = load.stress_z(point)
    assert result == expected
    
def test_double():

    result = double_add.stress_x(point)
    expected = 2*load.stress_x(point)
    assert result == expected
    
    result = double_add.stress_y(point)
    expected = 2*load.stress_y(point)
    assert result == expected
    
    result = double_add.stress_z(point)
    expected = 2*load.stress_z(point)
    assert result == expected
    
def test_rect():

    expected = (load.stress_x(point) +
                rectangular_load.stress_x(point) +
                rectangular_load_2.stress_x(point)
              )
    result = multi_add.stress_x(point)
    assert result == expected
    
    expected = (load.stress_y(point) +
                rectangular_load.stress_y(point) +
                rectangular_load_2.stress_y(point)
              )
    result = multi_add.stress_y(point)
    assert result == expected
    
    expected = (load.stress_z(point) +
                rectangular_load.stress_z(point) +
                rectangular_load_2.stress_z(point)
              )
    result = multi_add.stress_z(point)
    assert result == expected
    
def test_fails():

    with pytest.raises(ValueError):
        print(single_add.sum_effect("stress_fake", point))
    
