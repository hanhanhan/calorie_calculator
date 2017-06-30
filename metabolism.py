from functools import partial
from collections import namedtuple, OrderedDict

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
# UI Widgets


def get_widget_value(widget):
    """Return the named value from a widget button or toggle widget.
    """
    w = widgets[widget]

    if type(w) is RadioButtonGroup:
        index = widgets[widget].active
        return w.labels[index]

    if type(w) is Select or Slider:
        return w.value


def set_widget_value(widget):
    ''' Used to update ranges on button
    '''    
    # w = widgets[widget]

    # if widget = 'xaxis':
    # #  button has start, end, value
    # button = RadioButtonGroup(labels=labels, active=0)
    # widgets['xaxis'] = button
    # if type(w) is RadioButtonGroup:
    #     index = widgets[widget].active
    #     return w.labels[index]

    # if type(w) is Select or Slider:
    #     return w.value
    pass


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
    return eq_tup.parameters


def get_shown_widgets():
    """ Return subset of widgets shown based on equation parameters and xaxis 
    selections.
    """
    parameters = get_eq_parameters()
    # Here! xaxis may not be in new parameter set
    already_selected = get_widget_value('xaxis')
    options = {k: widgets[k] for k in parameters if k is not already_selected}

    shown_widgets = OrderedDict()
    shown_widgets['equation'] = widgets['equation']
    shown_widgets['xaxis'] = widgets['xaxis']
    shown_widgets.update(options)
    
    return shown_widgets


def get_partial_parameters():
    parameters = get_eq_parameters()
    # Here!
    already_selected = get_widget_value('xaxis')

    return [k for k in parameters if k is not already_selected]


def update_widgets(shown_widgets):

    # update range of sliders based on range of validity for equation
    for widget in shown_widgets:

        if widget in ['age', 'weight', 'height', 'bodyfat']:

            start, end = lookup_range(widget)

            conversion = {'lbs': kg_to_lb, 'inches': cm_to_inches}

            if (get_widget_value('units_system') is 'Imperial' 
            and get_units(widget) in ['lbs', 'kg']):

                units = get_units(widget)

                eq = conversion[units]
                start = eq(start)
                end = eq(end)

            shown_widgets[widget].start = start
            shown_widgets[widget].end = end
            # I would prefer to make this sticky, with units conversion
            shown_widgets[widget].end = round((start + end)/2)



def get_eq_tup():
    # Selected equation

    equation_name = get_widget_value('equation')

    # Look up equation info tuple based on equation name
    return eq_tup_D[equation_name]


def setup_equation():
    """ Setup partial equation for chosen x axis.
    """
    eq_T = get_eq_tup()
    equation = eq_T.equation 

    parameters = get_eq_parameters()
    already_selected = get_widget_value('xaxis')

    keywords = get_partial_parameters()
    values = [get_widget_value(k) for k in keywords]

    arguments = dict(zip(keywords, values))
    partial_eq = partial(equation, **arguments)

    return partial_eq


def lookup_range(parameter=None):
    """ Return the equation's validated range (min, max) 
    for the parameter chosen. Default is for xaxis.
    """
    if parameter is None:
        parameter = get_widget_value('xaxis')
     
    # lookup range of parameter from tuple by naming scheme
    for field in tuple_fields:
        if parameter in field and 'range' in field:
            i = tuple_fields.index(field)
            eq_T = get_eq_tup()
            return eq_T[i]

    print('not found')


def get_xy_data(eq_partial):

    x_start, x_stop = lookup_range()

    x = list(range(x_start,x_stop))

    eq_partial = setup_equation()

    xaxis = get_widget_value('xaxis')

    args_list = [{xaxis: x_i} for x_i in x]
    y = [eq_partial(**d) for d in args_list]
    return {'x': x, 'y': y}

def get_title_specifics():
    # Using the _ equation - equation Mifflin None 
    # No - xaxis weight None 
    # at height _ (in) height 78 inches 
    # at _ years - age 18 None 
    # for a _ - sex Male None 
    # pass
    parameters = get_eq_parameters()

    info = 'using the {} equation '.format(get_eq_tup().name)

    if 'sex' in parameters:
        sex_info = 'for a {} '.format(get_widget_value('sex'))
        info += sex_info

    if 'height' in parameters and not get_widget_value('xaxis'):
        height_info = 'at height {} {} '.format(get_widget_value('height'), get_units('height'))
        info += height_info
     
    if 'weight' in parameters and not get_widget_value('xaxis'): 
        weight_info = 'at weight {} {} '.format(get_widget_value('weight'), get_units('weight'))
        info += weight_info 

    if 'age' in parameters: 
        age_info = 'at {} years '.format(get_widget_value('age'))
        info += age_info
    
    return info

# -----------------------------------------------------------------------------


def create_figure():

    # UI Widgets

    # Update xaxis if new equation does not it as parameter
    if get_widget_value('xaxis') not in get_eq_parameters():
        widgets['xaxis'].value = 0

    shown_widgets = get_shown_widgets()
    
    # update ranges displayed and units
    update_widgets(shown_widgets)

    # get list of equation parameters
    # check xaxis value is in equation parameters
    
    controls = widgetbox(list(shown_widgets.values()), width=200)

    xaxis = get_widget_value('xaxis')

    units_system = get_widget_value('units_system')
    units = get_units(xaxis)

    # update_data() ? this part is all the same but i'm not sure what to do about arguments
    eq_partial = setup_equation()

    eq_T = get_eq_tup()

    source.data = get_xy_data(eq_partial)


    # Bokeh Plot
    hover = HoverTool(tooltips = [('Weight','$x{0}'), 
        ("Calories", "$y{0}")
        ])

    p = figure(plot_height=600, plot_width=600, tools=[hover])
    line = p.line('x', 'y', source=source, line_width=2)
    
    # improve to version from equation_tuple.title
    p.xaxis.axis_label = "{} ({})".format(xaxis.capitalize(), units)
    p.yaxis.axis_label = "Calories per Day RMR"

    title_specifics = get_title_specifics()

    p.title.text = "RMR vs {} {}".format(xaxis.capitalize(), title_specifics)

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
    source.data = get_xy_data(eq_partial)


def update_plot(attr, old, new):
    # update widgets including xaxis default value, ranges
    update_layout = create_figure()
    curdoc().clear()
    curdoc().add_root(update_layout)




# -----------------------------------------------------------------------------
# Initialize Widgets

# Setup
widgets = {}


# Equation Selection
labels = [eq.name for eq in met_eq_tuples]
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

labels = [o for o in parameters if o is not 'sex' and o is not 'units_system']
button = RadioButtonGroup(labels=labels, active=0)
widgets['xaxis'] = button


# Sex Selection
labels = ['Male', 'Female']
button = RadioButtonGroup(labels=labels, active=0)
widgets['sex'] = button


# Age
start, end = eq_tup.age_range
button = Slider(start=start, end=end, value=start, step=1, title="Age")
widgets['age'] = button


# Bodyfat
start, end = cunningham_T.bodyfat_range
button = Slider(start=start,end=end,value=start, step=1, title="% Bodyfat")
widgets['bodyfat'] = button


# Height
start, end = eq_tup.height_range

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
start, end = eq_tup.weight_range

if get_widget_value('units_system') is 'Imperial':
    start = kg_to_lb(start)
    end = kg_to_lb(end)
    title = "Weight (lbs)"
else:
    title = "Weight (kg)"

value = (start + end)/2
button = Slider(start=start, end=end, value=value, step=1, title=title)
widgets['weight'] = button

# Widget Event Listeners
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
