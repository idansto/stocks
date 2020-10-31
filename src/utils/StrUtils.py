


def getString(bytes):
    return "".join(chr(x) for x in bytes)


def create_comma_sperated_list(company_ids):
    return ",".join(map(str, company_ids))

def create_comma_sperated__quoated_list(company_ids):
    return ",".join(map(quote, company_ids))

def quote(str):
    return f"'{str}'"