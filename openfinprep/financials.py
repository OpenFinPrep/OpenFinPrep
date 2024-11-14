
def file_period_to_json(file, period):
    def get_attr(keys, cast = int):
        for k in keys:
            if k in period:
                return cast(period[k]) 
        return None

    return {
        'fillingDate': str(file.filing_date),
        'cik': str(file.cik).zfill(10),
        'revenue': get_attr(['Revenue', 'Net sales'])
    }