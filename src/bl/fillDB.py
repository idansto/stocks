# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import json
import re
from urllib.request import urlopen
import os.path
from tqdm import tqdm
from src.utils.sqlUtils import get_connection_cursor

features_dict = {"Revenue": "1", "Cost Of Goods Sold": "2", "Gross Profit": "3",
                 "Research And Development Expenses": "4", "SG&A Expenses": "5",
                 "Other Operating Income Or Expenses": "6", "Operating Expenses": "7", "Operating Income": "8",
                 "Total Non-Operating Income/Expense": "9", "Pre-Tax Income": "10", "Income Taxes": "11",
                 "Income After Taxes": "12", "Other Income": "13", "Income From Continuous Operations": "14",
                 "Income From Discontinued Operations": "15", "Net Income": "16", "EBITDA": "17", "EBIT": "18",
                 "Basic Shares Outstanding": "19", "Shares Outstanding": "20", "Basic EPS": "21",
                 "EPS - Earnings Per Share": "22"}

date_pattern = re.compile("^\d{4}-\d{1,2}-\d{1,2}$")
feature_name_pattern = re.compile('[^>]+>(.+)<')
original_data_pattern = re.compile('var originalData = (.+);\s+var source =')


def getTickersInfo(list):
    dic = dict()
    for ticker in list:
        tickerInfo = getTickerInfo(ticker)
        dic[ticker] = tickerInfo
    return dic


def writeToFile(data, fileName):
    file = open(fileName, 'w')
    json.dump(data, file)


def getTickerInfo(tickerName):
    tickerFileName = 'resources\\' + tickerName + '.json'
    if os.path.isfile(tickerFileName):
        file = open(tickerFileName, 'r')
        fileText = file.read()
        data = json.loads(fileText)
    else:
        companyName = getCompanyName(tickerName)
        print(f'loading {companyName} ticker: {tickerName} info')
        jsonStr = getTextFromMacrotrends(tickerName, companyName)
        data = json.loads(jsonStr)
        writeToFile(data, tickerFileName)
    return data


def getCompanyName(tickerName):
    file = open('resources/tickersInfo.json', 'r')
    fileText = file.read()
    data = json.loads(fileText)
    for dic in data:
        if dic["ticker"] == tickerName:
            return dic["comp_name"]

    return 'unknown'


# url pattern example: "https://www.macrotrends.net/stocks/charts/MSFT/microsoft/income-statement?freq=Q"
def getTextFromMacrotrends(tickerName, companyName):
    url = 'https://www.macrotrends.net/stocks/charts/{}/{}/income-statement?freq=Q'.format(tickerName, companyName)
    print(f'url = {url}')
    try:
        connection = urlopen(url)
        html = connection.read()
        # print(f'html = {html}')
        text = getString(html)
        return extractOriginalData(text)
    except:
        print(f'failed to read url: {url}')
        return None


def getJsonFromMacrotrends(tickerName, companyName):
    jsonStr = getTextFromMacrotrends(tickerName, companyName)
    if (jsonStr):
        return json.loads(jsonStr)
    return None


def extractOriginalData(text):
    match = original_data_pattern.search(text)
    # match = re.search('var originalData = (.+);\s+var source =', text)
    if (match):
        found = match.group(1)
        # print('extracted json', found)
        return found
    else:
        print('not found')
        return None
    #
    # try:
    #     found = re.search('var originalData = (.+);\s+var source =', text).group(1)
    # except AttributeError:
    #     found = ''
    # print(f'json =  {found}')
    # return found


def getString(bytes):
    return "".join(chr(x) for x in bytes)


def printStockScreenHeaders():
    file = open('../../resources/stock-screener.json', 'r')
    fileText = file.read()
    data = json.loads(fileText)
    dic = data[0]
    for key in dic:
        print(key)


def fillDBCompanies():
    data = getJsonFromFile('../../resources/stock-screener.json')
    connection, cursor = get_connection_cursor()
    tickerMax = comp_nameMax = comp_name_2Max = exchangeMax = zacks_x_ind_descMax = zacks_x_sector_descMax = zacks_m_ind_descMax = emp_cntMax = 0

    for dic in data:
        ticker = dic['ticker']
        comp_name = dic['comp_name']
        comp_name_2 = dic['comp_name_2']
        exchange = dic['exchange']
        zacks_x_ind_desc = dic['zacks_x_ind_desc']
        zacks_x_sector_desc = dic['zacks_x_sector_desc']
        zacks_m_ind_desc = dic['zacks_m_ind_desc']
        emp_cnt = dic['emp_cnt']

        tickerMax = max(len(ticker), tickerMax)
        comp_nameMax = max(len(comp_name), comp_nameMax)
        comp_name_2Max = max(len(comp_name_2), comp_name_2Max)
        exchangeMax = max(len(exchange), exchangeMax)
        zacks_x_ind_descMax = max(len(zacks_x_ind_desc), zacks_x_ind_descMax)
        zacks_x_sector_descMax = max(len(zacks_x_sector_desc), zacks_x_sector_descMax)
        zacks_m_ind_descMax = max(len(zacks_m_ind_desc), zacks_m_ind_descMax)
        emp_cntMax = max(len(emp_cnt), emp_cntMax)

        sql = "INSERT INTO shares.companies (ticker, comp_name, comp_name_2, exchange, zacks_x_ind_desc, zacks_x_sector_desc, zacks_m_ind_desc, emp_cnt) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = [ticker, comp_name, comp_name_2, exchange, zacks_x_ind_desc, zacks_x_sector_desc, zacks_m_ind_desc,
               emp_cnt]
        print(*val, sep=",")

        cursor.execute(sql, val)

    val = [tickerMax, comp_nameMax, comp_name_2Max, exchangeMax, zacks_x_ind_descMax, zacks_x_sector_descMax,
           zacks_m_ind_descMax, emp_cntMax]
    print(*val, sep=",")
    connection.commit()


def getJsonFromFile(fileName):
    file = open(fileName, 'r')
    fileText = file.read()
    data = json.loads(fileText)
    return data


def fillDBFeatures():
    data = getJsonFromFile('../../resources/MSFT.json')
    connection, cursor = get_connection_cursor()
    for dic in data:
        link = dic['field_name']
        featureName = extractFeautre(link)
        sql = "INSERT INTO shares.features (name) VALUES (%s)"
        val = [featureName]
        cursor.execute(sql, val)
        print(featureName)
    connection.commit()


# "<a href='/stocks/charts/MSFT/microsoft/revenue'>Revenue</a>
def extractFeautre(link):
    found = feature_name_pattern.match(link)
    if (found):
        found = found.group(1)
    return found


def printFeautres():
    data = getJsonFromFile('../../resources/MSFT.json')
    maxSize = 0
    for dic in data:
        link = dic['field_name']
        featureName = extractFeautre(link)
        print(featureName)
        maxSize = max(maxSize, len(featureName))
    print('maxsize = ', maxSize, len(data))


def tickerCompanyNameIterator():
    connection, cursor = get_connection_cursor()
    sql = "select c.ticker, c.comp_name from shares.companies c"
    cursor.execute(sql)
    return cursor.fetchall()
    # print('cursor = ',cursor)
    # for row in cursor:
    #     print('row = ', row)


def company_iterator():
    connection, cursor = get_connection_cursor()
    sql = "select c.id, c.ticker, c.comp_name from shares.companies c where c.ticker >= 'CLUB'"
    cursor.execute(sql)
    return cursor.fetchall()
    # print('cursor = ',cursor)
    # for row in cursor:
    #     print('row = ', row)


def financial_statements_URL_iterator():
    for (ticker, company_name) in tqdm(tickerCompanyNameIterator()):
        url = 'https://www.macrotrends.net/stocks/charts/{}/{}/income-statement?freq=Q'.format(ticker, company_name)
        print(url)


def get_feature_id(feature_name):
    return features_dict[feature_name]


def populate_db_financial_statements():
    connection, cursor = get_connection_cursor()
    for (company_id, ticker, company_name) in tqdm(company_iterator()):
        json = getJsonFromMacrotrends(ticker, company_name)
        if (json):
            for dic in json:
                link = dic['field_name']
                feature_name = extractFeautre(link)
                for key in dic:
                    if (is_date(key)):
                        date = key
                        value = dic[date]
                        if (value):
                            feature_id = get_feature_id(feature_name)
                            sql = "INSERT INTO shares.feature_data (company_id, feature_id, date, value) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE value=%s"
                            val = [company_id, feature_id, date, value, value]
                            cursor.execute(sql, val)
                connection.commit()


def is_date(key):
    result = date_pattern.match(key)
    # print(key, pattern, result)
    return result


# features_dict = {'revenue': '1', 'sales': '2'}
def print_feature_dict():
    connection, cursor = get_connection_cursor()
    sql = "select f.id, f.name from shares.features f"
    cursor.execute(sql)
    print("features_dict = {", end='')
    for (id, name) in cursor:
        print('"', name, '": ', '"', id, '", ', sep='', end='')
    print("}")


if __name__ == '__main__':
    pass
    # json = json.loads(None)
    # print (json)
    # print(extractFeautre("sdf"))
    # print(extractFeautre("df <a href = '/stocks/charts/MSFT/microsoft/revenue'>Revenue</a> "))
    # populate_db_financial_statements()
    # populate_db_financial_statements()
    # print_feature_dict()
#  is_date("sdfsd")
# is_date("2001-3-31")
#  is_date("2")
#  is_date("1234")
# # financial_statements_URL_iterator()
# tickerCompanyNameIterator()
# printFeautres()
# fillDBFeatures()
# fillDBCompanies()
# printStockScreenHeaders()
# jsonStr = getTextFromMacrotrends('MSFT', 'companyName')
# data = json.loads(jsonStr)
# # data = getTickerInfo('COKE')
# print(data)
# # print(data[0]['2019-06-30'])
# print(data[0]['field_name'])
