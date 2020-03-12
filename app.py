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
    prob_2 = None
    prob_3 = None
    global specificity, sensitivity, prevalence, threshold
    threshold = None
    bar = None
    sens_line = None
    specs_line = None
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
            sens_line = create_sens_graph()
            specs_line = create_spec_graph()
            
            prob_2 = posterior(sensitivity=sensitivity,specificity=specificity,prevalence=prob, threshold=threshold)
            prob_3 = posterior(sensitivity=sensitivity,specificity=specificity,prevalence=prob_2, threshold=threshold)

        else:
            flash('Error: All Fields are Required')
            

    return render_template('index.html', form=form, value=prob, threshold=threshold, plot=bar, sens=sens_line, specs=specs_line, probTwo=prob_2, probThree=prob_3)

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
            y=probs,
            mode='lines+markers'
        )
    ]

    layout = go.Layout(
        title=go.layout.Title(
            text='Probability of True Positive with Prevalence Rate',
            xref='paper',
            x=0
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text='Prevalence(%)',
                font=dict(
                    family='Roboto',
                    size=18,
                    color='#7f7f7f'
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text='Probability of a True Positive',
                font=dict(
                    family='Roboto',
                    size=18,
                    color='#7f7f7f'
                )
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graph

def create_sens_graph():

    probs=[]
    sens=[]
    for sen in [i*0.001+0.95 for i in range(1,50,2)]:
        sens.append(sen)
        prob = posterior(sensitivity=sen,specificity=specificity,prevalence=prevalence, threshold=threshold)
        probs.append(prob)
    
    data = [
        go.Scatter(
            x=sens,
            y=probs,
            mode='lines+markers'
        )
    ]

    layout = go.Layout(
        title=go.layout.Title(
            text='Probability of True Positive with Test Sensitivity',
            xref='paper',
            x=0
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text='Sensitivity(%)',
                font=dict(
                    family='Roboto',
                    size=18,
                    color='#7f7f7f'
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text='Probability of a True Positive',
                font=dict(
                    family='Roboto',
                    size=18,
                    color='#7f7f7f'
                )
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graph

def create_spec_graph():

    probs=[]
    specs=[]
    for spec in [i*0.001+0.95 for i in range(1,50,2)]:
        specs.append(spec)
        prob = posterior(sensitivity=sensitivity,specificity=spec,prevalence=prevalence, threshold=threshold)
        probs.append(prob)
    
    data = [
        go.Scatter(
            x=specs,
            y=probs,
            mode='lines+markers'
        )
    ]

    layout = go.Layout(
        title=go.layout.Title(
            text='Probability of True Positive with Test Specificity',
            xref='paper',
            x=0
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text='Specificity(%)',
                font=dict(
                    family='Roboto',
                    size=18,
                    color='#7f7f7f'
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text='Probability of a True Positive',
                font=dict(
                    family='Roboto',
                    size=18,
                    color='#7f7f7f'
                )
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    
    graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graph

if __name__ == "__main__":
    app.run(port=3000, debug=True)