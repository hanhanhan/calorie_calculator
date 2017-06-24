from functools import partial
from collections import namedtuple

from bokeh.layouts import widgetbox, row, column
from bokeh.plotting import figure, curdoc, output_file
from bokeh.models import Slider, Select, RadioButtonGroup, HoverTool
from bokeh.io import output_file, show

controls =  None
x_options = ['Height', 'Weight', 'Age']
# 1 choose x axis parameter
# 2 choose values for other two parameters

# starting values

# eq_value
# units_value
# age_value
# height_value
# weight_value
# sex_value
# bf_value

    # # get x axis variable
    # xs = parameters[x.value]
    # x_axis_label = x.value

    # # get values for other two variables
    # for option in x_options:
    #     # one of these won't work
    #     # if option is not x.value:
    #     age = slider_age.value
    #     height = slider_height.value
    #     sex = button_sex.active != 1
    #     equation = button_equation.active

# height = 200 # cm
# age = 40 
# sex = namedtuple()
# equation = mifflin

# 4ft up to 9ft
MIN_HEIGHT = 122
MAX_HEIGHT = 272
HEIGHTS = list(range(MIN_HEIGHT, MAX_HEIGHT))

# range from study
MIN_AGE = 19
MAX_AGE = 78
AGES = list(range(MIN_AGE, MAX_AGE))

# validate not below normal BMI
WEIGHTS = list(range(35, 200))

parameters = {'Height': HEIGHTS, 'Age': AGES, 'Weight': WEIGHTS}

# -----------------------------------------------------------------------------
# Metabolic Equations for Resting Metabolic Rate

def mifflin(weight=None, height=None, age=None, sex=None):
    """Basal metabolic rate in calories
    based on weight in kg, height in cm, and
    sex (male = 1, female = 0)
    """
    return 9.99 * weight + 6.25 * height - 4.92 * age + 166 * sex - 161

# instead of partials?
def harris_benedict(weight=None, height=None, age=None, sex=None):
    """Resting metabolic rate in calories
    based on weight in kg, height in cm, and
    sex (male = 1, female = 0)
    """
    if sex is 1:
        return 66.5 + 13.75 * weight + 5.003 * height - 6.755 * age
    if sex is 0:
        return 655.1 + 9.563 * weight + 1.850 * height - 4.676 * age

def cunningham(weight=None, bf=None):
    """Resting metabolic rate in calories
    based on weight in kg and percent body fat
    """
    return (weight - weight * bf * 0.01) * 21.6 + 500

def schofield(age=None, weight=None, sex=None):
    """Resting metabolic rate based on on weight in kg, age, and
    sex (male = 1, female = 0)
    """
    # ugh update from kilojoules

    # Females
    if sex is 1:
        if age >= 60:
            return 38 * weight + 2755
        if age >= 30 and age < 60:
            return 34 * weight + 3538
        if age >= 18 and age < 30:
            return 62 * weight + 2036
        if age >= 10 and age < 18:
            return 244 * weight - 130
        if age >= 3 and age < 10:
            85 * weight + 2033

    # Males
    if sex is 0:
        if age >= 60:
            return 49 * weight + 2459
        if age >= 30 and age < 60:
            return 48 * weight + 3653
        if age >= 18 and age < 30:
            return 63 * weight + 2896
        if age >= 10 and age < 18:
            return 74 * weight + 2754
        if age >= 3 and age < 10:
            return 95 * weight + 2110


met_eq_functions = [mifflin, harris_benedict, cunningham, schofield]
sex_values = ['Male', 'Female']

T = namedtuple('equation_tuple',['Name', 'Equation', 'Standard_Error', 
    'Parameters', 'Description', 'References', 'Age_Range', 'Weight_Range', 
    'Height_Range', 'Bodyfat_Range'])


# not sure if this works w/ multiple lines
# T = namedtuple('equation_tuple','Name Equation Standard_Error Parameters Description', 
#     'References Age_Range Weight_Range Height_Range')


mifflin_T = T(
    Name = "Mifflin",
    Equation = mifflin,
    Standard_Error = (0.1),
    Parameters = ['weight', 'age', 'height', 'sex'],
    Description = None,
    References= None,
    Age_Range = (18,80),
    Weight_Range = (30, 200),
    Height_Range = (122,272),
    Bodyfat_Range = None
    )

harris_benedict_T = T(
    Name = "Harris Benedict",
    Equation = harris_benedict,
    Standard_Error = (0.1),
    Parameters = ['weight', 'age', 'height', 'sex'],
    Description = None,
    References= None,
    Age_Range = (18,80),
    Weight_Range = None,
    Height_Range = (122,272),
    Bodyfat_Range = None
    ) 

cunningham_T = T(
    Name = "Cunningham",
    Equation = cunningham,
    Standard_Error = (0.1),
    Parameters = ['weight', 'bodyfat'],
    Description = 'For bodybuilders with low percent bodyfat.',
    References= None,
    Age_Range = (18,80),
    Weight_Range = None,
    Height_Range = (122,272),
    Bodyfat_Range = (4,25)
    )

schofield_T = T(
    Name = "Schofield",
    Equation = schofield,
    Standard_Error = (0.1),
    Parameters = ['weight', 'age'],
    Description = 'WHO',
    References= None,
    Age_Range = (3,80),
    Weight_Range = None,
    Height_Range = (122,272),
    Bodyfat_Range = None
    )

# also include error, age range, weight range?, height range? in tuple?

# -----------------------------------------------------------------------------

def cm_to_inches(cm):
    return 0.3937 * cm

def kg_to_lb(kg):
    return 2.20462 * kg

def bmi(weight, height):
    return weight / (0.01 * 0.01 * height * height)

def underweight(bmi):
    return bmi < 19

# -----------------------------------------------------------------------------
# Configure Widgets

# x axis
def select_x_axis(equation_tuple):
    options = [v for v in equation_tuple.Parameters if v is not 'sex']
    picker_x_axis = Select(title='X-Axis', value=0, 
        options=options)
    picker_x_axis.on_change('value', update)
    return picker_x_axis

def get_min_max(value, equation_tuple):

    if value is 'weight':
        x_min = min(equation_tuple.Weight_Range)
        x_max = max(equation_tuple.Weight_Range)
        # return equation_tuple.Weight_Range
        
    elif value is 'age':
        x_min = min(equation_tuple.Age_Range)
        x_max = max(equation_tuple.Age_Range)
        # return equation_tuple.Age_Range

    elif value is 'height':
        x_min = min(equation_tuple.Height_Range)
        x_max = max(equation_tuple.Height_Range)
        # return equation_tuple.Height_Range

    # else? i'd prefer as a check
    else: #  x_axis is 'bodyfat'
        x_min = min(equation_tuple.Bodyfat_Range)
        x_max = max(equation_tuple.Bodyfat_Range)
        # return equation_tuple.Bodyfat_Range

    return [x_min, x_max]

def get_current_value(value): # units!
    if value is 'weight':
        return slider_weight.value
        
    if value is 'age':
        return slider_age.value

    if value is 'height':
        return slider_height.value

    if value is 'bodyfat':
        return slider_bf.value

    if value is 'sex':
        return sex_values.index(button_sex.value)


def update_widgets(units, equation_tuple, parameters):
    """Change units displayed based on user selected units (imperial or metric),
    and equation ranges of validity for age, weight, height.
    """
    # update to use ranges in tuples throughout

    if 'age' in parameters:
    # if equation_tuple.Age_Range and 'age' in parameters:
        min_age, max_age = get_min_max('age', equation_tuple)

        slider_age = Slider(start=min_age, end=max_age, value=min_age, step=1, title="Age")
        slider_age.on_change('value', update)
        widgets.append(slider_age)
    
    if 'height' in parameters:
    # if equation_tuple.Height_Range and 'height' in parameters:
        min_height, max_height = get_min_max('height', equation_tuple)
        height_title = "Height (cm)"

        if units is 'Imperial':
            min_height = cm_to_inches(min_height)
            max_height = cm_to_inches(max_height)
            height_title = "Height (in)"

        slider_height = Slider(start=min_height, end=max_height, value=min_height, step=1, title="Height")
        slider_height.on_change('value', update)

        widgets.append(slider_height)

    # verify against bmi
    if 'weight' in parameters:
        min_weight = 20
        max_weight = 200
        weight_title = "Weight (kg)"

        if units is 'Imperial':
            min_weight = kg_to_lb(min_weight)
            max_weight = kg_to_lb(max_weight)
            weight_title = "Weight (lb)"

        slider_weight = Slider(start=min_weight, end=max_weight, value=min_weight, step=1, title=weight_title)
        slider_weight.on_change('value', update)

    if 'sex' in parameters:
        button_sex = RadioButtonGroup(labels=sex_values, active=1)
        button_sex.on_change('active', update)

        widgets.append(button_sex)

    if 'bodyfat' in parameters:
        min_bf = 5
        # find out study validated range, prob not validated for higher body fat %s
        max_bf = 20
        slider_bf = Slider(start=min_bf, end=max_bf, value=min_bf, step=0.2, title="% Bodyfat")
        slider_bf.on_change('active', update)

        widgets.append(slider_bf)


def create_figure():

    # bokeh plot
    hover = HoverTool(tooltips = [
        ("x, y", "xs, ys")
        ])

    p = figure(plot_height=600, plot_width=600, tools=[hover])

    # Widgets
    # widgets = [], append units + equation up here? global?
    # make values 'sticky' between widget updates
    # will need to separate out weight to make sure only plotting for min normal bmi
    # verify % bodyfat ranges, other ranges

    # Which metabolic equation is selected
    equation_tuple = met_eq_tuples[button_equation.active]

    # Set x-axis options based on metabolic equation parameters
    x_axis_picker = select_x_axis(equation_tuple)
    widgets.append(x_axis_picker)

    # Translate from indices to named value
    x_parameter = equation_tuple.Parameters[x_axis_picker.value]
    x_min, x_max = get_min_max(x_parameter, equation_tuple)
    x = list(range(x_min, x_max))

    # arguments_D = { k:v for k in additonal_parameters for v in get_current_value(k) }
    
    arguments_D = {}
    for k in additonal_parameters:
        arguments_D[k] = get_current_value(k)

    met_eq_partial = partial(equation_tuple.Equation(), arguments_D)

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
    additonal_parameters = [
        p for p in equation.Parameters 
        if equation.Parameters.index(p) is not x_axis_picker.value
        ]

    update_widgets(units, equation_tuple, additional_parameters)
 
    controls = widgetbox(widgets, width=200)


    # Layout / Output

    layout = row(controls, p)
    curdoc().add_root(layout)
    show(p)
    return p

def update(attr, old, new):
    layout.children[1] = create_figure()


# Equation Widget
# Other widgets will be set based on parameters, validated ranges for equation chosen.

met_eq_labels = ["Mifflin St Jeor", "Harris Benedict", "Cunningham", "Schofield"]
# met_eq_functions = [mifflin, harris_benedict, cunningham, schofield]
met_eq_tuples = [mifflin_T, harris_benedict_T, cunningham_T, schofield_T]
sex_values = [ "Male", "Female"]

button_equation = RadioButtonGroup(labels=met_eq_labels, active=0)
button_equation.on_change('active', update)
widgets = []
widgets.append(button_equation)

# Units Widget
# Units displayed for other widgets will be set based on this.
units_labels = ["Imperial", "Metric"]
button_units = RadioButtonGroup(labels=units_labels, active=0)
button_units.on_change('active', update)
widgets.append(button_units)

create_figure()
# # Layout / Output

# layout = row(controls, create_figure())
# curdoc().add_root(layout)


