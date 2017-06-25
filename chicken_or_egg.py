from functools import partial
from collections import namedtuple

from bokeh.layouts import widgetbox, row, column
from bokeh.plotting import figure, curdoc, output_file
from bokeh.models import Slider, Select, RadioButtonGroup, HoverTool
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
    index = widgets[widget].value
    return widget.labels[index]


def get_eq_parameters():
    """ Return all equation parameters from equation name.
    """
    equation = get_widget_value(widgets['equation'])
    eq_tup = eq_tup_D[equation]
    return eq_tup.Parameters


def get_shown_widgets():
    """ Return subset of widgets shown based on equation parameters and xaxis 
    selections.
    """
    parameters = get_eq_parameters()
    already_selected = get_widget_value(widgets['xaxis'])
    options = [o for o in parameters if o is not already_selected]

    shown_widgets = widgets['equation'] + widgets['xaxis'] + options
    
    return shown_widgets

def setup_equation():
    """ 
    """

# -----------------------------------------------------------------------------
# Initialize Widgets

# Setup
widgets = {}


# Equation Selection
labels = [eq.Name for eq in met_eq_tuples]
button = RadioButtonGroup(labels=labels, active=0)
button.on_change('active', update)
widgets['equation'] = button
eq_tup = eq_tup_D[equation]


# Units Selection
# Units displayed for other widgets will be set based on this.
labels = ["Imperial", "Metric"]
button = RadioButtonGroup(labels=labels, active=0)
button.on_change('active', update)
widgets['units'] = button


# X-Axis Selection
# Selection is based on equation selected.
parameters = get_eq_parameters()

labels = [o for o in parameters if o is not 'sex']
button = Select(title="X-Axis", labels=labels, value=0)
button.on_change('active', update)
widgets['xaxis'] = button


# Sex Selection
labels = ['Male', 'Female']
button = RadioButtonGroup(labels=labels, active=0)
widgets['sex'] = button


# Age
start, stop = eq_tup.Age_Range
button = Slider(start=start, end=end, value=start, step=1, title="Age")
widgets['age'] = button


# Bodyfat
start, stop = cunningham_T.Bodyfat_Range
button = Slider(start=start,end=end,value=start,step=1,title="% Bodyfat")


# Height
start, stop = eq_tup.Height_Range

if get_widget_value('units') is 'Imperial':
    start = cm_to_inches(start)
    end = cm_to_inches(end)
    title = "Weight (inches)"
else:
    title = "Weight (cm)"

value = (start + end)/2
button = Slider(start=start, end=end, value=value, step=1, title=title)


# Weight
# Would prefer to limit this based on BMI
start, end = eq_tup.Weight_Range

if get_widget_value('units') is 'Imperial':
    start = kg_to_lb(start)
    end = kg_to_lb(end)
    title = "Weight (lb)"
else:
    title = "Weight (kg)"

value = (start + end)/2
button = Slider(start=start, end=end, value=value, step=1, title=title)




# -----------------------------------------------------------------------------


def create_figure():

    # bokeh plot
    hover = HoverTool(tooltips = [
        ("x, y", "xs, ys")
        ])

    p = figure(plot_height=600, plot_width=600, tools=[hover])

    # UI Widgets
    shown_widgets = get_shown_widgets()
    controls = widgetbox(shown_widgets, width=200)

    # Set up equation, x and y values based on UI values
    met_eq_partial = 

    y = [met_eq_partial(x_i) for x_i in x]

    p.line(x, y, line_width=2)
    # improve to version from equation_tuple.title
    p.xaxis.axis_label = x_parameter
    p.yaxis.axis_label = "Calories per Day RMR"
    p.title = "this should be a long title"
    # Determine units
    # units = units_labels[button_units.value]

    # Create widgets for remaining equation parameters
    # based on equation selected:
    # set widget boxes visible for remaining parameters
    # set units, ranges on widgets
    # set info, ref, desc
    # set ranges for parameters

    layout = row(controls, p)
    curdoc().add_root(layout)
    show(p)
    return p

def update(attr, old, new):
    layout.children[1] = create_figure()


# Equation Widget
# Other widgets will be set based on parameters, validated ranges for equation chosen.


# # Layout / Output

# layout = row(controls, create_figure())
# curdoc().add_root(layout)


