
# features_dict = {"Revenue": "1", "Cost Of Goods Sold": "2", "Gross Profit": "3",
#                  "Research And Development Expenses": "4", "SG&A Expenses": "5",
#                  "Other Operating Income Or Expenses": "6", "Operating Expenses": "7", "Operating Income": "8",
#                  "Total Non-Operating Income/Expense": "9", "Pre-Tax Income": "10", "Income Taxes": "11",
#                  "Income After Taxes": "12", "Other Income": "13", "Income From Continuous Operations": "14",
#                  "Income From Discontinued Operations": "15", "Net Income": "16", "EBITDA": "17", "EBIT": "18",
#                  "Basic Shares Outstanding": "19", "Shares Outstanding": "20", "Basic EPS": "21",
#                  "EPS - Earnings Per Share": "22"}

features_dict = {"Revenue": "1", "Cost Of Goods Sold": "2", "Gross Profit": "3", "Research And Development Expenses": "4",
                 "SG&A Expenses": "5", "Other Operating Income Or Expenses": "6", "Operating Expenses": "7",
                 "Operating Income": "8", "Total Non-Operating Income/Expense": "9", "Pre-Tax Income": "10",
                 "Income Taxes": "11", "Income After Taxes": "12", "Other Income": "13",
                 "Income From Continuous Operations": "14", "Income From Discontinued Operations": "15",
                 "Net Income": "16", "EBITDA": "17", "EBIT": "18", "Basic Shares Outstanding": "19",
                 "Shares Outstanding": "20", "Basic EPS": "21", "EPS - Earnings Per Share": "22", "Current Ratio": "23",
                 "Long-term Debt / Capital": "24", "Debt/Equity Ratio": "25", "Gross Margin": "26",
                 "Operating Margin": "27", "EBIT Margin": "28", "EBITDA Margin": "29", "Pre-Tax Profit Margin": "30",
                 "Net Profit Margin": "31", "Asset Turnover": "32", "Inventory Turnover Ratio": "33",
                 "Receiveable Turnover": "34", "Days Sales In Receivables": "35", "ROE - Return On Equity": "36",
                 "Return On Tangible Equity": "37", "ROA - Return On Assets": "38", "ROI - Return On Investment": "39",
                 "Book Value Per Share": "40", "Operating Cash Flow Per Share": "41", "Free Cash Flow Per Share": "42"}




reverse_features_dict = {v: k for k, v in features_dict.items()}


def get_feature_id(feature_name):
    return features_dict[feature_name]


def get_feature_name(feature_id):
    return reverse_features_dict[str(feature_id)]


def get_company_metrics_names(feature_ids):
    result = list(map(get_feature_name, feature_ids))
    return result



