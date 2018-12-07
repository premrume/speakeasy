#################
#### imports ####
#################

from flask import Flask, render_template, send_from_directory
from flask_uploads import UploadSet, IMAGES, TEXT, DOCUMENTS, configure_uploads
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

################
#### config ####
################

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

db = MongoEngine()
db.init_app(app)

# Configure the image uploading via Flask-Uploads
ende = UploadSet('ende', IMAGES + TEXT + DOCUMENTS)
kor = UploadSet('kor', IMAGES + TEXT + DOCUMENTS)
configure_uploads(app, ende)
configure_uploads(app, kor)

####################
#### blueprints ####
####################

from project.home.views import home_blueprint
from project.nifi.views import nifi_blueprint

# register the blueprints
app.register_blueprint(home_blueprint)
app.register_blueprint(nifi_blueprint)


############################
#### custom error pages ####
############################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

@app.errorhandler(410)
def page_not_found(e):
    return render_template('410.html'), 410
