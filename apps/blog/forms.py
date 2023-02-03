from flask_wtf import FlaskForm
import wtforms
import wtforms.validators as validators

from apps.blog import Blog
from services.unique_slugify import unique_slugify


class BlogForm(FlaskForm):
    slug = wtforms.StringField("Slug", validators=[
        validators.Regexp('^[a-z0-9-]*$',
                          message="Slug allowed only lowercase letters, numbers, -")
    ])
    title = wtforms.StringField("Title", validators=[validators.InputRequired()])
    content = wtforms.TextAreaField("Content", validators=[validators.InputRequired()])

    def validate_slug(self, field):

        if field.data == "":
            field.data = unique_slugify(Blog(), self.title.data)
        elif Blog.query.filter_by(slug=field.data).first():
            raise validators.ValidationError("Given slug already in use")

        return field
