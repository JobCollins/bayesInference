from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length


class BayeForm(FlaskForm):
    """Bayes Inference Form"""
    specificity = DecimalField('Specificity', [DataRequired()])
    sensitivity = DecimalField('Sensitivity', [DataRequired()])
    prevalence = DecimalField('Prevalence', [DataRequired()])
    p_threshold = DecimalField('Threshold', [DataRequired()])
    bayes_infer = SubmitField('Bayes Inference')