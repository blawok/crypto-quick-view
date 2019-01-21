from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired

# class InfoForm(FlaskForm):
#     """
#     class that inherits from FlaskForm
#     used for getting values from user
#     """
#     currency = SelectField(u'Currency:',
#                            choices = [('lisk', 'LSK'),
#                                       ('bitcoin', 'BTC'),
#                                       ('ripple', 'XRP'),
#                                       ('ethereum', 'ETH'),
#                                       ('litecoin', 'LTC')
#                                       ],
#                            validators=[DataRequired()])
#     fromDate = StringField("From when?", validators=[DataRequired()])
#     tillDate = StringField("Until when?", validators=[DataRequired()])
#     submit = SubmitField('Submit')


# class UpdateForm(FlaskForm):
#     """
#     class that inherits from FlaskForm
#     used for getting values from user to update cryptoStats
#     """
#     currencyUpdate = SelectField(u'Currency:',
#                            choices = [('lisk', 'LSK'),
#                                       ('bitcoin', 'BTC'),
#                                       ('ripple', 'XRP'),
#                                       ('ethereum', 'ETH'),
#                                       ('litecoin', 'LTC')
#                                       ],
#                            validators=[DataRequired()])
#     dateUpdate = StringField("Choose date to update", validators=[DataRequired()])
#     highUpdate = IntegerField("Change high value", validators=[DataRequired()])
#     lowUpdate = IntegerField("Change low value", validators=[DataRequired()])

#     submit = SubmitField('Submit')


class InfoForm(FlaskForm):
    """
    class that inherits from FlaskForm
    used for getting values from user
    """
    currency = SelectField(u'Currency:',
                           choices = [('LSK','lisk'),
                                      ('BTC','bitcoin'),
                                      ('XRP','ripple'),
                                      ('ETH','ethereum'),
                                      ('LTC','litecoin')
                                      ],
                           validators=[DataRequired()])
    fromDate = StringField("From when?", validators=[DataRequired()])
    tillDate = StringField("Until when?", validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpdateForm(FlaskForm):
    """
    class that inherits from FlaskForm
    used for getting values from user to update cryptoStats
    """
    currencyUpdate = SelectField(u'Currency:',
                           choices = [('LSK','lisk'),
                                      ('BTC','bitcoin'),
                                      ('XRP','ripple'),
                                      ('ETH','ethereum'),
                                      ('LTC','litecoin')
                                      ],
                           validators=[DataRequired()])
    dateUpdate = StringField("Choose date to update", validators=[DataRequired()])
    highUpdate = IntegerField("Change high value", validators=[DataRequired()])
    lowUpdate = IntegerField("Change low value", validators=[DataRequired()])

    submit = SubmitField('Submit')
