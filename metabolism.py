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
    w = widgets[widget]

    if type(w) is RadioButtonGroup:
        index = widgets[widget].active
        return w.labels[index]

    if type(w) is Select or Slider:
        return w.value


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


def get_eq_tup():
    # Selected equation
    equation_name = get_widget_value('equation')

    # Look up equation info tuple based on equation name
    return eq_tup_D[equation_name]


def setup_equation():
    """ 
    """
    eq_T = get_eq_tup()
    equation = eq_T.Equation 

    parameters = get_eq_parameters()
    already_selected = get_widget_value('xaxis')

    keywords = [k for k in parameters if k is not already_selected]
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
    eq_partial = setup_equation()
    eq_T = get_eq_tup()

    values = ['weight', 'age', 'height']
    ranges = ['Weight_Range', 'Age_Range', 'Height_Range']

    x_start, x_stop = lookup_range()
    x = list(range(x_start,x_stop))
    y = [eq_partial(x_i) for x_i in x]

    p.line(x, y, line_width=2)
    # improve to version from equation_tuple.title
    p.xaxis.axis_label = "Placeholder"
    p.yaxis.axis_label = "Calories per Day RMR"
    p.title.text = "this should be a long title"

    layout = row(controls, p)
    curdoc().add_root(layout)
    # show(p)
    return p

def update(attr, old, new):
    layout.children[1] = create_figure()


# -----------------------------------------------------------------------------
# Initialize Widgets

# Setup
widgets = {}


# Equation Selection
labels = [eq.Name for eq in met_eq_tuples]
button = RadioButtonGroup(labels=labels, active=0)
button.on_change('active', update)
widgets['equation'] = button
eq_tup = eq_tup_D[labels[0]]


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
button = RadioButtonGroup(labels=labels, active=0)
button.on_change('active', update)
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

if get_widget_value('units') is 'Imperial':
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

if get_widget_value('units') is 'Imperial':
    start = kg_to_lb(start)
    end = kg_to_lb(end)
    title = "Weight (lb)"
else:
    title = "Weight (kg)"

value = (start + end)/2
button = Slider(start=start, end=end, value=value, step=1, title=title)
widgets['weight'] = button


# -----------------------------------------------------
# Initial call
create_figure()
