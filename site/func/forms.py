from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):
    name = StringField("Videos", render_kw={
                       "placeholder": "Paste link",
                       "class": "form-input",
                       "id": "formGroupExampleInput"})
