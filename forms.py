from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired

class InfoForm(FlaskForm):
    """
    class that inherits from FlaskForm
    used for getting values from user
    """
    currency = SelectField(u'Currency:',
                           choices = [('lisk', 'LSK'),
                                      ('bitcoin', 'BTC'),
                                      ('ripple', 'XRP'),
                                      ('ethereum', 'ETH'),
                                      ('litecoin', 'LTC')
                                      ],
                           validators=[DataRequired()])
    fromDate = StringField("From when?", validators=[DataRequired()])
    tillDate = StringField("Until when?", validators=[DataRequired()])
    submit = SubmitField('Submit')
