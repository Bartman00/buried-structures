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
