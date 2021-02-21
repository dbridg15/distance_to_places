import json
import os
import requests

# TODO: logging, better exception handling

OS_API_KEY = os.environ.get('OS_API_KEY')
DATA_DIR = 'data'


def get_train_stations():
    """
    use ordnance-surveys `OS Features API` to return all uk train stations as
    list of dictionaries in form:
    >>> [{'Station Name': (x_coord, y_coord)}, ...]
    """

    request = 'GetFeature'
    typeNames = 'Zoomstack_RailwayStations'
    count = 100
    startIndex = 0
    outputFormat = 'GEOJSON'

    url = ('https://api.os.uk/features/v1/wfs?service=wfs&version=2.0.0'
           f'&request={request}'
           f'&typeNames={typeNames}'
           f'&count={count}'
           f'&outputFormat={outputFormat}'
           f'&key={OS_API_KEY}'
           )

    out = requests.get(f'{url}&startIndex={startIndex}')

    features = []
    # keep paging through results until none more are returned
    while len(content := json.loads(out.content)['features']) > 0:

        startIndex += count
        features.extend(content)

        out = requests.get(f'{url}&startIndex={startIndex}')

    return {i['properties']['Name']: tuple(i['geometry']['coordinates'])
            for i in features}


if __name__ == '__main__':
    """if run as standalone script then save dictionary as json"""

    uk_train_stations = get_train_stations()

    filepath = os.path.join(DATA_DIR, 'uk_train_stations.json')

    with open(filepath, 'w') as f:
        json.dump(uk_train_stations, f)
