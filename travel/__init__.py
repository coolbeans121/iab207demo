from werkzeug.exceptions import HTTPException
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
#task 2 wk 12
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import datetime
#task 3 wk 12
from flask import render_template, flash



db = SQLAlchemy()
#task 3 wk 12
app = Flask(__name__)
def create_app():
    #we use this utility module to display forms quickly
    Bootstrap5(app)

    #this is a much safer way to store passwords
    Bcrypt(app)

    #a secret key for the session object
    #(it would be better to use an environment variable here)
    app.secret_key = 'somerandomvalue'

    #Configue and initialise DB
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///traveldb.sqlite'
    db.init_app(app)

    #config upload folder
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
    
    #task 2 wk 12
    login_manager = LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #task 2 wk 12
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
          return User.query.get(int(user_id))

    #add Blueprints
    from . import views
    app.register_blueprint(views.mainbp)
    from . import destinations
    app.register_blueprint(destinations.destbp)
    from . import auth
    app.register_blueprint(auth.authbp)

    #task 3 wk 12
    @app.errorhandler(HTTPException) 
    def not_found(e): 
      flash("Error " + e.description)
      return render_template("error.html", error=e), 404
      

    #this creates a dictionary of variables that are available
    #to all html templates
    @app.context_processor
    def get_context():
      year = datetime.datetime.today().year
      return dict(year=year)

    return app

