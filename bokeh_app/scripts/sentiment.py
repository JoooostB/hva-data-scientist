from math import pi
import pandas as pd

from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.models import Panel

output_file("pie.html")


def sentiment_tab(df):
    sentiment_count = df["Sentiment"].value_counts()
    x = {
        'Positive': sentiment_count.iloc[0],
        'Negative': sentiment_count.iloc[1]
    }
    chart_colors = ['#DAF7A6', '#FF5733']

    data = pd.Series(x).reset_index(name='value').rename(columns={'index':'sentiment'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi

    data['color'] = chart_colors[:len(x)]

    p = figure(plot_height=350, title="Sentiment Chart", toolbar_location=None,
               tools="hover", tooltips="@sentiment: @value", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='sentiment', source=data)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None
    tab = Panel(child=p, title='Sentiment Chart')
    return tab
