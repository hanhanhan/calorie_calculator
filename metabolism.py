from functools import partial
from collections import namedtuple

from bokeh.layouts import widgetbox, row, column
from bokeh.plotting import figure, curdoc, output_file
from bokeh.models import Slider, Select, RadioButtonGroup, HoverTool
from bokeh.io import output_file, show


x_options = ['Height', 'Weight', 'Age']
# 1 choose x axis parameter
# 2 choose values for other two parameters

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

equation_T = namedtuple('Name', 'Label', 'Standard Error', 'Parameters', 'Description', 'References')

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

met_eq_labels = ["Mifflin St Jeor", "Harris Benedict", "Cunningham"]
met_eq_functions = [mifflin, harris_benedict, cunningham]
met_eq_D = dict(zip(met_eq_labels, met_eq_functions))

# also include error, age range, weight range?, height range? in tuple?

# -----------------------------------------------------------------------------

def metric_to_imperial(kg, cm):
    Pass

def imperial_to_metric(ft, inch, lb):
    Pass

#starting values
height = 200 # cm
age = 40 
sex = namedtuple()
equation = mifflin

def create_figure():
    
    # get x axis variable
    xs = parameters[x.value]
    x_axis_label = x.value

    # get values for other two variables
    for option in x_options:
        # one of these won't work
        # if option is not x.value:
        age = slider_age.value
        height = slider_height.value
        sex = button_sex.active != 1
        equation = button_equation.active

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

# UI Widgets
x = Select(title='X-Axis', value='Height', options=x_options)
x.on_change('value', update)

slider_age = Slider(start=MIN_AGE, end=MAX_AGE, value=40, step=1, title="Age")
slider_age.on_change('value', update)

slider_height = Slider(start=MIN_HEIGHT, end=MAX_HEIGHT, value=170, step=1, title="Height")
slider_height.on_change('value', update)

button_sex = RadioButtonGroup(labels=["Male", "Female"], active=1)
button_sex.on_change('active', update)

button_equation = RadioButtonGroup(labels=met_eq_labels, active=0)
button_equation.on_change('active', update)

controls = widgetbox([x, slider_age, slider_height, button_sex, button_equation], width=200)



# Layout / Output

layout = row(controls, create_figure())
curdoc().add_root(layout)





# button_sex = RadioButtonGroup(labels=["Male", "Female"], active=0)
# equation = Select(title="Equation:", value="Mifflin StJeor", options=["Mifflin St Jeor", "Harris Benedict"])
# static height
# static age

# weight along x axis




# if __name__ == '__main__':
#     create_figure()

