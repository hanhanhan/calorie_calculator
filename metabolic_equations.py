 # Metabolic Equations for Resting Metabolic Rate
from collections import namedtuple

# Metabolic Equations

def mifflin(weight=None, height=None, age=None, sex=None):
    """Basal metabolic rate in calories
    based on weight in kg, height in cm, and
    sex (male = 1, female = 0)
    """
    if sex is 'Male':
        sex = 1
    else:
        sex = 0

    return 9.99 * weight + 6.25 * height - 4.92 * age + 166 * sex - 161


def harris_benedict(weight=None, height=None, age=None, sex=None):
    """Resting metabolic rate in calories
    based on weight in kg, height in cm, and
    sex.
    """
    if sex is 'Male':
        return 66.5 + 13.75 * weight + 5.003 * height - 6.755 * age
    else: 
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
    if sex is 'Female':
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
    else: 
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

# Tuples with Associated Data

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
    References = None,
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
    References = None,
    Age_Range = (3,80),
    Weight_Range = None,
    Height_Range = (122,272),
    Bodyfat_Range = None
    )

# also include error, age range, weight range?, height range? in tuple?

# met_eq_functions = ['mifflin', 'harris_benedict', 'cunningham', 'schofield']

met_eq_tuples = [mifflin_T, harris_benedict_T, cunningham_T, schofield_T]
met_eq_functions = [eq.Name for eq in met_eq_tuples]
labels = [eq.Name for eq in met_eq_tuples]
eq_tup_D = dict(zip(met_eq_functions, met_eq_tuples))


sex_values = ['Male', 'Female']

# -----------------------------------------------------------------------------

def cm_to_inches(cm):
    return 0.3937 * cm

def kg_to_lb(kg):
    return 2.20462 * kg

def bmi(weight, height):
    return weight / (0.01 * 0.01 * height * height)

def underweight(bmi):
    return bmi < 19