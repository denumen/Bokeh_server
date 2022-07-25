import pandas as pd
import numpy as np
from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable


def table_tab(data):
    # group kardane data bar asase describe ke neshon dahandeye name counr charak ha va miangin o ... ast
    d = data.groupby('name')['arr_delay'].describe()
    # tanzimate adade ashari ta 1ragham
    d['mean'] = d['mean'].round(1)
    # tanzimat raghame ashari ta 1ragham
    d['std'] = d['std'].round(1)
    # reset kardane index be 0 1 2 ...
    d = d.reset_index()
    # sakhte table baraye tabe data
    c = ColumnDataSource(d)
    flights_table = DataTable(
        # tanzime source data ha
        source=c,
        # tanzimate sotoon ha
        columns=[
            TableColumn(field='name', title='ایرلاین'),
            TableColumn(field='count', title='تعداد پرواز'),
            TableColumn(field='mean', title='میانگین تاخیر'),
            TableColumn(field='std', title='انحراف استاندارد تاخیر'),
            TableColumn(field='min', title='کمینه‌ی تاخیر'),
            TableColumn(field='25%', title='۲۵٪'),
            TableColumn(field='50%', title='۵۰٪'),
            TableColumn(field='75%', title='۷۵٪'),
            TableColumn(field='max', title='بیشنیه‌ی تاخیر'),

        ],
        width=1500
    )
    tab = Panel(child=flights_table, title='خلاصه‌ی تاخیرها')
    return tab
