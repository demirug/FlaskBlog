from flask_wtf import FlaskForm
import wtforms
import wtforms.validators as validators


class BlogForm(FlaskForm):
    username = wtforms.StringField("Username",
                                   validators=[validators.Length(5, 32), validators.InputRequired()])
    password = wtforms.PasswordField("Password", validators=[validators.Length(9, 24), validators.InputRequired()])
    remember_me = wtforms.BooleanField("Remember me", default=False)
