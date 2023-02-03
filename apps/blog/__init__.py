from flask import Blueprint

from .models import *

blog = Blueprint('blog', __name__, template_folder='templates', static_folder='static')

from .routes import *
