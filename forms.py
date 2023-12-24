"""Forms for Flask Cafe."""
from flask_wtf import FlaskForm

from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, URL, Optional

from models import City


class CSRFProtection(FlaskForm):
    """CSRFProtection form, intentionally has no fields."""


class CafeEditForm(FlaskForm):
    """Form for adding/editing cafes."""

    name = StringField(
        'Name',
        validators=[InputRequired(), Length(max=50)],
    )

    description = TextAreaField(
        '(Optional) Cafe Description',
        validators=[Optional()],
    )

    url = StringField(
        '(Optional)Cafe URL',
        validators=[Optional(), URL()],
    )

    address = StringField(
        'Address',
        validators=[InputRequired(), Length(max=100)],
    )

    city_code = SelectField(
        'City',
        choices=[(city.id, city.name) for city in City.query.all()],
    )

    image_url = StringField(
        '(Optional) Image URL',
        validators=[Optional(), URL()]
    )

