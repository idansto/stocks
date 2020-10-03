from databuilder.bl.FeaturesDataBuilderBL import extractFeautreName
from utils.FileUtils import getJsonFromFile
from utils.SqlUtils import get_connection_cursor


def fillDBFeatures():
    data = getJsonFromFile('../../../resources/MSFT.json')
    connection, cursor = get_connection_cursor()
    for dic in data:
        link = dic['field_name']
        featureName = extractFeautreName(link)
        sql = "INSERT INTO shares.features (name) VALUES (%s)"
        val = [featureName]
        cursor.execute(sql, val)
        print(featureName)
    connection.commit()


# features_dict = {'revenue': '1', 'sales': '2'}
def print_feature_dict():
    connection, cursor = get_connection_cursor()
    sql = "select f.id, f.name from shares.features f"
    cursor.execute(sql)
    print("features_dict = {", end='')
    for (id, name) in cursor:
        print('"', name, '": ', '"', id, '", ', sep='', end='')
    print("}")

##################################################################################################


def printFeautresTRY() -> None:
    data = getJsonFromFile('../../../resources/MSFT.json')
    maxSize = 0
    for dic in data:
        link = dic['field_name']
        featureName = extractFeautreName(link)
        print(featureName)
        maxSize = max(maxSize, len(featureName))
    print('maxsize = ', maxSize, len(data))



