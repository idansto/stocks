import json

from utils.FileUtils import getJsonFromFile
from utils.SqlUtils import get_connection_cursor


def fillDBCompaniesFromJsonFile():
    data = getJsonFromFile('../../../resources/stock-screener.json')
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

#########################################################################################################

def printCompaniesStockScreenHeadersTRY():
    file = open('../../../resources/stock-screener.json', 'r')
    fileText = file.read()
    data = json.loads(fileText)
    dic = data[0]
    for key in dic:
        print(key)