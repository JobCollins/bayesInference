from flask import Flask, url_for, render_template, redirect, request
from forms import BayeForm
import os
from flask_bootstrap import Bootstrap


app = Flask(__name__, instance_relative_config=False)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap(app)


@app.route('/')
def home():
    form = BayeForm()
    return render_template('bayes.html', form=form)


@app.route('/bayes', methods=['GET', 'POST'])
def bayes():
    form = BayeForm(request.form)
    if form.validate_on_submit():
        specificity = form.specificity.data
        sensitivity = form.sensitivity.data
        prevalence = form.prevalence.data
        threshold = form.p_threshold.data

        print('Here is', specificity, sensitivity, prevalence, threshold)
    else:
        print('Not valid')
        

    return render_template('layout.html', form=form)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
