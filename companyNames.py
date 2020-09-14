import json


def get_all_company_names():
    file = open('tickersInfo.json', 'r')
    json_obj = json.load(file)
    dic = dict()
    for tickerInfo in json_obj:
        dic[tickerInfo["ticker"]] = tickerInfo["comp_name"]
    return dic


if __name__ == '__main__':
    company_names_dic = get_all_company_names()
    print(company_names_dic)
