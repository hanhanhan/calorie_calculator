from functools import partial
from collections import namedtuple

from bokeh.layouts import widgetbox, row, column
from bokeh.plotting import figure, curdoc
from bokeh.models import Slider, Select, RadioButtonGroup, HoverTool
from bokeh.models import ColumnDataSource
from bokeh.io import output_file, show

from metabolic_equations import *

# Things that should be linked:
# parameter, widget, values (if by index)
# eg sex, button_sex, ['male','female'] 


# 1. set up all buttons, eq, x axis with default values
# 2. update functions cascading eq -> units -> x-axis -> options
# 3. 

# -----------------------------------------------------------------------------
#
def get_widget_value(widget):
    """Return the named value from a widget button or toggle widget.
    """
    w = widgets[widget]

    if type(w) is RadioButtonGroup:
        index = widgets[widget].active
        return w.labels[index]

    if type(w) is Select or Slider:
        return w.value


def get_units(parameter):

    if get_widget_value('units_system') is 'Metric':
        if parameter is 'weight':
            return 'kg'
        if parameter is 'height':
            return 'cm'

    if get_widget_value('units_system') is 'Imperial':
        if parameter is 'weight':
            return 'lbs'
        if parameter is 'height':
            return 'inches' 


def get_eq_parameters():
    """ Return all equation parameters from equation name.
    """
    equation = get_widget_value('equation')
    eq_tup = eq_tup_D[equation]
    return eq_tup.Parameters


def get_shown_widgets():
    """ Return subset of widgets shown based on equation parameters and xaxis 
    selections.
    """
    parameters = get_eq_parameters()
    already_selected = get_widget_value('xaxis')
    options = [widgets[o] for o in parameters if o is not already_selected]

    shown_widgets = []
    shown_widgets.append(widgets['equation'])
    shown_widgets.append(widgets['xaxis'])
    shown_widgets += options
    
    return shown_widgets

def get_partial_parameters():
    parameters = get_eq_parameters()
    already_selected = get_widget_value('xaxis')

    return [k for k in parameters if k is not already_selected]


def get_eq_tup():
    # Selected equation
    equation_name = get_widget_value('equation')

    # Look up equation info tuple based on equation name
    return eq_tup_D[equation_name]


def setup_equation():
    """ Setup partial equation for chosen x axis.
    """
    eq_T = get_eq_tup()
    equation = eq_T.Equation 

    parameters = get_eq_parameters()
    already_selected = get_widget_value('xaxis')

    keywords = get_partial_parameters()
    values = [get_widget_value(k) for k in keywords]

    arguments = dict(zip(keywords, values))
    partial_eq = partial(equation, **arguments)

    return partial_eq


def lookup_range():
    """ Return the equation's validated range (min, max) 
    for the x-axis parameter chosen.
    """

    # Placeholder. Consider units.

    return (30,300)

def get_xy_data(eq_partial):
    x_start, x_stop = lookup_range()
    x = list(range(x_start,x_stop))
    y = [round(eq_partial(x_i)) for x_i in x]
    return [x,y]

# -----------------------------------------------------------------------------


def create_figure():

    # UI Widgets
    shown_widgets = get_shown_widgets()
    controls = widgetbox(shown_widgets, width=200)

    xaxis = get_widget_value('xaxis')
    units_system = get_widget_value('units_system')
    units = get_units(xaxis)

    # update_data() ? this part is all the same but i'm not sure what to do about arguments
    eq_partial = setup_equation()
    eq_T = get_eq_tup()

    source.data['x'], source.data['y'] = get_xy_data(eq_partial)

    # Bokeh Plot
    hover = HoverTool(tooltips = [('Weight','$x{0}'), 
        ("Calories", "$y{0}")
        ])

    p = figure(plot_height=600, plot_width=600, tools=[hover])
    line = p.line('x', 'y', source=source, line_width=2)
    
    # improve to version from equation_tuple.title
    p.xaxis.axis_label = "{} ({})".format(xaxis.capitalize(), units)
    p.yaxis.axis_label = "Calories per Day RMR"
    p.title.text = "this should be a long title"

    update_layout = row(controls, p)
    # show(p)
    return update_layout


def update_data(attr, old, new):

    # Set up equation, x and y values based on UI values
    eq_partial = setup_equation()

    # get from existing graph
    x_start, x_stop = lookup_range()
    x = list(range(x_start,x_stop))
    y = [round(eq_partial(x_i)) for x_i in x]
    source.data['x'], source.data['y'] = get_xy_data(eq_partial)


def update_plot(attr, old, new):

    update_layout = create_figure()
    curdoc().clear()
    curdoc().add_root(update_layout)




# -----------------------------------------------------------------------------
# Initialize Widgets

# Setup
widgets = {}


# Equation Selection
labels = [eq.Name for eq in met_eq_tuples]
button = RadioButtonGroup(labels=labels, active=0)
button.on_change('active', update_plot)
widgets['equation'] = button
eq_tup = eq_tup_D[labels[0]]


# Units Selection
# Units displayed for other widgets will be set based on this.
labels = ["Imperial", "Metric"]
button = RadioButtonGroup(labels=labels, active=0)
button.on_change('active', update_plot)
widgets['units_system'] = button


# X-Axis Selection
# Selection is based on equation selected.
parameters = get_eq_parameters()

labels = [o for o in parameters if o is not 'sex']
button = RadioButtonGroup(labels=labels, active=0)
widgets['xaxis'] = button


# Sex Selection
labels = ['Male', 'Female']
button = RadioButtonGroup(labels=labels, active=0)
widgets['sex'] = button


# Age
start, end = eq_tup.Age_Range
button = Slider(start=start, end=end, value=start, step=1, title="Age")
widgets['age'] = button


# Bodyfat
start, end = cunningham_T.Bodyfat_Range
button = Slider(start=start,end=end,value=start, step=1,title="% Bodyfat")
widgets['bodyfat'] = button


# Height
start, end = eq_tup.Height_Range

if get_widget_value('units_system') is 'Imperial':
    start = cm_to_inches(start)
    end = cm_to_inches(end)
    title = "Height (inches)"
else:
    title = "Height (cm)"

value = round((start + end)/2)
button = Slider(start=start, end=end, value=value, step=1, title=title)
widgets['height'] = button


# Weight
# Would prefer to limit this based on BMI
start, end = eq_tup.Weight_Range

if get_widget_value('units_system') is 'Imperial':
    start = kg_to_lb(start)
    end = kg_to_lb(end)
    title = "Weight (lbs)"
else:
    title = "Weight (kg)"

value = (start + end)/2
button = Slider(start=start, end=end, value=value, step=1, title=title)
widgets['weight'] = button

for key in widgets:

    w = widgets[key]

    if type(w) is Slider:
        w.on_change('value', update_data)
    
    if type(w) is RadioButtonGroup or type(w) is Select:
        w.on_change('active', update_plot)


# -----------------------------------------------------
# Initial call

# Get x (or y) data from line (glyph)
# documentation looks like you can use 'x' hmmmmmm
# l.data_source.data['x']
# examples use ColumnDataSource dictionary
#
source = ColumnDataSource({'x':[], 'y':[]})
layout = create_figure()

# globals - document, layout, glyph?, source,

curdoc().add_root(layout)
curdoc().title = "Resting Metabolism Rate"
