from flask import Flask
from flask import request, escape
import os

from distance_to_places import (load_features_data,
                                get_point,
                                find_nearest,
                                table_from_features,
                                create_map)


DATA_DIR = 'distance_to_places/data/'

current_dir = os.getcwd()
filepath = os.path.join(current_dir, DATA_DIR, 'uk_train_stations.json')



app = Flask(__name__)

@app.route("/")
def index():
    uk_train_stations = load_features_data(filepath)
    postcode = str(escape(request.args.get("postcode", "")))
    if postcode:
        nearest_n = nearest_n_from_postcode(postcode, uk_train_stations)
        table = table_from_features(nearest_n)
        m = create_map(nearest_n)._repr_html_()
    else:
        table = ""
        m = ""
    return (
        """<form action="" method="get">
                Enter Postcode: <input type="text" name="postcode">
                <input type="submit" value="Show nearest train stations">
            </form>"""
        + table
        + m
    )

def nearest_n_from_postcode(postcode, targets):
    point = get_point(postcode)
    return find_nearest(point, targets)

if __name__ == '__main__':
    app.run(debug=True)