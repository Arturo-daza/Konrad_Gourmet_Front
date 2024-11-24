from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField(
        "Correo Electrónico",
        validators=[DataRequired(message="Este campo es obligatorio"), Email(message="Ingrese un correo válido")],
    )
    password = PasswordField(
        "Contraseña",
        validators=[DataRequired(message="Este campo es obligatorio")],
    )
    submit = SubmitField("Iniciar Sesión")
