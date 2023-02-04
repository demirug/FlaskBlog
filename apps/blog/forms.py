import re

from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
import wtforms
import wtforms.validators as validators

from apps.blog import Blog
from mixins.modelform import ModelFormMixin
from services.unique_slugify import unique_slugify


class BlogForm(ModelFormMixin, FlaskForm):
    model = Blog

    slug = wtforms.StringField("Slug", validators=[
        validators.Regexp('^[a-z0-9-]*$',
                          message="In slug allowed only lowercase letters, numbers, '-' char")
    ])
    title = wtforms.StringField("Title", validators=[validators.InputRequired()])
    content = CKEditorField('Content', validators=[validators.InputRequired()])

    def validate_title(self, field):
        if len(re.sub('[^aA-zZ\d]', '', self.title.data)) < 5:
            raise validators.ValidationError("Too short title")
        return field

    def validate_slug(self, field):
        if field.data == "":
            field.data = unique_slugify(self.get_instance(), self.title.data)
        elif Blog.query.filter(Blog.slug == field.data, Blog.id != self.get_instance().id).first():
            raise validators.ValidationError("Given slug already in use")

        return field


class CommentForm(FlaskForm):
    text = CKEditorField('Comment', validators=[validators.InputRequired(), validators.Length(min=15)])
