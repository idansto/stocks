from urllib.request import *
import re
from html.parser import HTMLParser
from html.entities import name2codepoint


#
#
# class MyHTMLParser(HTMLParser):
#     contents = ""
#
#     def error(self, message):
#         pass
#
#     def handle_starttag(self, tag, attrs):
#         # print("Start tag:", tag)
#         for attr in attrs:
#             pass
#             # print("     attr:", attr)
#
#     def handle_endtag(self, tag):
#         pass
#         # print("End tag  :", tag)
#
#     def handle_data(self, data):
#         # print("Data     :", data)
#         self.contents += data
#
#     def handle_comment(self, data):
#         pass
#         # print("Comment  :", data)
#
#     def handle_entityref(self, name):
#         c = chr(name2codepoint[name])
#         # print("Named ent:", c)
#
#     def handle_charref(self, name):
#         if name.startswith('x'):
#             c = chr(int(name[1:], 16))
#         else:
#             c = chr(int(name))
#         # print("Num ent  :", c)
#
#     def handle_decl(self, data):
#         pass
#         # print("Decl     :", data)
#
#
# parser = MyHTMLParser()
class RevenuesGetter:

    @staticmethod
    def get_revenues(company_name, ticker):
        revenues = []
        url = "https://www.macrotrends.net/stocks/charts/" + ticker + "/" + company_name + "/financial-statements"
        f = urlopen(url)
        my_file = f.read()
        my_file = str(my_file)

        print(my_file)
        substring = '{"field_name":"<a href=\'\\/stocks\\/charts\\/MSFT\\/microsoft\\/revenue\'>Revenue<\\/a>","popup_icon":"<div class=\'ajax-chart\' data-tipped-options=\\"ajax: {data: { t: \'MSFT\', s: \'revenue\', freq: \'A\', statement: \'financial-statements\' }}\\"><i style=\'font-size:18px; color:#337ab7;\' class=\'fas fa-chart-bar\'><\\/i><\\/span><\\/div>",'
        # print(parser.contents)
        # idx = parser.contents.find(substring)
        return revenues
