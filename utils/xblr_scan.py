import argparse
from edgar import *

set_identity("ofp@openfinprep.org")

parser = argparse.ArgumentParser(
    description="Find amounts in filings"
)
parser.add_argument(
    "company", type=str, help="Symbol"
)
parser.add_argument(
    "amount", type=float, help="Amount"
)
parser.add_argument(
    "--form", type=str, help="Form (%(default)s)", default="10-K"
)

args = parser.parse_args()

c = Company(args.company)
filings = c.get_filings(form=[args.form])
financials = filings[0].obj().financials
xinst = financials.xbrl_data.instance

for i, row in xinst.query_facts().iterrows():
    try:
        v = float(row['value'])
        if v == args.amount:
            print(row['concept'])
    except:
        continue