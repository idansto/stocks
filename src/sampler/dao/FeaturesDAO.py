
features_dict = {"Revenue": "1", "Cost Of Goods Sold": "2", "Gross Profit": "3",
                 "Research And Development Expenses": "4", "SG&A Expenses": "5",
                 "Other Operating Income Or Expenses": "6", "Operating Expenses": "7", "Operating Income": "8",
                 "Total Non-Operating Income/Expense": "9", "Pre-Tax Income": "10", "Income Taxes": "11",
                 "Income After Taxes": "12", "Other Income": "13", "Income From Continuous Operations": "14",
                 "Income From Discontinued Operations": "15", "Net Income": "16", "EBITDA": "17", "EBIT": "18",
                 "Basic Shares Outstanding": "19", "Shares Outstanding": "20", "Basic EPS": "21",
                 "EPS - Earnings Per Share": "22"}

def get_feature_id(feature_name):
    return features_dict[feature_name]


