from bokeh.palettes import Category20_16
from bokeh.models.widgets import CheckboxGroup, CheckboxButtonGroup
import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models.widgets import Slider, RangeSlider, Select
from bokeh.layouts import column, row, WidgetBox
from bokeh.models import Panel
import pandas as pd
from itertools import chain
from bokeh.models import FuncTickFormatter


def route_tab(data):
    def md(origin, dest):
        # sakhte dataset jadid baraye mabda va maghsad
        subset = data[(data['origin'] == origin) & (data['dest'] == dest)]
        # sakhte set az name airline ha va tabdil be list bedoone tekrari
        airlines = list(set(subset['name']))
        # sakhte list khali baraye data mehvare x
        xs = []
        # sakhte list khali baraye data mehvare y
        ys = []
        # sakhte dictionary baraye data haye vared shode
        dic = {}
        # joda kardane data name airline va takhir ha besoorate list index dar
        for i, j in enumerate(airlines):
            airline_flights = subset[subset['name'] == j]
            # ezafe kardane takhir ha be list mehvare x
            xs.append(list(airline_flights['arr_delay']))
            # ezafe kardane tedade airline ha be mehvare y
            ys.append([i for _ in range(len(airline_flights))])
            dic[i] = j
        # sakhte list besoorate chain dar mehvare x o y va list sazi ba *xs na besoorate (xyzcv..) (x, y, z, c, ...)
        xs = list(chain(*xs))
        ys = list(chain(*ys))
        # return data baraye plot az x o y m dictionary
        return ColumnDataSource(data = {'x': xs, 'y': ys}), dic

    def mp(src, o_init, d_init, dic):
        # sakhte figure
        p = figure()
        # sakhte nemodare noghtei ba x o y , data va size
        p.circle('x', 'y', source=src, size=10)
        # taeine mehvare x ba toole dictionary
        p.yaxis[0].ticker.desired_num_ticks = len(dic)
        # taeine mehvare y ba name har airline
        p.yaxis.formatter = FuncTickFormatter(
            code="""
            var labels = %s;
            return labels[tick];
            """ % dic
        )
        return p
    # function update
    def update(attr, old, new):
        # taeine mabda
        origin = os.value
        # taeine maghsad
        dest = ds.value
        # berooz resani mabda o maghsad
        new_src, new_dic = md(origin, dest)
        # berooz resani data haye source
        src.data.update(new_src.data)
        # taghire mehvare x ba toole data jadid dictionary
        p.yaxis[0].ticker.desired_num_ticks = len(new_dic)
        # taeine mehvare jadide y ba airline haye jadid dar dictionary
        p.yaxis.formatter = FuncTickFormatter(
            code="""
            var labels = %s;
            return labels[tick];
            """ % new_dic
        )
    # sakhte set az data jadid bedoone tekrari va tabdil be list
    origins = list(set(data['origin']))
    # sakhte set az data jadid bedoone tekdade az maghsad va tabdil be list
    dests = list(set(data['dest']))
    # sakhte listbox mabda va maghsad va taeine meghdar avalie
    os = Select(title='مبداها', value='EWR', options=origins)
    ds = Select(title='مقصدها', value='IAH', options=dests)
    # tanzime data jadid ba taghire list box va jaigozari dar function update
    os.on_change('value', update)
    ds.on_change('value', update)
    # taeine meghdare avalie baraye orgin o destination value
    o_init = os.value
    d_init = ds.value
    # jaigozari data haye avalie dar source o dictionary
    src, dic = md(o_init, d_init)
    # tanzimate figure ba source o data avalie origin o destination o dictionary
    p = mp(src, o_init, d_init, dic)
    # tanzime widget list box ba origin va destination
    w = WidgetBox(os, ds)
    l = row(w, p)
    # tanzime name tab
    tab = Panel(child=l, title='مبدا/مقصد')
    return tab
