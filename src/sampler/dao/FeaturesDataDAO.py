from tqdm import tqdm

from sampler.dao.CompaniesDAO import tickerCompanyNameIteratorTRY


def financial_statements_URL_iteratorTRY():
    for (ticker, company_name) in tqdm(tickerCompanyNameIteratorTRY()):
        url = 'https://www.macrotrends.net/stocks/charts/{}/{}/income-statement?freq=Q'.format(ticker, company_name)
        print(url)


