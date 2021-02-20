import json
import os
import requests
from typing import List
from pyproj import Transformer

from dtypes import Point, Feature

# TODO: logging, better exception handling

OS_API_KEY = os.environ.get('OS_API_KEY')


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
    query returns as (easting, northing) in EPSG27700 projection
    """

    maxresults = 1  # only want the closest match

    url = ('https://api.os.uk/search/names/v1/find?'
           f'query={query}'
           f'&maxresults={maxresults}'
           f'&key={OS_API_KEY}'
           )

    out = requests.get(url)

    result = json.loads(out.content)['results'][0]['GAZETTEER_ENTRY']

    return Point(result.get('GEOMETRY_X'), result.get('GEOMETRY_Y'))


def _distance(p1: Point, p2: Point) -> float:
    """calculate the distance between two points"""

    x_2, y_2 = ((i[0] - i[1])**2 for i in zip(p1, p2))

    return (x_2 + y_2)**0.5


def find_nearest(point: Point, targets: dict, n: int = 5) -> List[Feature]:
    """
    return the nearest n targets to point

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

    return sorted(distances)[:n]


transformer = Transformer.from_crs("EPSG:27700", "EPSG:4326")


def transform_points(features: List[Feature]) -> List[Feature]:
    """
    transform 'location' attribute in list of Features
    from EPSG:27700 to EPSG:4326 projection
    """

    for i in features:
        i.location = Point(*transformer.transform(*i.location))

    return features
