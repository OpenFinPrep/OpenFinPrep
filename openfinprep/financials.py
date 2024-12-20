import math

def file_period_to_json(file):
    financials = file.obj().financials
    xinst = financials.xbrl_data.instance

    # To find keys in xinst:
    # xinst.facts.index.get_level_values('concept')[xinst.facts.index.get_level_values('concept').str.contains("Interest")]

    stmt = financials.get_income_statement().data
    stmt.to_csv("gaap.csv")
    level_0 = stmt[stmt['level'] == 0]
    level_1 = stmt[stmt['level'] == 1]

    period = {}
    added_0 = {}
    for i, row in level_0.iterrows():
        if row['concept'] not in period:
            item = float(row.iloc[0])
            if not math.isnan(item):
                period[row['concept']] = item
                added_0[row['concept']] = True
    
    for i, row in level_1.iterrows():
        concept = row['concept']
        if concept in added_0:
            continue
        if concept not in period:
            period[concept] = 0.0
        
        item = float(row.iloc[0])
        if not math.isnan(item):
            period[concept] += item

    def get_attr(keys, cast = int, fallback=None):
        if isinstance(keys, str):
            keys = [keys]
        
        for k in keys:
            if k in period:
                return cast(period[k])
        if fallback is not None:
            return cast(query_attr(fallback))
        
        return 0

    def query_attr(keys, cast = int):
        if isinstance(keys, str):
            keys = [keys]

        for k in keys:
            k = k.replace("_", ":")
            df = xinst.facts[xinst.facts.index.get_level_values('concept').str.endswith(k)]
            if len(df) > 0:
                return cast(df['value'].iloc[0])

        return 0

    def abs_int(v):
        return abs(int(v))


    r = {
        'fillingDate': str(file.filing_date),
        'cik': str(file.cik).zfill(10),
        'period': financials.xbrl_data.instance.get_fiscal_period_focus(),
        'revenue': get_attr(['us-gaap_Revenues', 'us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax'], abs_int),
        'costOfRevenue': get_attr('us-gaap_CostOfGoodsAndServicesSold', abs_int),
        'grossProfit': get_attr('us-gaap_GrossProfit'),
        'researchAndDevelopmentExpenses': get_attr('us-gaap_ResearchAndDevelopmentExpense', abs_int),
        'generalAndAdministrativeExpenses': get_attr('us-gaap_GeneralAndAdministrativeExpense', abs_int),
        'sellingAndMarketingExpenses': get_attr('us-gaap_SellingAndMarketingExpense', abs_int),
        'sellingGeneralAndAdministrativeExpenses': get_attr('us-gaap_SellingGeneralAndAdministrativeExpense', abs_int),
        'otherExpenses': 0,
        'totalOtherIncomeExpensesNet': get_attr('us-gaap_NonoperatingIncomeExpense'),
        'operatingIncome': get_attr('us-gaap_OperatingIncomeLoss'),
        'incomeBeforeTax': get_attr('us-gaap_IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest'),
        'netIncome': get_attr('us-gaap_NetIncomeLoss'),
        'eps': get_attr('us-gaap_EarningsPerShareBasic', float),
        'epsdiluted': get_attr('us-gaap_EarningsPerShareDiluted', float),
        'weightedAverageShsOut': get_attr('us-gaap_WeightedAverageNumberOfSharesOutstandingBasic'),
        'weightedAverageShsOutDil': get_attr('us-gaap_WeightedAverageNumberOfDilutedSharesOutstanding'),
        'incomeTaxExpense': 0,
        'operatingExpenses': 0,
        'costAndExpenses': 0,
        'interestExpense': get_attr([], int, fallback='us-gaap_InterestExpense'),
        'interestIncome': get_attr([], int, fallback='us-gaap_InvestmentIncomeNet'),
        'depreciationAndAmortization': query_attr(['us-gaap_DepreciationDepletionAndAmortization', 'DepreciationAmortizationAndOther'], int),
        'ebidta': 0,
    }

    def compute_sub(key, v1, v2):
        if r[key] == 0 and r[v1] > 0 and r[v2] > 0:
            r[key] = r[v1] - r[v2]

    def compute_add(key, v1, v2):
        if r[key] == 0 and r[v1] > 0 and r[v2] > 0:
            r[key] = r[v1] + r[v2]

    def compute_expr(key, expr):
        if r[key] == 0:
            r[key] = eval(expr, None, r)

    def compute_ratio(key, v1, v2):
        if v1 in r and r[v2] != 0:
            r[key] = r[v1] / r[v2]
        else:
            r[key] = 0

    compute_expr('grossProfit', 'revenue - costOfRevenue')
    compute_expr('sellingGeneralAndAdministrativeExpenses', 'sellingAndMarketingExpenses + generalAndAdministrativeExpenses')
    compute_expr('incomeTaxExpense', 'incomeBeforeTax - netIncome')
    compute_expr('operatingExpenses', 'grossProfit - operatingIncome')
    compute_expr('costAndExpenses', 'revenue - operatingIncome')
    compute_expr('ebidta', 'operatingIncome + depreciationAndAmortization')

    compute_ratio('grossProfitRatio', 'grossProfit', 'revenue')
    compute_ratio('operatingIncomeRatio', 'operatingIncome', 'revenue')
    compute_ratio('incomeBeforeTaxRatio', 'incomeBeforeTax', 'revenue')
    compute_ratio('netIncomeRatio', 'netIncome', 'revenue')
    compute_ratio('ebitdaratio', 'ebidta', 'revenue')
    

    # Compute additional ratios
    # if r['revenue']:
    #     r['grossProfitRatio'] = r['grossProfit'] / r['revenue']

    return r