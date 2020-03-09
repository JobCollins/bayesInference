from flask import Flask, url_for, render_template, redirect
from forms import BayeForm
import os


app = Flask(__name__, instance_relative_config=False)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=('GET', 'POST'))
def bayes():
    form = BayeForm()
    if form.validate_on_submit():
        return redirect(url_for('success'))

    return render_template('bayes.html', form=form)

if __name__ == '__main__':
    app.run(port=3000, debug=True)
