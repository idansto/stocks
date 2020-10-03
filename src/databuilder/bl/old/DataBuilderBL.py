import json
import re
from urllib.request import urlopen
import os.path


class DataBuilder:

    def get_data(self, list):
        dic = dict()
        for ticker in list:
            ticker_info = self.getTickerInfo(ticker)
            dic[ticker] = ticker_info
        return dic

    def writeToFile(self, data, file_name):
        file = open(file_name, 'w')
        json.dump(data, file)

    def getTickerInfo(self, ticker_name):
        ticker_file_name = ticker_name + '.json'
        if os.path.isfile(ticker_file_name):
            file = open(ticker_file_name, 'r')
            file_text = file.read()
            data = json.loads(file_text)
        else:
            company_name = self.getCompanyName(ticker_name)
            print(f'loading {company_name} ticker: {ticker_name} info')
            json_str = self.get_json_from_macrotrends(ticker_name, company_name)
            data = json.loads(json_str)
            self.writeToFile(data, ticker_file_name)
        return data

    def getCompanyName(self, ticker_name):
        file = open('../../../../resources/tickersInfo.json', 'r')
        file_text = file.read()
        data = json.loads(file_text)
        for dic in data:
            if dic["ticker"] == ticker_name:
                return dic["comp_name"]

        return 'unknown'

    # url pattern example: "https://www.macrotrends.net/stocks/charts/MSFT/microsoft/financial-statements"
    def get_json_from_macrotrends(self, ticker_name, company_name):
        url = 'https://www.macrotrends.net/stocks/charts/{}/{}/financial-statements?freq=Q'.format(ticker_name,
                                                                                                   company_name)
        connection = urlopen(url)
        html = connection.read()
        print(f'html = {html}')
        text = self.getString(html)
        return self.extract_original_data(text)

    def extract_original_data(self, text):
        try:
            found = re.search('var originalData = (.+);\s+var source =', text).group(1)
        except AttributeError:
            found = ''
        print(f'json =  {found}')
        return found

    def getString(self, bytes):
        return "".join(chr(x) for x in bytes)

    if __name__ == '__main__':
        data = getTickerInfo('aapl')
        print(data)
        print(data[5]['2019-06-30'])
