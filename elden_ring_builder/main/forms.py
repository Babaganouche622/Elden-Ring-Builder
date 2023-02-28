from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

# form for create_build
class CreateBuildForm(FlaskForm):
    name = StringField('Build Name', validators=[DataRequired()])
    description = StringField('Build Description', validators=[DataRequired()])
    submit = SubmitField('Create Build')

class CreateWeaponForm(FlaskForm):
    name = StringField('Weapon Name', validators=[DataRequired()])
    image = StringField('Weapon Image', validators=[DataRequired()])
    submit = SubmitField('Create Weapon')
    