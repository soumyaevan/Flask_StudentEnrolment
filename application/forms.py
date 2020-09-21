from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Regexp, Length, Email, EqualTo, ValidationError
from application.models import User

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=6, max=15)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=6, max=15)])
    confirm_password = PasswordField("Password", validators=[DataRequired(),Length(min=6, max=15), EqualTo('password')])
    first_name = StringField("First Name", validators=[DataRequired(),Length(min=6, max=15), Regexp("^[^@#$%&*)(]\w+$")])
    last_name = StringField("Last Name", validators=[DataRequired(), Regexp("^[^@#$%&*)(]\w+$")])
    submit = SubmitField("Register")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("This email address is already registered")