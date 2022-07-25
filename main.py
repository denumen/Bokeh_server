from random import random
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from bokeh.models import Button
from bokeh.layouts import column

# sakhte figure ba x o y az 0ta 100
p = figure(x_range=(0, 100), y_range=(0, 100), )

# sakhte result baraye click ruye button
result = p.text(x=[], y=[], text=[], text_color=[])

# sakhte array datasource
Data_Source = result.data_source

# sakhte button
button = Button(label='ثبت')

# sakhte i baraye pallete rangi
i = 0

# sakhte class baraye click button ke be array harbar click kardan x o y ra moshakhas mikonad va rang +1 mishe ta 3ta
# va tekrar mishe va matni ke bayaad ruye nemodar neshoon dade beshe va chasboondan be datasource
def click_button():
    global i
    new_data = dict()
    new_data['x'] = Data_Source.data['x'] + [random()*70 + 15]
    new_data['y'] = Data_Source.data['y'] + [random()*70 + 15]
    new_data['text'] = Data_Source.data['text'] + [str(random()*70)]
    new_data['text_color'] = Data_Source.data['text_color'] + [RdYlBu3[i % 3]]
    Data_Source.data = new_data
    print(new_data)
    i = i+1


# ezafe kardane function be button
button.on_click(click_button)

# ezafe kardane figure va dokme be safhe root
curdoc().add_root(column(button, p))

# run kardane servere bokeh
# cd folderi ke tush hastim ... cd bokeh_server
# bokeh serve --show main.py ya flights.py ya ....