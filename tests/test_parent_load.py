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

    assert load_a.stress(point_a, direction="x") == 1
    assert load_a.stress(point_a, direction="y") == 2
    assert load_a.stress(point_a, direction="z") == 3
    
def test_displacement():

    assert load_a.displacement(point_a, "x") == -1
    assert load_a.displacement(point_a, "y") == -2
    assert load_a.displacement(point_a, "z") == -3
    
def test_not_implimented():
    
    with pytest.raises(NotImplementedError):
        print(load_a.stress(point_a, direction="r"))
        
    with pytest.raises(NotImplementedError):
        print(load_a.displacement(point_a, direction="?"))
    with pytest.raises(NotImplementedError):
        print(load_a.displacement(point_a, direction=""))
        
def test_reference():

    assert load_a.reference() == "No reference, made up load"

def test_description():

    assert load_a.description() == """
    Parent load that just has hard coded loads and
    displacements.
    """
def test_markdown():

    assert load_a.markdown() == """
    # Parent Load

    Includes hard coded stresses and displacements.
    """

