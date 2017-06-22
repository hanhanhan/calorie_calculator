from bokeh.layouts import widgetbox, row, column
from bokeh.plotting import figure, curdoc, output_file
from bokeh.models import Slider, Select, RadioButtonGroup
from bokeh.io import output_file, show
from functools import partial
options = ['Height', 'Weight', 'Age']
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

#starting values
height = 200 # cm
age = 40 
sex = 0

def metric_to_imperial(kg, cm):
    Pass

def imperial_to_metric(ft, inch, lb):
    Pass

def mifflin(weight, height, age, sex):
    """Basal metabolic rate in calories
    based on weight in kg, height in cm, and
    sex (male = 1, female = 0)
    """
    return 9.99 * weight + 6.25 * height - 4.92 * age + 166 * sex - 161

def create_figure():
    x_axis_label = x.value
    # get x axis variable
    # get values for other two variables
    # set x axis widget to None/Gray/remove from widgetbox

    # partially apply to metabolism equation
    # use x axis range to get y axis values
    # update line


    age = slider_age.value

    # validate against normal BMI at minimum
    kw['x_range'] = sorted(set())
    kw['y_range'] = sorted(set([mifflin(weight, height, age, sex) for x in kw['x_range']]))
    
    p = figure(plot_height=600, plot_width=800, tools='pan, box_zoom, reset')
    p.line(kw['x_range'], kw['y_range'], line_width=2)

    return p

def update(attr, old, new):
    layout.children[1] = create_figure()

# UI Widgets
x = Select(title='X-Axis', value='Height', options=options)
x.on_change('value', update)

slider_age = Slider(start=MIN_AGE, end=MAX_AGE, value=40, step=1, title="Age")
slider_age.on_change('value', update)

controls = widgetbox([x, slider_age], width=200)

layout = row(controls, create_figure())
show(layout)


# slider_height = Slider(start=MIN_HEIGHT, end=MAX_HEIGHT, value=1, step=1, title="Height")


# button_sex = RadioButtonGroup(labels=["Male", "Female"], active=0)
# equation = Select(title="Equation:", value="Mifflin StJeor", options=["Mifflin St Jeor", "Harris Benedict"])
# static height
# static age

# weight along x axis




# if __name__ == '__main__':
#     create_figure()

