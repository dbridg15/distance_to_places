import json
import os
import requests
from typing import List
from collections import namedtuple
from dataclasses import dataclass
from pyproj import Transformer

# TODO: logging, better exception handling

OS_API_KEY = os.environ.get('OS_API_KEY')


# custom types

Point = namedtuple('Point', ['x', 'y'])


@dataclass
class Feature:
    name: str
    distance: float
    location: Point

    def __lt__(self, other):
        """Feature classes are sorted by distance"""
        return self.distance < other.distance


# functions


def load_features_data(filepath: str) -> dict:
    """
    load features data in a json file and return as dict
    converts location tuples to Points
    """

    with open(filepath, 'r') as f:
        data = json.load(f)

    return {k: Point(*v) for k, v in data.items()}


def get_point(query: str) -> Point:
    """
    use ordnance-surveys `OS Names API` to find the coordinated of a search
    query (postcode) returns as (easting, northing) in EPSG27700 projection

    TODO: i think the places api would be better for this but cant get access
    """

    maxresults = 1  # only want the closest match
    local_type = 'Postcode'

    url = ('https://api.os.uk/search/names/v1/find?'
           f'query={query}'
           f'&maxresults={maxresults}'
           f'&fq=local_type:{local_type}'
           f'&key={OS_API_KEY}'
           )

    out = requests.get(url)

    result = json.loads(out.content)['results'][0]['GAZETTEER_ENTRY']

    return Point(result.get('GEOMETRY_X'), result.get('GEOMETRY_Y'))


def _distance(p1: Point, p2: Point) -> float:
    """calculate the distance between two points"""

    x_2, y_2 = ((i[0] - i[1])**2 for i in zip(p1, p2))

    return (x_2 + y_2)**0.5


transformer = Transformer.from_crs("EPSG:27700", "EPSG:4326")


def transform_points(features: List[Feature]) -> List[Feature]:
    """
    transform 'location' attribute in list of Features
    from EPSG:27700 to EPSG:4326 projection
    """

    for i in features:
        i.location = Point(*transformer.transform(*i.location))

    return features


def find_nearest(point: Point, targets: dict, n: int = 5) -> List[Feature]:
    """
    return the nearest n targets to point, with 'location' attributes converted
    to lat/long

    Parameters
    ----------
    point : Point
        the point to find nearest targets to
    targets : dict
        dict in form:
            >>> {'target_name': Point(x, y), ...}
    n : int, optional
        number of results to return, by default 5

    Returns
    -------
    list(Feature)
        the closest n targets to point
    """

    distances = [Feature(k, _distance(v, point), v)
                 for k, v in targets.items()]

    top_n = sorted(distances)[:n]

    return transform_points(top_n)


def feature_to_table_item(feature: Feature) -> str:
    """convert a feature to a table row in HTML"""
    return ''.join([f'<td>{i}</td>' for i in
                    (feature.name,
                     f'{int(feature.distance)}m',
                     f'{feature.location.x:.6f}, {feature.location.y:.6f}')])


def table_from_features(features: List[Feature]) -> str:
    """converts a list of features to a HTML table"""

    headers = ''.join([f'<th>{c}</th>' for c in
                       ('Station Name', 'Distance', 'Lat/Long')])

    rows = [feature_to_table_item(f) for f in features]
    body = ''.join(f'<tr>{i}</tr>' for i in [headers, *rows])
    return f'<table>{body}</table>'
