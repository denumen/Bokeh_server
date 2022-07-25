from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from os.path import dirname, join
import pandas as pd
from hist import hist_tab
from table import table_tab
from route import route_tab

# read data
data = pd.read_csv('D:\Datasets\Flights\Flights.csv', index_col=0).dropna()


# read kardane tab haye mokhtalef
tab_hist = hist_tab(data)
tab_table = table_tab(data)
tab_route = route_tab(data)

# sakhte tab ha ba tab haye sakhte shode
tabs = Tabs(tabs=[tab_hist, tab_table, tab_route])

# ezafe kardane plot va tab ha be root
curdoc().add_root(tabs)
