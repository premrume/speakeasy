#################
#### imports ####
#################
from flask import Flask, render_template
from flask_uploads import UploadSet, IMAGES, TEXT, configure_uploads
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface

################
#### config ####
################
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

################
#### mongoengine pain ####
################
db = MongoEngine()
db.init_app(app)

################
#### flask-uploads pain ####
################
ende = UploadSet('ende', IMAGES + TEXT)
kor = UploadSet('kor', IMAGES + TEXT)
enko = UploadSet('enko', IMAGES + TEXT)
configure_uploads(app, ende)
configure_uploads(app, kor)
configure_uploads(app, enko)

####################
#### blueprints ####
####################
from project.nifi.views import nifi_blueprint
# register the blueprints
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
