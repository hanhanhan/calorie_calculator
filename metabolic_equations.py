 # Metabolic Equations for Resting Metabolic Rate
from collections import namedtuple
from inspect import getargspec

# Metabolic Equations, Tuples with Meta Info, Constants

def mifflin(weight=None, height=None, age=None, sex=None, units_system=None):
    """Basal metabolic rate in calories
    based on weight in kg, height in cm, and
    sex (male = 1, female = 0)
    """
    if units_system is 'Imperial':
        height = height * 2.54 # inches to cm
        weight = weight * 0.453592 # lbs to kg

    if sex is 'Male':
        sex = 1
    else:
        sex = 0

    return 9.99 * weight + 6.25 * height - 4.92 * age + 166 * sex - 161


def harris_benedict(weight=None, height=None, age=None, sex=None, units_system=None):
    """Resting metabolic rate in calories
    based on weight in kg, height in cm, and
    sex.
    """
    if units_system is 'Imperial':
        height = height * 2.54 # inches to cm
        weight = weight * 0.453592 # lbs to kg

    if sex is 'Male':
        return 66.5 + 13.75 * weight + 5.003 * height - 6.755 * age
    else: 
        return 655.1 + 9.563 * weight + 1.850 * height - 4.676 * age


def cunningham(weight=None, bodyfat=None, units_system=None):
    """Resting metabolic rate in calories
    based on weight in kg and percent body fat
    """

    if units_system is 'Imperial':
        weight = weight * 0.453592 # lbs to kg

    return (weight - weight * bodyfat * 0.01) * 21.6 + 500


def schofield(age=None, weight=None, sex=None, units_system=None):
    """Resting metabolic rate based on on weight in kg, age, and
    sex (male = 1, female = 0)
    """

    if units_system is 'Imperial':
        weight = weight * 0.453592 # lbs to kg

    # Females
    if sex is 'Female':
        if age >= 60:
            return 9.082 * weight + 658.5
        if age >= 30 and age < 60:
            return 8.126 * weight + 845.6
        if age >= 18 and age < 30:
            return 14.818 * weight + 486.6
        if age >= 10 and age < 18:
            return 13.384 * weight + 692.6
        if age >= 3 and age < 10:
            return 20.315 * weight + 485.9


    # Males
    else: 
        if age >= 60:
            return 11.711 * weight + 587.7
        if age >= 30 and age < 60:
            return 11.472 * weight + 873.1
        if age >= 18 and age < 30:
            return 15.057 * weight + 692.2
        if age >= 10 and age < 18:
            return 17.686 * weight + 658.2
        if age >= 3 and age < 10:
            return 22.706 * weight + 504.3

# Tuples with Associated Data 

# better to put as separate variable? or use _fields protected method?
tuple_fields = ['name', 'equation', 'standard_error', 
    'parameters', 'description', 'references', 'age_range', 'weight_range', 
    'height_range', 'bodyfat_range']

T = namedtuple('equation_tuple', tuple_fields)

# not sure if this works w/ multiple lines
# T = namedtuple('equation_tuple','Name Equation Standard_Error Parameters Description', 
#     'References Age_Range Weight_Range Height_Range')

mifflin_T = T(
    name = "Mifflin St Jeor",
    equation = mifflin,
    standard_error = (0.1),
    # parameters = getargspec(mifflin).args, # better way ?
    parameters = ['weight', 'age', 'height', 'sex', 'units_system'],
    description = None,
    references = None,
    age_range = (18,80),
    weight_range = (30, 200),
    height_range = (122,272),
    bodyfat_range = None
    )

harris_benedict_T = T(
    name = "Harris Benedict",
    equation = harris_benedict,
    standard_error = (0.1),
    parameters = ['weight', 'age', 'height', 'sex', 'units_system'],
    description = None,
    references = None,
    age_range = (18,80),
    weight_range = (30,200),
    height_range = (122,272),
    bodyfat_range = None
    ) 

cunningham_T = T(
    name = "Cunningham",
    equation = cunningham,
    standard_error = (0.1),
    parameters = ['weight', 'bodyfat', 'units_system'],
    description = 'For bodybuilders with low percent bodyfat.',
    references= None,
    age_range = None,
    weight_range = (30,200),
    height_range = None,
    bodyfat_range = (4,25)
    )

schofield_T = T(
    name = "Schofield",
    equation = schofield,
    standard_error = (0.1),
    parameters = ['weight', 'age', 'units_system'],
    description = 'WHO',
    references = None,
    age_range = (3,80),
    weight_range = (30, 330),
    height_range = None,
    bodyfat_range = None
    )

# also include error, age range, weight range?, height range? in tuple?

# met_eq_functions = ['mifflin', 'harris_benedict', 'cunningham', 'schofield']

met_eq_tuples = [mifflin_T, harris_benedict_T, cunningham_T, schofield_T]
met_eq_functions = [eq.name for eq in met_eq_tuples]
labels = [eq.name for eq in met_eq_tuples]
eq_tup_D = dict(zip(met_eq_functions, met_eq_tuples))


sex_values = ['Male', 'Female']

# -----------------------------------------------------------------------------

def cm_to_inches(cm):
    return round(0.3937 * cm)

def kg_to_lb(kg):
    return round(2.20462 * kg)

def inches_to_cm(inches):
    return round(2.54 * inches)

def lb_to_kg(lb):
    return round(0.453592 * lb)

conversion_D = {'kg': lb_to_kg, 'lbs': kg_to_lb, 
    'cm': inches_to_cm, 'inches': cm_to_inches}

def bmi(weight, height):
    return round(weight / (0.01 * 0.01 * height * height))

def underweight(bmi):
    return bmi < 19