from flask import Blueprint, Flask, render_template, make_response

def create_app(args):
    bp = Blueprint('Main app', __name__)

    @bp.route("/")
    def index():
        return make_response(render_template("index.html"))

    app = Flask(__name__)

    if args.debug:
        app.config["TEMPLATES_AUTO_RELOAD"] = True
    if args.url_prefix:
        app.register_blueprint(bp, url_prefix=args.url_prefix)
    else:
        app.register_blueprint(bp)
    
    return app