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
def bayes():
    form = BayesForm(request.form)
    prob = None
    #print(form.errors)
    if request.method == 'POST':

        if form.validate():
            specificity_v=request.form['specificity']
            sensitivity_v=request.form['sensitivity']
            prevalence_v=request.form['prevalence']
            threshold_v=request.form['threshold']
            
            flash('Your values are: Specificity {} Sensitivity {} Prevalence {} Threshold {}'.format(specificity_v, sensitivity_v, prevalence_v, threshold_v))

            """
            Computes the posterior using Bayes' rule
            """
            p_user = float(prevalence_v)
            p_non_user = 1-float(prevalence_v)
            p_pos_user = float(sensitivity_v)
            p_neg_user = float(specificity_v)
            p_pos_non_user = 1-float(specificity_v)
            
            num = p_pos_user*p_user
            den = p_pos_user*p_user+p_pos_non_user*p_non_user
            
            
            prob = num/den
            
            
            if prob > float(threshold_v):
                print("The test-taker could be an user")
            else:
                print("The test-taker may not be an user")

        else:
            flash('Error: All Fields are Required')

    return render_template('index.html', form=form, value=prob)

if __name__ == "__main__":
    app.run(port=3000, debug=True)