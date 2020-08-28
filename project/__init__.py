# IMPORTS
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_login import current_user, login_required
from flask_mail import Mail
from config import *


# CONFIG
app = Flask(__name__, instance_relative_config=True)
'''
Add second line: export APP_SETTINGS="config.DevelopmentConfig"
app.config.from_object(os.environ['APP_SETTINGS'])
'''

print(app.config) ## See What is the state of app.config
app.config.from_object("config.DevelopmentConfig")
print("After creating it from object")
print(app.config) ## Look at it now

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

from project.models import User, Items


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


# BLUEPRINTS
from project.users.views import users_blueprint
from project.items.views import items_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(items_blueprint)


# ROUTES
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """Render homepage"""

    all_user_items = Items.query.filter_by(user_id=current_user.id)
    return render_template('home.html', items=all_user_items)


# ERROR PAGES
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(410)
def page_gone(e):
    return render_template('410.html'), 410

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    app.run(debug=True)

