import os
import webbrowser

from distance_to_places import (load_features_data,
                                get_point,
                                find_nearest,
                                create_map)


DATA_DIR = 'distance_to_places/data/'

if __name__ == '__main__':

    current_dir = os.getcwd()
    filepath = os.path.join(current_dir, DATA_DIR, 'uk_train_stations.json')

    map_filename = 'index.html'
    map_url = f'file://{os.path.join(current_dir, map_filename)}'

    uk_train_stations = load_features_data(filepath)

    point = get_point(input('postcode: '))

    nearest_n = find_nearest(point, uk_train_stations, 10)

    m = create_map(nearest_n)

    m.save(map_filename)

    webbrowser.open(map_url)
