import json
import os.path
import re
from typing import Optional, Any
from urllib.request import urlopen

from tqdm import tqdm


# "<a href='/stocks/charts/MSFT/microsoft/revenue'>Revenue</a>
from sampler.dao.CompaniesDAO import company_iterator
from sampler.dao.FeaturesDAO import get_feature_id
from utils.DateUtils import is_date
from utils.FileUtils import writeToFileAsJSON
from utils.SqlUtils import get_connection_cursor
from utils.StrUtils import getString

feature_name_pattern = re.compile('[^>]+>(.+)<')
original_data_pattern = re.compile('var originalData = (.+);\\s+var source =')

def extractFeautreName(link):
    found = feature_name_pattern.match(link)
    if found:
        found = found.group(1)
    return found


def populate_db_financial_statements():
    connection, cursor = get_connection_cursor()
    for (company_id, ticker, company_name) in tqdm(company_iterator()):
        json: Optional[Any] = getJsonFromMacrotrends(ticker, company_name)
        if (json):
            for dic in json:
                link = dic['field_name']
                feature_name = extractFeautreName(link)
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


def getJsonFromMacrotrends(tickerName, companyName) -> object:
    jsonStr = getTextFromMacrotrends(tickerName, companyName)
    if (jsonStr):
        return json.loads(jsonStr)
    return None


def extractOriginalData(text: object) -> object:
    match = original_data_pattern.search(text)
    # match = re.search('var originalData = (.+);\s+var source =', text)
    if (match):
        found = match.group(1)
        # print('extracted json', found)
        return found
    else:
        print('not found')
        return None


#################################################################################################

#
# try:
#     found = re.search('var originalData = (.+);\s+var source =', text).group(1)
# except AttributeError:
#     found = ''
# print(f'json =  {found}')
# return found


def getCompanyNameFromJsonFileTRY(tickerName):
    file = open('resources/tickersInfo.json', 'r')
    fileText = file.read()
    data = json.loads(fileText)
    for dic in data:
        if dic["ticker"] == tickerName:
            return dic["comp_name"]

    return 'unknown'

def getTickersInfoTRY(list):
    dic = dict()
    for ticker in list:
        tickerInfo = getTickerInfoFromJsonFileTRY(ticker)
        dic[ticker] = tickerInfo
    return dic


def getTickerInfoFromJsonFileTRY(tickerName):
    tickerFileName = 'resources\\' + tickerName + '.json'
    if os.path.isfile(tickerFileName):
        file = open(tickerFileName, 'r')
        fileText = file.read()
        data = json.loads(fileText)
    else:
        companyName = getCompanyNameFromJsonFileTRY(tickerName)
        print(f'loading {companyName} ticker: {tickerName} info')
        jsonStr = getTextFromMacrotrends(tickerName, companyName)
        data = json.loads(jsonStr)
        writeToFileAsJSON(data, tickerFileName)
    return data
