import json


def do():
    file = open('tickersInfo.json', 'r')
    jsonObj = json.load(file)
    dic = dict()
    for tickerInfo in jsonObj:
        # print(f'{tickerInfo["ticker"]} {tickerInfo["comp_name"]}')
        dic[tickerInfo["ticker"]] = tickerInfo["comp_name"]
    return dic


if __name__ == '__main__':
    dic = do()
    print(dic)
