from bokeh.layouts import widgetbox, row, column
from bokeh.plotting import figure, curdoc
from bokeh.models import Slider, Select, RadioButtonGroup
# from bokeh.models.widgets import Slider, Select, RadioButtonGroup
from bokeh.io import output_file, show

options = ['Height', 'Weight', 'Age']

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

    #starting values
    height_p = 200 # cm
    age_p = 40 
    sex_p = 0

    kw = {}
    kw['title'] = 'Estimated RMR vs Weight' # for m/f + age
    kw['x_axis_label'] = 'Weight'
    kw['y_axis_label'] = 'Calories'

    # validate against normal BMI at minimum
    kw['x_range'] = sorted(set(WEIGHTS))
    kw['y_range'] = sorted(set([mifflin(weight, height_p, age_p, sex_p) for weight in WEIGHTS]))
    
    p = figure(plot_height=600, plot_width=800, tools='pan, box_zoom, reset')
    p.line(WEIGHTS, kw['y_range'], line_width=2)

    # p_html = show(p, notebook_handle=True)

    return p

def update(attr, old, new):
    layout.children[1] = create_figure()

x = Select(title='X-Axis', value='mpg', options=options)


# UI Widgets
x = Select(title='X-Axis', value='Height', options=[])
x.on_change('value', update)

controls = widgetbox([x], width=200)
layout = row(controls, create_figure())
curdoc().add_root(layout)

# slider_height = Slider(start=MIN_HEIGHT, end=MAX_HEIGHT, value=1, step=1, title="Height")
# slider_age = Slider(start=MIN_AGE, end=MAX_AGE, value=1, step=1, title="Age")
# button_sex = RadioButtonGroup(labels=["Male", "Female"], active=0)
# equation = Select(title="Equation:", value="Mifflin StJeor", options=["Mifflin St Jeor", "Harris Benedict"])
# static height
# static age

# weight along x axis




if __name__ == '__main__':
    create_figure()

