import os
import yaml
from flask import Blueprint, send_from_directory, Flask, render_template, make_response, jsonify, current_app
from edgar.reference.tickers import get_company_ticker_name_exchange 
from edgar import set_identity, use_local_storage

def create_app(args):
    bp = Blueprint('ofp', __name__)
    set_identity("openfinprep@openfinprep.org")
    if args.use_local_storage:
        use_local_storage()


    @bp.route("/")
    def index():
        return render_template("index.html")

    @bp.route("/search")
    def general_search():
        """
        name: General Search
        group: Company Search
        params: 
         - name: query
           default: AA
         - name: limit
           type: number
         - name: exchange
        tags: []
        """
        companies = get_company_ticker_name_exchange()
        companies = companies.drop(columns=['cik'])
        return companies.to_json(orient='records')

    @bp.route("/cik_search")
    def cik_search():
        """
        name: CIK Search
        group: Company Search
        params: []
        tags: []
        """
        companies = get_company_ticker_name_exchange()
        companies = companies.drop(columns=['ticker', 'exchange'])
        companies['cik'] = companies['cik'].apply(lambda x: str(x).zfill(10))
        return companies.to_json(orient='records')

    @bp.route("/income-statement")
    def income_statement():
        """
        name: Income Statement
        group: Financial Statements
        params: []
        tags:
         - label: Annual/Quarter
           type: info
        """
        return [{}]

    @bp.route("/endpoints")
    def endpoints():
        """
         - Company Search
         - Financial Statements
        """
        ep = [
            general_search,
            cik_search,
            income_statement,
        ]

        groups = yaml.safe_load(endpoints.__doc__)
        output = [{'group': g, 'endpoints': []} for g in groups]

        urls = current_app.url_map.bind("openfinprep.org", "/")
        specs = []

        for e in ep:
            spec = yaml.safe_load(e.__doc__)
            group_id = groups.index(spec['group'])
            del spec['group']
            spec['url'] = urls.build("ofp." + e.__name__, {})
            output[group_id]['endpoints'].append(spec)

        return jsonify(output)

    app = Flask(__name__, 
                static_url_path='', 
                static_folder=os.path.join(os.path.dirname(__file__), "webapp", "build"),
                template_folder=os.path.join(os.path.dirname(__file__), "webapp", "build"))

    if args.debug:
        app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.register_blueprint(bp, url_prefix="/api")
    
    return app