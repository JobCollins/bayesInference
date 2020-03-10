from random import randint
from time import strftime
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'SjdnUends821Jsdlkvxh391ksdODnejdDw'

class BayesForm(Form):
    specificity = TextField('Specificity:', validators=[validators.required()])
    sensitivity = TextField('Sensitivity:', validators=[validators.required()])
    prevalence = TextField('Prevalence:', validators=[validators.required()])
    threshold = TextField('Probability Threshold:', validators=[validators.required()])


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = BayesForm(request.form)

    #print(form.errors)
    if request.method == 'POST':

        specificity_v=request.form['specificity']
        sensitivity_v=request.form['sensitivity']
        prevalence_v=request.form['prevalence']
        threshold_v=request.form['threshold']

        if form.validate():
            
            flash('Your values are: Specificity {} Sensitivity {} Prevalence {} Threshold {}'.format(specificity_v, sensitivity_v, prevalence_v, threshold_v))

        else:
            flash('Error: All Fields are Required')

    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(port=3000, debug=True)