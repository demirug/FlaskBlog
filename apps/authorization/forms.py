from flask_wtf import FlaskForm
import wtforms
import wtforms.validators as validators
from werkzeug.security import check_password_hash

from apps.authorization import User


class LoginForm(FlaskForm):
    username = wtforms.StringField("Username",
                                   validators=[validators.Length(5, 32), validators.InputRequired()])
    password = wtforms.PasswordField("Password", validators=[validators.Length(9, 24), validators.InputRequired()])
    remember_me = wtforms.BooleanField("Remember me", default=False)

    def validate_password(self, field):
        user = User.query.filter_by(username=self.username.data).first()

        if user is None or not check_password_hash(user.psw_hash, field.data):
            raise validators.ValidationError("Incorrect login or password")

        if not user.is_active:
            raise validators.ValidationError("Please verify your email address")

        self.user = user

        return field

    def get_user(self):
        return self.user


class RegisterForm(FlaskForm):
    username = wtforms.StringField("Username", validators=[
        validators.Length(5, 32),
        validators.InputRequired(),
        validators.Regexp('^(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?![_.])$')
    ])

    email = wtforms.EmailField("Email", validators=[validators.InputRequired()])

    password = wtforms.PasswordField("Password", validators=[
        validators.Length(9, 24),
        validators.InputRequired(),
        validators.Regexp('^(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?![_.])$')
    ])
    password_cnf = wtforms.PasswordField("Confirm password",
                                         validators=[validators.Length(9, 24), validators.EqualTo('password')])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() is not None:
            raise validators.ValidationError("Given username already in use")
        return field


class ChangePasswordForm(FlaskForm):

    def __init__(self, user: User, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    password_old = wtforms.PasswordField("Old Password", validators=[
        validators.Length(9, 24),
        validators.InputRequired(),
        validators.Regexp('^(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?![_.])$')
    ])
    password = wtforms.PasswordField("New Password", validators=[
        validators.Length(9, 24),
        validators.InputRequired(),
        validators.Regexp('^(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$')
    ])
    password_cnf = wtforms.PasswordField("Confirm password",
                                         validators=[validators.Length(9, 24), validators.EqualTo('password')])

    def validate_password_old(self, field):
        if not check_password_hash(self.user.psw_hash, field.data):
            raise validators.ValidationError("Incorrect old password")
        return field

    def validate_password(self, field):
        if self.password_old.data == field.data:
            raise validators.ValidationError("New/Old passwords are same")
        return field