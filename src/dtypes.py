from collections import namedtuple
from dataclasses import dataclass


Point = namedtuple('Point', ['x', 'y'])


@dataclass
class Feature:
    name: str
    distance: float
    location: Point

    def __lt__(self, other):
        """Feature classes are sorted by distance"""
        return self.distance < other.distance
