from math import atan2, pi

from buried_structures.point import Origin, Point_3d
from buried_structures.rectangular_load import Rectangular_Load
import pytest

length, width = 10, 20
magnitude = 2.0
o = Origin()
load = Rectangular_Load(o, magnitude, length, width)

all_single_directions = ["x", "y", "z", "shear_xz", "shear_yz", "shear_xy"]

def test_type():
    assert load.load_type == "Rectangular Load"


def test_center():
    assert load.center == o


def test_magnitude():
    assert load.magnitude == 2.0


def test_corner_stress():

    z = 0
    # R1 = length
    # R2 = width
    # R3 = (length**2 + width**2) ** 0.5

    p = magnitude / (2 * pi)

    a = atan2(length * width, 0)
    result = p * a

    assert result == load.corner_stress(z, "z")

    result_x = p * a
    assert result_x == load.corner_stress(z, "x")
    assert result_x == load.corner_stress(z, "y")

def test_corner_stress_0():
    # Tests that should result in 0 corner stress
    
    no_length = Rectangular_Load(o, 1, 0, width)
    no_width = Rectangular_Load(o, 1.0, length, 0)
    no_magnitude = Rectangular_Load(o, 0, length, width)
    
    for direction in all_single_directions:
        assert no_length.corner_stress(1.0, direction) == 0
        assert no_width.corner_stress(1.0, direction) == 0
        assert no_magnitude.corner_stress(1.0, direction) == 0
        
def test_corner_stress_2():

    p_2pi = 2 * pi

    unit_load = Rectangular_Load(o, p_2pi, length, width)
    z = 10.0

    p = 1.0
    R1 = (length**2 + z**2) ** 0.5
    R2 = (width**2 + z**2) ** 0.5
    R3 = (length**2 + width**2 + z**2) ** 0.50

    a = atan2(length * width, z * R3)
    print(f"{z=}")
    print(f"{p=}")
    print(f"{R1=}")
    print(f"{R2=}")
    print(f"{R3=}")
    print(f"{a=}")
    result_z = p * (a + length * width * z / R3 * (1 / R1**2 + 1 / R2**2))
    print(f"{result_z=}")
    assert result_z == unit_load.corner_stress(z, "z")

    result_x = p * (a - length * width * z / (R1**2 * R3))
    assert result_x == unit_load.corner_stress(z, "x")

    result_x = p * (a - length * width * z / (R2**2 * R3))
    assert result_x == unit_load.corner_stress(z, "y")
       
def test_corner_raises():
    with pytest.raises(ValueError):
        print(load.corner_stress(1.0, "fake"))
        
    with pytest.raises(ValueError):
        print(load.corner_stress(-1.0, "x"))
    

def test_corner_stress_unit():

    p_2pi = 2 * pi

    unit_load = Rectangular_Load(o, p_2pi, length, width)
    z = 1.0

    p = 1.0
    R1 = (length**2 + z**2) ** 0.5
    R2 = (width**2 + z**2) ** 0.5
    R3 = (length**2 + width**2 + z**2) ** 0.50

    a = atan2(length * width, z * R3)
    result_z = p * (a + length * width * z / R3 * (1 / R1**2 + 1 / R2**2))
    assert result_z == unit_load.corner_stress(z, "z")

    result_x = p * (a - length * width * z / (R1**2 * R3))
    assert result_x == unit_load.corner_stress(z, "x")

    result_x = p * (a - length * width * z / (R2**2 * R3))
    assert result_x == unit_load.corner_stress(z, "y")


def test_within():

    p2 = Point_3d(0, 0, 0)
    assert load.within(p2)

    p3 = Point_3d(0, 0, 10)
    assert load.within(p3)

    p4 = Point_3d(5, 0, 10)
    assert load.within(p4)

    p5 = Point_3d(5, 10, 10)
    assert load.within(p5)


def test_not_within():

    p2 = Point_3d(5.00001, 0, 0)
    assert not load.within(p2)

    p3 = Point_3d(0, 10.01, 0)
    assert not load.within(p3)

def test_under_corner():

    p2 = Point_3d(0, 0,0)
    assert not load.under_corner(p2)
    
    p3 = Point_3d(length/2, width/2, 0)
    assert load.under_corner(p3)
    
    for corner in load.corner_points:
        assert load.under_corner(corner)
        
    p4 = load.corner_points[3].shifted_point(0.001)
    assert not load.under_corner(p4)

def test_interior_center():

    corner = Point_3d(length / 2, width / 2)
    print(f"Corner = {corner}")
    print(f"o = {o}")
    sub_center = corner.midpoint(o)
    sub_rectangle = Rectangular_Load(sub_center, magnitude, length / 2, width / 2)

    expected = load.interior_superposition(Point_3d(0, 0), "corner_stress", "x")
    print(f"{expected=}")

    result = 4 * sub_rectangle.corner_stress(o.z(), "x")
    print(f"{result=}")
    assert expected == result
    
    print('----- Shifted test -----')
    down_shift = 10.0
    o_shift = o.shifted_point(dz=down_shift)
    print(f"o_shift = {o_shift}")
    print(f"sub_center: {sub_center}")
    
    print("sub_rectangle: ")
    print(sub_rectangle)
    
    expected = load.interior_superposition(Point_3d(0, 0, down_shift), 
                                           "corner_stress", "z")
    print(f"{expected=}")

    result = 4 * sub_rectangle.corner_stress(o_shift.z(), "z")
    # print("sub_rectangle:")
    # print(sub_rectangle)
    print(f"{result=}")
    assert expected == result

    
def test_interior_raises():
    
    p2 = Point_3d(length/2, width/2 + 0.001, 0)

    with pytest.raises(ValueError):
        print(load.interior_superposition(p2, "corner_stress", "x"))
    
    with pytest.raises(ValueError):
        print(load.interior_superposition(o, "corner_stress", "fake"))
    
    with pytest.raises(AttributeError):
        print(load.interior_superposition(o, "fake_function", "x"))
        
def test_interior_edge():

    # Put a point on an edge.

    p2 = Point_3d(0, width/2, 0)

    result = load.interior_superposition(p2, "corner_stress", "z")
    
    sub_point = Point_3d(length/4, 0, 0)
    sub_rectangle = Rectangular_Load(sub_point, magnitude, length/2, width)
    expected = 2 * sub_rectangle.corner_stress(0, "z")
    
    assert result == expected
    
    z_shift = 12
    p3 = Point_3d(0, width/2, z_shift)

    result = load.interior_superposition(p3, "corner_stress", "z")
    
    expected = 2 * sub_rectangle.corner_stress(z_shift, "z")
    assert result == expected


def test_interior_general():

    point = Point_3d(length/4, width/4, 10)
    print(f"point:\n{point}")
    result_z = load.interior_superposition(point, "corner_stress", "z")
    result_x = load.interior_superposition(point, "corner_stress", "x")
    result_y = load.interior_superposition(point, "corner_stress", "y")

    corners = load.corner_points
    

    expected_x, expected_y, expected_z = 0, 0, 0
    for corner in corners:
        center_point = corner.midpoint(point)
        sub_length = corner.dx(point)
        sub_width = corner.dy(point)
        
        print(f"corner:\n{corner}")
        print(f"center_point:\n{center_point}")
        print(f"sub_length:\n{sub_length}")
        print(f"sub_width:\n{sub_width}")

        mag_term = magnitude / (2*pi)
        R1 = (sub_length**2 + point.z()**2) ** 0.50
        R2 = (sub_width**2 + point.z()**2) ** 0.50
        R3 = (sub_length**2 + sub_width**2 + point.z()**2) ** 0.50
        atan_term = atan2(sub_length*sub_width,(point.z()*R3))
        
        print(f"{R1=}")
        print(f"{R2=}")
        print(f"{R3=}")
        print(f"{atan_term=}")
        print(f"{mag_term=}")
        
        temp_z = mag_term*(atan_term + 
                               sub_length*sub_width*point.z()/R3*(
                                   1/R1**2 + 1/R2**2
                                   ))
        print(f"{temp_z=}")
        expected_z += temp_z

        temp_x = mag_term*(atan_term - 
                           sub_length*sub_width*point.z() / (
                               R1**2 * R3
                               ))
        print(f"{temp_x=}")
        expected_x += temp_x
        
        temp_y = mag_term*(atan_term - 
                           sub_length*sub_width*point.z() / (
                               R2**2 * R3
                               ))
        
        expected_y += temp_y
        
    assert result_z == expected_z
    assert result_x == expected_x
    assert result_y == expected_y

def test_exterior_raises():

    p2 = Point_3d(length/2, width/2, 0)

    with pytest.raises(ValueError):
        print(load.exterior_superposition(p2, "corner_stress", "x"))

    p3 = Point_3d(length/2 + 0.1, width/2, 0)
    with pytest.raises(ValueError):
        print(load.exterior_superposition(p3, "corner_stress", "fake"))

    with pytest.raises(AttributeError):
        print(load.exterior_superposition(p3, "fake_function", "x"))
        
def test_exterior_outside():

    print("test_exterior_outside:")
    z = 10.0
    point = Point_3d(length, width, z)
    print(f"point: \n{point}")

    p_term = magnitude / (2 * pi)

    # Furthest  corner
    corner = Point_3d(-length/2, -width/2, z)
    l, w = corner.dx(point, absolute=True), corner.dy(point, absolute=True)
    R1 = (l**2 + z**2) ** 0.50
    R2 = (w**2 + z**2) ** 0.50
    R3 = (l**2 + w**2 + z**2) ** 0.50
    aterm = atan2(l*w, z*R3)
    furthest = p_term * ( aterm + l*w*z/R3 * (1/R1**2 + 1/R2**2))
    

    # Middle corners
    corner = Point_3d(length/2, -width/2, z)
    l, w = corner.dx(point, absolute=True), corner.dy(point, absolute=True)
    R1 = (l**2 + z**2) ** 0.50
    R2 = (w**2 + z**2) ** 0.50
    R3 = (l**2 + w**2 + z**2) ** 0.50
    aterm = atan2(l*w, z*R3)
    
    middle_1 = p_term * ( aterm + l*w*z/R3 * (1/R1**2 + 1/R2**2))
    
    corner = Point_3d(-length/2, width/2, z)
    l, w = corner.dx(point, absolute=True), corner.dy(point, absolute=True)
    R1 = (l**2 + z**2) ** 0.50
    R2 = (w**2 + z**2) ** 0.50
    R3 = (l**2 + w**2 + z**2) ** 0.50
    aterm = atan2(l*w, z*R3)
    
    middle_2 = p_term * ( aterm + l*w*z/R3 * (1/R1**2 + 1/R2**2))
    
    # Nearest corner
    corner = Point_3d(length/2, width/2, z)
    l, w = corner.dx(point, absolute=True), corner.dy(point, absolute=True)
    R1 = (l**2 + z**2) ** 0.50
    R2 = (w**2 + z**2) ** 0.50
    R3 = (l**2 + w**2 + z**2) ** 0.50
    aterm = atan2(l*w, z*R3)
    
    nearest = p_term * ( aterm + l*w*z/R3 * (1/R1**2 + 1/R2**2))
    
    print(f"{nearest=}")
    print(f"{l=}, {w=}")
    print(f"{R1=}, {R2=}, {R3=}")
    print(f"{aterm=}")
    
    result = load.exterior_superposition(point, "corner_stress", "z")
    
    expected = nearest - middle_1 - middle_2 + furthest
    print(f"{middle_1=}")
    print(f"{middle_2=}")
    print(f"{furthest=}")
    
    assert expected == result

def test_exterior_within():
    # Test with symmetry

    print("test_exterior_within:")
    z = 10.0
    point = Point_3d(0, width, z)
    print(f"point: \n{point}")

    p_term = magnitude / (2 * pi)
    print(f"{p_term=}")

    # Furthest  corner
    corner = Point_3d(-length/2, -width/2, z)
    l, w = corner.dx(point, absolute=True), corner.dy(point, absolute=True)
    R1 = (l**2 + z**2) ** 0.50
    R2 = (w**2 + z**2) ** 0.50
    R3 = (l**2 + w**2 + z**2) ** 0.50
    aterm = atan2(l*w, z*R3)
    furthest = p_term * ( aterm + l*w*z/R3 * (1/R1**2 + 1/R2**2))
    print(f"{furthest=}")
    

    # Nearest corner - Pursposely used kitty corner to test symmetry
    corner = Point_3d(length/2, width/2, z)
    l, w = corner.dx(point, absolute=True), corner.dy(point, absolute=True)
    R1 = (l**2 + z**2) ** 0.50
    R2 = (w**2 + z**2) ** 0.50
    R3 = (l**2 + w**2 + z**2) ** 0.50
    aterm = atan2(l*w, z*R3)
    
    nearest = p_term * ( aterm + l*w*z/R3 * (1/R1**2 + 1/R2**2))
    
    print("------NEAREST--------")
    print(f"{l=}, {w=}")
    print(f"{R1=}, {R2=}, {R3=}")
    print(f"{aterm=}")
    print(f"{nearest=}")
    
    result = load.exterior_superposition(point, "corner_stress", "z")
    print(f"{result=}")
    
    expected = 2*furthest - 2*nearest
    print(f"{expected=}")
    
    assert abs(expected - result) <= 1e-6
    

    point = Point_3d(0, -width, z)
    result = load.exterior_superposition(point, "corner_stress", "z")
    assert abs(expected - result) <= 1e-6
    
def test_exterior_within_2():


    # Test with symmetry

    print("test_exterior_within:")
    z = 10.0
    point = Point_3d(length*3, 0, z)
    print(f"point: \n{point}")

    p_term = magnitude / (2 * pi)
    print(f"{p_term=}")

    # Furthest  corner
    corner = Point_3d(-length/2, -width/2, z)
    l, w = corner.dx(point, absolute=True), corner.dy(point, absolute=True)
    R1 = (l**2 + z**2) ** 0.50
    R2 = (w**2 + z**2) ** 0.50
    R3 = (l**2 + w**2 + z**2) ** 0.50
    aterm = atan2(l*w, z*R3)
    furthest = p_term * ( aterm + l*w*z/R3 * (1/R1**2 + 1/R2**2))
    print(f"{furthest=}")
    

    # Nearest corner - Pursposely used kitty corner to test symmetry
    corner = Point_3d(length/2, width/2, z)
    l, w = corner.dx(point, absolute=True), corner.dy(point, absolute=True)
    R1 = (l**2 + z**2) ** 0.50
    R2 = (w**2 + z**2) ** 0.50
    R3 = (l**2 + w**2 + z**2) ** 0.50
    aterm = atan2(l*w, z*R3)
    
    nearest = p_term * ( aterm + l*w*z/R3 * (1/R1**2 + 1/R2**2))
    
    print("------NEAREST--------")
    print(f"{l=}, {w=}")
    print(f"{R1=}, {R2=}, {R3=}")
    print(f"{aterm=}")
    print(f"{nearest=}")
    
    result = load.exterior_superposition(point, "corner_stress", "z")
    print(f"{result=}")
    
    expected = 2*furthest - 2*nearest
    print(f"{expected=}")
    
    assert abs(expected - result) <= 1e-6
    

    point = Point_3d(-length*3, 0, z)
    result = load.exterior_superposition(point, "corner_stress", "z")
    assert abs(expected - result) <= 1e-6
