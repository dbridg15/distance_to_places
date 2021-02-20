import folium
from folium.plugins import FloatImage
import os
import datetime
from typing import List
from dtypes import Feature


OS_API_KEY = os.environ.get('OS_API_KEY')


def create_map(features: List[Feature]) -> folium.Map:
    """
    creates a leaflet map, centred on and with markers for supplied features

    uses `OS Maps API` for map tiles

    Parameters
    ----------
    features : List[Feature]
        list of features to add as markers to the map

    Returns
    -------
    folium.Map
        a folium (leaflet) map object
    """

    base_path = 'https://api.os.uk'

    layer = 'Light_3857'

    endpoint_path = f'/maps/raster/v1/zxy/{layer}/{{z}}/{{x}}/{{y}}.png?'

    zxy_path = f'{base_path}{endpoint_path}key={OS_API_KEY}'

    # Obtain current date-time
    date = datetime.date.today()
    os_attr = f'Contains OS data © Crown copyright and database right {date}'

    # Create a new Folium map
    # Ordnance Survey basemap using the OS Data Hub OS Maps API
    # Zoom levels 7 - 16 correspond to the open data zoom scales only
    m = folium.Map(min_zoom=7,
                   max_zoom=16,
                   tiles=zxy_path,
                   attr=os_attr,
                   )

    # OS logo image
    logo = 'os-logo-maps.svg'
    logo_url = f'https://labs.os.uk/public/os-api-branding/v0.2.0/img/{logo}'
    # Folium FloatImage plugin for displaying an image on the map
    float_image = FloatImage(logo_url, bottom=1, left=1)
    _ = float_image.add_to(m)

    for f in features:

        popup = (f'<b>Station Name:</b> {f.name}<br />'
                 f'<b>Distance:</b> {int(f.distance)}m<br />'
                 f'<b>LatLong:</b> {str(f.location)}')

        folium.Marker(location=f.location,
                      popup=popup).add_to(m)

    m.fit_bounds([f.location for f in features])

    return m
