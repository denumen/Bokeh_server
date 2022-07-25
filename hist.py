from bokeh.palettes import Category20_16
from bokeh.models.widgets import CheckboxGroup, CheckboxButtonGroup
import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models.widgets import Slider, RangeSlider
from bokeh.layouts import column, row, WidgetBox
from bokeh.models import Panel
import pandas as pd


# sakhte function baraye tabe histogram
def hist_tab(data):

# sakhte function baraye daryafte data ha va baze takhir az -60 ta 120 min va tanzime bin baraye histogram
    def md(s_data, rs=-60, re=120, bin=10):
# sakhte dataframe baraye sotoon haye data histogram
        d = pd.DataFrame(columns=['proportion', 'left', 'right', 'f_proportoin', 'f_interval', 'name', 'color'])
# mohasebe baze takhir
        r = re - rs
        for i, r_data in enumerate(s_data):
            # joda kardane data haye har sherkat havapeymai va index kardane tedade harkodoom
            subset = data[data['name'] == r_data]
            # tanzimate mehvare x ha be nesbate mizane takhir ba nesbate bins va range takhir
            arr_hist, edge = np.histogram(subset['arr_delay'], bins=int(r / bin), range=(rs, re))
            # sakhte dataframe az dataset baraye histogram
            arr_df = pd.DataFrame({
                'proportion': arr_hist / np.sum(arr_hist), 'left': edge[:-1], 'right': edge[1:]
            })
            # tanzime adade ashari ta 2ragham
            arr_df['f_proportoin'] = ['%0.5f' % p for p in arr_df['proportion']]
            #
            arr_df['f_interval'] = ['%d to %d minutes' % (left, right) for left, right in zip(arr_df['left'], arr_df['right'])]
            # daryafte name az r_data
            arr_df['name'] = r_data
            # tanzimate rangbandi
            arr_df['color'] = Category20_16[i]
            d = d.append(arr_df)
        # data haro az chap sort mikonim
        d = d.sort_values(['name', 'left'])
        d = ColumnDataSource(d)
        return d

    def mp(s_data):
        # rasme plot ba name takhir parvaz va tanzime tool o arz
        p = figure(plot_width=700, plot_height=700, title='تاخیر در پرواز')
        # chon bala tanzim kardim histogram hast nemoodar inja az quad estefade mikonim va tanzimat midim
        p.quad(source=s_data, bottom=0, top='proportion', left='left', right='right', color='color', fill_alpha=0.7,
               legend_field='name')
        return p

    def update(attr, old, new):
        # tanzimate checkbox
        air_lines_checked = [chbox.labels[i] for i in chbox.active]
        # daryafte value haye slider va airline haye tik khorde va taghire data
        ds = md(air_lines_checked, range_slider.value[0], range_slider.value[1], slider.value)
        src.data.update(ds.data)



    # liste airline ha tabdil be set baraye hazfe tekrari ha va tabdil be list dobare
    air_lines = list(set(data['name']))
    # moratab sazi airline ha
    air_lines.sort()
    # list kardane rang ha
    colors = list(Category20_16)
    # moratab kardane rang ha
    colors.sort()
    # tanzime checkbox avalie ruye airline 0 o 1
    chbox = CheckboxGroup(labels=air_lines, active=[0, 1])
    # tanzime active va update kardane cheeckbox
    chbox.on_change('active', update)
    # ezafe kardane slider bins
    slider = Slider(start=1, end=30, step=1, value=5, title='دانه‌بندی هیستوگرام')
    # tanzimate update slider
    slider.on_change('value', update)
    # tanzimate slider baraye baze takhir ha
    range_slider = RangeSlider(start=-60, end=180, value=(-60, 120), step=5, title='بازه‌ی تاخیرها')
    range_slider.on_change('value', update)
    ###
    init_data = [chbox.labels[i] for i in chbox.active]
    src = md(init_data)
    p = mp(src)

    w = WidgetBox(chbox, slider, range_slider)
    l = row(w, p)
    tab = Panel(child=l, title='پنل هیستوگرام')
    return tab
