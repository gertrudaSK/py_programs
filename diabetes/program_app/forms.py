from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField
from wtforms.validators import NumberRange


class Questions:
    polyuria = 'Do you urinate more than usual and passes excessive or abnormally large amounts of urine each time you urinate?'
    polydipsia = 'Do you often feel very thirsty?'
    weight = 'Do you recently sudden lost your weight?'
    weakness = 'Do you often feel weakness?'
    polyphagia = 'Do you feel excessive appetite?'
    genital = 'Do you feeling itchy and sore outside your genital area?'
    vision = 'Is your visual acuity decreased?'
    itching = 'Do you often feel itching and want to scratch your skin?'
    irritability = 'Are you often feeling irritable?'
    healing = 'Did you had a wound that was healing not properly?'
    paresis = 'Are your movements weaker than usual?'
    muscle = 'Do your muscles feel tight and you find it more difficult to move than you usually do, especially after rest?'
    alopecia = 'Do you have hair loss?'
    obesity = 'Do you have excess fat especially around the waist?'


class DiabetesForm(FlaskForm):
    age = IntegerField('Age', [NumberRange(min=1, max=120)])
    gender = SelectField('Gender', choices=[(1, 'Male'), (0, 'Female')],
                         coerce=int)
    polyuria = SelectField(Questions.polyuria, choices=[(1, 'Yes'), (0, 'No')],
                           coerce=int)
    polydipsia = SelectField(Questions.polydipsia,
                             choices=[(1, 'Yes'), (0, 'No')], coerce=int)
    weight = SelectField(Questions.weight, choices=[(1, 'Yes'), (0, 'No')],
                         coerce=int)
    weakness = SelectField(Questions.weakness, choices=[(1, 'Yes'), (0, 'No')],
                           coerce=int)
    polyphagia = SelectField(Questions.polyphagia,
                             choices=[(1, 'Yes'), (0, 'No')], coerce=int)
    genital = SelectField(Questions.genital, choices=[(1, 'Yes'), (0, 'No')],
                          coerce=int)
    vision = SelectField(Questions.vision, choices=[(1, 'Yes'), (0, 'No')],
                         coerce=int)
    itching = SelectField(Questions.itching, choices=[(1, 'Yes'), (0, 'No')],
                          coerce=int)
    irritability = SelectField(Questions.irritability,
                               choices=[(1, 'Yes'), (0, 'No')], coerce=int)
    healing = SelectField(Questions.healing, choices=[(1, 'Yes'), (0, 'No')],
                          coerce=int)
    paresis = SelectField(Questions.paresis, choices=[(1, 'Yes'), (0, 'No')],
                          coerce=int)
    muscle = SelectField(Questions.muscle, choices=[(1, 'Yes'), (0, 'No')],
                         coerce=int)
    alopecia = SelectField(Questions.alopecia, choices=[(1, 'Yes'), (0, 'No')],
                           coerce=int)
    obesity = SelectField(Questions.obesity, choices=[(1, 'Yes'), (0, 'No')],
                          coerce=int)
    submit = SubmitField('Submit', render_kw={'class': 'btn btn-success'})
