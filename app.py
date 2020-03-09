from flask import Flask, url_for, render_template, redirect
from forms import BayeForm


app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')


@app.route('/', methods=('GET', 'POST'))
def bayes_infer():
    form = BayeForm()
    if form.validate_on_submit():
        return redirect(url_for('success'))

    return render_template('index.html', form=form)