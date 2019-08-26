from bokeh.plotting import figure
from bokeh.models import Panel
import pandas as pd


def count_tab(df):
    df['Review_Date'] = pd.to_datetime(df['Review_Date'], format='%m/%d/%Y')
    df_date_count = df["Review_Date"].dt.date.value_counts()
    df_date_count = df_date_count.to_frame()
    df_date_count = df_date_count.rename(columns={'Review_Date': 'Reviews'})
    df_date_count.index.names = ['Date']
    df_date_count.sort_index(inplace=True)

    test = df_date_count['Reviews']
    p = figure(plot_width=400, plot_height=400, x_axis_type='datetime')
    p.line(df_date_count.index, test, line_width=2)

    tab = Panel(child=p, title='Review Count')
    return tab
