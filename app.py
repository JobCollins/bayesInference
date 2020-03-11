from random import randint
from time import strftime
from flask import Flask, render_template, flash, request, Response
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# plotting
import json
import plotly
import plotly.graph_objs as go

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
    global specificity, sensitivity, prevalence, threshold
    threshold = None
    bar = None
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
            specificity = float(specificity_v)
            sensitivity = float(sensitivity_v)
            prevalence = float(prevalence_v)
            threshold = float(threshold_v)

            p_user = prevalence
            p_non_user = 1-prevalence
            p_pos_user = sensitivity
            p_neg_user = specificity
            p_pos_non_user = 1-float(specificity_v)
            
            
            num = p_pos_user*p_user
            den = p_pos_user*p_user+p_pos_non_user*p_non_user
            
            
            prob = num/den
            
            
            if prob > float(threshold_v):
                print("The test-taker could be an user")
            else:
                print("The test-taker may not be an user")
            
            bar = create_graph()

        else:
            flash('Error: All Fields are Required')
            

    return render_template('index.html', form=form, value=prob, threshold=threshold, plot=bar)

def posterior(specificity, sensitivity, prevalence, threshold):
    
    p_user = prevalence
    p_non_user = 1-prevalence
    p_pos_user = sensitivity
    p_neg_user = specificity
    p_pos_non_user = 1-specificity
    
    
    num = p_pos_user*p_user
    den = p_pos_user*p_user+p_pos_non_user*p_non_user
    
    
    prob = num/den

    return prob

@app.route("/", methods=['POST'])
def plot_png():
    # logic        
    bar = create_graph()
    print('Here the bar')
    print(bar)
    
    return render_template('index.html', plot=bar)

def create_graph():

    probs=[]
    prevs=[]
    for prev in [i*0.001 for i in range(1,51,2)]:
        prevs.append(prev*100)
        prob = posterior(sensitivity=sensitivity,specificity=specificity,prevalence=prev, threshold=threshold)
        probs.append(prob)
    
    data = [
        go.Scatter(
            x=prevs,
            y=probs
        )
    ]

    graph = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graph

if __name__ == "__main__":
    app.run(port=3000, debug=True)