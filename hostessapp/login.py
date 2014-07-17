from flask.ext.login import LoginManager, login_user , logout_user , current_user , login_required
from hostessapp import app
from models import Sister

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return Sister.query.get(int(id))