from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class InfoForm(FlaskForm):
    currency = StringField('currency', validators=[DataRequired()])
    fromDate = StringField("From when?", validators=[DataRequired()])
    tillDate = StringField("Until when?", validators=[DataRequired()])
    submit = SubmitField('Submit')
