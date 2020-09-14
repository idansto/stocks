import json
import re
from urllib.request import urlopen
import os.path


def getTickersInfo(list):
    dic = dict()
    for ticker in list:
        ticker_info = getTickerInfo(ticker)
        dic[ticker] = ticker_info
    return dic


def writeToFile(data, file_name):
    file = open(file_name, 'w')
    json.dump(data, file)


def getTickerInfo(tickerName):
    ticker_file_name = tickerName + '.json'
    if os.path.isfile(ticker_file_name):
        file = open(ticker_file_name, 'r')
        file_text = file.read()
        data = json.loads(file_text)
    else:
        company_name = getCompanyName(tickerName)
        print(f'loading {company_name} ticker: {tickerName} info')
        json_str = get_json_from_macrotrends(tickerName, company_name)
        data = json.loads(json_str)
        writeToFile(data, ticker_file_name)
    return data


def getCompanyName(ticker_name):
    file = open('tickersInfo.json', 'r')
    file_text = file.read()
    data = json.loads(file_text)
    for dic in data:
        if dic["ticker"] == ticker_name:
            return dic["comp_name"]

    return 'unknown'


# url pattern example: "https://www.macrotrends.net/stocks/charts/MSFT/microsoft/financial-statements"
def get_json_from_macrotrends(ticker_name, company_name):
    url = 'https://www.macrotrends.net/stocks/charts/{}/{}/financial-statements?freq=Q'.format(ticker_name,
                                                                                               company_name)
    connection = urlopen(url)
    html = connection.read()
    print(f'html = {html}')
    text = getString(html)
    return extractOriginalData(text)


def extractOriginalData(text):
    try:
        found = re.search('var originalData = (.+);\s+var source =', text).group(1)
    except AttributeError:
        found = ''
    print(f'json =  {found}')
    return found


def getString(bytes):
    return "".join(chr(x) for x in bytes)


if __name__ == '__main__':
    data = getTickerInfo('COKE')
    print(data)
    print(data[5]['2019-06-30'])
