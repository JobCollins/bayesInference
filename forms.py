from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length


class BayeForm(FlaskForm):
    """Bayes Inference Form"""
    specificity = DecimalField('Specificity', validators=[DataRequired()])
    sensitivity = DecimalField('Sensitivity', validators=[DataRequired()])
    prevalence = DecimalField('Prevalence', validators=[DataRequired()])
    p_threshold = DecimalField('Threshold', validators=[DataRequired()])
    bayes_infer = SubmitField('Bayes Inference')