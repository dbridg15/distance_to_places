from flask import Flask, request, escape, render_template
import os

from distance_to_places import (load_features_data,
                                get_point,
                                find_nearest,
                                table_from_features,
                                create_map)


app = Flask(__name__)

DATA_DIR = 'distance_to_places/data/'

current_dir = os.getcwd()
filepath = os.path.join(current_dir, DATA_DIR, 'uk_train_stations.json')


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
    return render_template('index.html', table=table, m=m)


def nearest_n_from_postcode(postcode, targets):
    point = get_point(postcode)
    return find_nearest(point, targets)


if __name__ == '__main__':
    app.run(debug=True)
