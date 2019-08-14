from bokeh.models import GMapOptions
from bokeh.models import Panel
from bokeh.plotting import gmap


def geo_tab(df):
    df_sample = df.sample(frac=.25)    # Show 25% of the records, otherwise the map will be slow.
    map_options = GMapOptions(lat=47.335728, lng=4.115118, map_type="roadmap", zoom=5)

    api_key = "AIzaSyAhJoQsJr9IdsbXthpM4i84HsYvJtXxLXc"

    # Output backend WebGL for better performance.
    p = gmap(api_key, map_options, title="Austin", output_backend="webgl")

    data = dict(lat=df_sample['lat'],
                lon=df_sample['lng'])

    p.circle(x="lon", y="lat", size=12, fill_color="blue", fill_alpha=0.8, source=data)

    tab = Panel(child=p, title='Review Locations')
    return tab
