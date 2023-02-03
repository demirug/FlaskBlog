from flask import Blueprint
from apps.authorization.models import User
from extensions import login_manager

from .models import *

authorization = Blueprint('authorization', __name__, template_folder='templates', static_folder='static')

login_manager.login_view = "authorization.login"

from .routes import *


@login_manager.unauthorized_handler
def handle_unauthorized():
    return redirect(url_for(login_manager.login_view, next=url_for(request.endpoint, **request.view_args)))


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.filter_by(id=user_id).first()
