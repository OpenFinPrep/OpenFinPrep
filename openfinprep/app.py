import os
import yaml
from flask import Blueprint, send_from_directory, Flask, render_template, make_response, jsonify, current_app, request
import pandas as pd
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

    def filter_by_text(df, param, columns, operator = 'contains'):
        p = request.args.get(param)

        if p is not None:
            sel = None
            for col in columns:
                if operator == 'contains':
                    if sel is None:
                        sel = df[col].str.contains(p, case=False)
                    else:
                        sel |= df[col].str.contains(p, case=False)
                elif operator == 'match':
                    if sel is None:
                        sel = df[col] == p
                    else:
                        sel |= df[col] == p
                else:
                    raise Exception("Invalid operator")

            df = df[sel]
        return df

    def filter_limit(df):
        p = request.args.get('limit')
        if p is not None:
            try:
                df = df.head(int(request.args.get('limit')))
            except ValueError:
                abort(400, description="Invalid limit")
        return df

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
        df = get_company_ticker_name_exchange()
        df = df.drop(columns=['cik'])

        df = filter_by_text(df, 'query', ['name', 'ticker'], 'contains')
        # df = filter_by_text(df, 'exchange', ['exchange'], 'match')
        df = filter_limit(df)

        return df.to_json(orient='records')

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

    
    @bp.errorhandler(400)
    def invalid_api(e):
        return jsonify({"error": str(e.description)}), 400

    @bp.errorhandler(500)
    def server_error(e):
        return jsonify({"error": str(e.description)}), 500

    @bp.errorhandler(403)
    def denied(e):
        return jsonify({"error": str(e.description)}), 403

    app = Flask(__name__, 
                static_url_path='', 
                static_folder=os.path.join(os.path.dirname(__file__), "webapp", "build"),
                template_folder=os.path.join(os.path.dirname(__file__), "webapp", "build"))

    if args.debug:
        app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.register_blueprint(bp, url_prefix="/api")
    
    return app