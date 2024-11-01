from flask import Blueprint, Flask, render_template, make_response
from edgar.reference.tickers import get_company_ticker_name_exchange 
from edgar import set_identity, use_local_storage
import yaml

def create_app(args):
    bp = Blueprint('Main app', __name__)
    set_identity("openfinprep@openfinprep.org")
    if args.use_local_storage:
        use_local_storage()

    @bp.route("/")
    def index():
        return make_response(render_template("index.html"))

    @bp.route("/stock/list")
    def stock_list():
        """
        name: Symbol List
        group: Stock List
        params: []
        tags: 
         - label: Test
           color: yellow
        """
        companies = get_company_ticker_name_exchange()
        companies = companies.drop(columns=['cik'])
        return companies.to_json(orient='records')

    @bp.route("/cik_list")
    def cik_list():
        """
        name: CIK List
        group: Stock List
        params: []
        tags: []
        """
        companies = get_company_ticker_name_exchange()
        companies = companies.drop(columns=['ticker', 'exchange'])
        companies['cik'] = companies['cik'].apply(lambda x: str(x).zfill(10))
        return companies.to_json(orient='records')

    @bp.route("/endpoints")
    def endpoints():
        ep = [
            stock_list,
            cik_list,
        ]

        for e in ep:
            specs = yaml.safe_load(e.__doc__)
        print(specs)

        # TODO: group/endpoint sorting order?
        
        return "{}"

    app = Flask(__name__)

    if args.debug:
        app.config["TEMPLATES_AUTO_RELOAD"] = True
    if args.url_prefix:
        app.register_blueprint(bp, url_prefix=args.url_prefix)
    else:
        app.register_blueprint(bp)
    
    return app