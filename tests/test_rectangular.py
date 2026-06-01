from buried_structures.rectangular_load import Rectangular_Load
import pytest
from buried_structures.point import Point_3d, Origin
from math import atan2, pi

length, width = 10, 20
magnitude = 2.0
o = Origin()
load = Rectangular_Load(o, magnitude, length, width)

def test_type():
    assert load.load_type == "Rectangular Load"
    
def test_center():
    assert load.center == o
    
def test_magnitude():
    assert load.magnitude == 2.0
    
def test_corner():
    
    z = 0
    R1 = length
    R2 = width
    R3 = (length**2 + width**2) ** 0.5


    p = magnitude / (2 * pi)

    a = (atan2(length*width, 0))
    result = p * (a + length*width/R3 * (1/R1**2 + 1/R2**2))

    assert result == load.stress_corner(z, "z")
    
    result_x = p * a
    assert result_x == load.stress_corner(z, "x")
    assert result_x == load.stress_corner(z, "y")
    
def test_1():

    p_2pi = 2 * pi

    unit_load = Rectangular_Load(o, p_2pi, length, width)
    z = 1.0
    
    p = 1.0
    R1 = (length**2 + z**2)**0.5
    R2 = (width**2 + z**2)**0.5
    R3 = (length**2 + width**2 + z**2) ** 0.50
    
    a = (atan2(length*width, z*R3))
    result_z = p * (a + length*width*z/R3 * (1/R1**2 + 1/R2**2) )
    assert result_z == unit_load.stress_corner(z, "z")

    result_x = p * (a - length*width*z/(R1**2 * R3))
    assert result_x == unit_load.stress_corner(z, "x")
    
    result_x = p * (a - length*width*z/(R2**2 * R3))
    assert result_x == unit_load.stress_corner(z, "y")


