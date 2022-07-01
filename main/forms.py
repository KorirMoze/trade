from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, length, Email, equal_to, ValidationError

from main.models import User


class RegistrationForm(FlaskForm):

    userName = StringField("UserName", validators=[DataRequired(), length(min=2, max=20)])
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password" , validators=[DataRequired()])
    phoneNumber=StringField("Enter Your Phone Number", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),equal_to("password")])
    submit = SubmitField("Sign Up")

    def validate_userName(self,userName):
        user = User.query.filter_by(userName=userName.data).first()
        if user:
            raise ValidationError("Username Is already in use by Another User")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email Is already in use by Another User")

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(),Email()])
    password = PasswordField("Password" , validators=[DataRequired()])
    remember = BooleanField("Stay Logged In")
    submit = SubmitField("Sign in")




