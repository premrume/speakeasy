################
# main login stuff
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

################
# nifi stuff
from flask_uploads import UploadSet, IMAGES, TEXT
from flask_mongoengine import MongoEngine

dbm = MongoEngine()

################
#### flask-uploads pain ####
################
ende = UploadSet('ende', IMAGES + TEXT)
kor = UploadSet('kor', IMAGES + TEXT)
enko = UploadSet('enko', IMAGES + TEXT)
