from functools import partial
from collections import namedtuple

from bokeh.layouts import widgetbox, row, column
from bokeh.plotting import figure, curdoc, output_file
from bokeh.models import Slider, Select, RadioButtonGroup, HoverTool
from bokeh.io import output_file, show


x_options = ['Height', 'Weight', 'Age']
# 1 choose x axis parameter
# 2 choose values for other two parameters

# starting values

eq_value
units_value
age_value
height_value
weight_value
sex_value
bf_value

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

def harris_benedict(weight=None, height=None, age=None, sex=None):
    """Resting metabolic rate in calories
    based on weight in kg, height in cm, and
    sex (male = 1, female = 0)
    """
    if sex is 1:
        return 66.5 + 13.75 * weight + 5.003 * height – 6.755 × age
    if sex is 0:
        return 655.1 + 9.563 * weight + 1.850 * height – 4.676 * age

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
        if age >= 30 && age < 60:
            return 34 * weight + 3538
        if age >= 18 && age < 30:
            return 62 * weight + 2036
        if age >= 10 && age < 18:
            return 244 * weight - 130
        if age >= 3 && age < 10:
            85 * weight + 2033

    # Males
    if sex is 0:
        if age >= 60:
            return 49 * weight + 2459
        if age >= 30 && age < 60:
            return 48 * weight + 3653
        if age >= 18 && age < 30:
            return 63 * weight + 2896
        if age >= 10 && age < 18:
            return 74 * weight + 2754
        if age >= 3 && age < 10:
            return 95 * weight + 2110


met_eq_functions = [mifflin, harris_benedict, cunningham, schofield]

T = namedtuple('equation_tuple',['Name', 'Label', 'Standard Error', 'Parameters', 
    'Description', 'References', 'Age_Range', 'Weight_Range', 'Height_Range'])

# not sure if this works w/ multiple lines
# equation_T = namedtuple('Name Label Standard_Error Parameters Description', 
    # 'References Age_Range Weight_Range Height_Range')


mifflin_T = T(
    'Name' = "Mifflin"
    'Equation' = mifflin
    'Standard Error' = (0.1)
    'Parameters' = ['weight', 'age', 'height', 'sex']
    'Description' = 
    'References'= None
    'Age_Range' = (18,80)
    'Weight_Range' = None
    'Height_Range' = (122,272)
    )

harris_benedict_T = T(
    'Name' = "Harris Benedict"
    'Equation' = harris_benedict
    'Standard Error' = (0.1)
    'Parameters' = ['weight', 'age', 'height', 'sex']
    'Description' = 'Standard Error'
    'References'= None
    'Age_Range' = (18,80)
    'Weight_Range' = None
    'Height_Range' = (122,272)
    )

cunningham_T = T(
    'Name' = "Cunningham"
    'Equation' = cunningham
    'Standard Error' = (0.1)
    'Parameters' = ['weight', 'bodyfat']
    'Description' = 'For bodybuilders with low percent bodyfat.'
    'References'= None
    'Age_Range' = (18,80)
    'Weight_Range' = None
    'Height_Range' = (122,272)
    )

schofield_T = T(
    'Name' = "Schofield"
    'Equation' = schofield
    'Standard Error' = (0.1)
    'Parameters' = ['weight', 'age']
    'Description' = 'WHO'
    'References'= None
    'Age_Range' = (3,80)
    'Weight_Range' = None
    'Height_Range' = (122,272)
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
    options = [p for p in equation_tuple.Parameters if p is not 'sex']
    picker_x_axis = Select(title='X-Axis', value=0, 
        options=options)
    picker_x_axis.on_change('value', update)
    return picker_x_axis

def update_widgets(units, equation_tuple, parameters):
    """Change units displayed based on user selected units (imperial or metric),
    and equation ranges of validity for age, weight, height.
    """
    if 'age' in parameters:
    # if equation_tuple.Age_Range and 'age' in parameters:
        min_age = min(equation_tuple.Age_Range)
        max_age = max(equation_tuple.Age_Range)

        slider_age = Slider(start=min_age, end=max_age, value=min_age, step=1, title="Age")
        slider_age.on_change('value', update)
        widgets.append(slider_age)
    
    if 'height' in parameters:
    # if equation_tuple.Height_Range and 'height' in parameters:
        min_height = min(equation_tuple.Height_Range)
        max_height = max(equation_tuple.Height_Range)
        height_title = "Height (cm)"

        if units is 'Imperial':
            min_height = cm_to_inches(min_height)
            max_height = cm_to_inches(max_height)
            height_title = "Height (in)"

        slider_height = Slider(start=min_height, end=max_height, value=min_height, step=1, title="Height")
        slider_height.on_change('value', update)

        widgets.append(slider_height)

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
        button_sex = RadioButtonGroup(labels=["Male", "Female"], active=1)
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

    # widgets = [], append units + equation up here? global?
    # make values 'sticky' between widget updates
    # will need to separate out weight to make sure only plotting for min normal bmi
    # verify % bodyfat ranges, other ranges

    # Which metabolic equation is selected
    equation_tuple = met_eq_tuples[button_equation.active]

    # Set x-axis options based on metabolic equation parameters
    x_axis_picker = select_x_axis(equation_tuple)
    widgets.append(x_axis_picker)

    # Determine units
    units = units_labels[button_units.value]

    # Create widgets for remaining equation parameters
    # based on equation selected:
    # set widget boxes visible for remaining parameters
    # set units, ranges on widgets
    # set info, ref, desc
    # set ranges for parameters
    additonal_parameters = 
        [p for p in equation.Parameters 
        if equation.Parameters.index(p) is not x_axis_picker.value]

    update_widgets(units, equation_tuple, additional_parameters)

    controls = widgetbox(widgets, width=200)
    # associate equation name with correct equation tuple
    


    # get values for arguments
    # apply partials
    # put in x range
    # get out y range result




    # set x axis widget to None/Gray/remove from widgetbox

    # partially apply to metabolism equation
    # pass as dictionary defined above?
    met_eq_partial = partial(equation, sex=sex, height=height, age=age)

    # use x axis range to get y axis values
    # update line

    # validate against normal BMI at minimum

    xs = sorted(set(WEIGHTS))
    ys = sorted(set([mifflin_partial(x) for x in WEIGHTS]))
    
    hover = HoverTool(tooltips = [
        ("x, y", "xs, ys")
    ])

    p = figure(plot_height=600, plot_width=600, tools=[hover])
    p.line(xs, ys, line_width=2)

    return p

def update(attr, old, new):
    layout.children[1] = create_figure()

# Equation Widget
# Other widgets will be set based on parameters, validated ranges for equation chosen.

met_eq_labels = ["Mifflin St Jeor", "Harris Benedict", "Cunningham", "Schofield"]
# met_eq_functions = [mifflin, harris_benedict, cunningham, schofield]
met_eq_tuples = [mifflin_T, harris_benedict_T, cunningham_T, schofield_T]

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

# Layout / Output

layout = row(controls, create_figure())
curdoc().add_root(layout)


