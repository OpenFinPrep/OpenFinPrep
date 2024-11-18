import math

def file_period_to_json(file):
    financials = file.obj().financials
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

    def get_attr(keys, cast = int):
        for k in keys:
            if k in period:
                return cast(period[k]) 
        return 0

    def abs_int(v):
        return abs(int(v))


    #TODO: totalOtherIncomeExpensesNet for DIS incorrect?
    
    r = {
        'fillingDate': str(file.filing_date),
        'cik': str(file.cik).zfill(10),
        'period': financials.xbrl_data.instance.get_fiscal_period_focus(),
        'revenue': get_attr(['us-gaap_Revenues', 'us-gaap_RevenueFromContractWithCustomerExcludingAssessedTax'], abs_int),
        'costOfRevenue': get_attr(['us-gaap_CostOfGoodsAndServicesSold'], abs_int),
        'grossProfit': get_attr(['us-gaap_GrossProfit']),
        'researchAndDevelopmentExpenses': get_attr(['us-gaap_ResearchAndDevelopmentExpense'], abs_int),
        'generalAndAdministrativeExpenses': get_attr(['us-gaap_GeneralAndAdministrativeExpense'], abs_int),
        'sellingAndMarketingExpenses': get_attr(['us-gaap_SellingAndMarketingExpense'], abs_int),
        'sellingGeneralAndAdministrativeExpenses': get_attr(['us-gaap_SellingGeneralAndAdministrativeExpense'], abs_int),
        'totalOtherIncomeExpensesNet': get_attr(['us-gaap_NonoperatingIncomeExpense'])
        
    }

    def compute_sub(key, v1, v2):
        if r[key] == 0 and r[v1] > 0 and r[v2] > 0:
            r[key] = r[v1] - r[v2]

    def compute_add(key, v1, v2):
        if r[key] == 0 and r[v1] > 0 and r[v2] > 0:
            r[key] = r[v1] + r[v2]

    def compute_ratio(key, v1, v2):
        if v1 in r and r[v2] != 0:
            r[key] = r[v1] / r[v2]
        else:
            r[key] = 0

    compute_sub('grossProfit', 'revenue', 'costOfRevenue')
    compute_add('sellingGeneralAndAdministrativeExpenses', 'sellingAndMarketingExpenses', 'generalAndAdministrativeExpenses')
    compute_ratio('grossProfitRatio', 'grossProfit', 'revenue')

    # Compute additional ratios
    # if r['revenue']:
    #     r['grossProfitRatio'] = r['grossProfit'] / r['revenue']

    return r