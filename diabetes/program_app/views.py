from flask import render_template, flash, request
from program_app import app
from .forms import DiabetesForm
import joblib
import os

def load_model():
    print("kelias", os.getcwd())
    loaded_rf = joblib.load(
        "program_app/training_model/random_forest.joblib")
    return loaded_rf


@app.route('/', methods=['GET', 'POST'])
def home():
    form = DiabetesForm()
    if request.method == 'POST' and form.validate():
        age = form.age.data
        gender = form.gender.data
        polyuria = form.polyuria.data
        polydipsia = form.polydipsia.data
        weight = form.weight.data
        weakness = form.weakness.data
        polyphagia = form.polyphagia.data
        genital = form.genital.data
        vision = form.vision.data
        itching = form.itching.data
        irritability = form.irritability.data
        healing = form.healing.data
        paresis = form.paresis.data
        muscle = form.muscle.data
        alopecia = form.alopecia.data
        obesity = form.obesity.data
        model = load_model()
        prediction = model.predict([[age, gender, polyuria, polydipsia, weight,
                                     weakness, polyphagia, genital, vision,
                                     itching, irritability, healing, paresis,
                                     muscle, alopecia, obesity]])
        flash(f'You got {prediction[0]} test!', 'info')
        return render_template('diabetes_form.html', form=form)
    return render_template('diabetes_form.html', form=form)
