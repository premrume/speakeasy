from flask import Flask


def create_app():

    server = Flask(__name__, instance_relative_config=True)

    config(server)

    register_extensions_main(server)
    register_blueprints_main(server)

    register_extensions_nifi(server)
    register_blueprints_nifi(server)
 
    seattle(server)

    return server

def config(server):
    server.config.from_pyfile('flask.cfg')

def register_extensions_main(server):
    from app.extensions import db
    from app.extensions import login
    from app.extensions import migrate
    db.init_app(server)
    login.init_app(server)
    login.login_view = 'main.login'
    migrate.init_app(server, db)


def register_blueprints_main(server):
    from app.main.webapp import server_bp
    server.register_blueprint(server_bp)

def register_extensions_nifi(server):
    from app.extensions import dbm, ende, kor, enko
    from flask_uploads import configure_uploads
    dbm.init_app(server)
    configure_uploads(server, ende)
    configure_uploads(server, kor)
    configure_uploads(server, enko)

def register_blueprints_nifi(server):
    from app.nifi.views import nifi_blueprint
    server.register_blueprint(nifi_blueprint)

def seattle(server):
    ############################
    #### custom error pages ####
    ############################
    from flask import render_template
    @server.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @server.errorhandler(403)
    def page_not_found(e):
        return render_template('403.html'), 403

    @server.errorhandler(410)
    def page_not_found(e):
        return render_template('410.html'), 410

