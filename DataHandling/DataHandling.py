import pandas as pd
import numpy as np
from HandlingFunc import *
import matplotlib.pyplot as plt


### Final_rating will be the y-value (tagging). probably above/below 4.
### Need to understand how to deal with 'Description'.

display_options(maxRows=False)
originalDataSet = (pd.read_csv('../DataAcquisition/gamesDataSet.csv'))
df = originalDataSet.copy()

# At first, using info() and describe() functions, we can see we have no missing-values, due to the strict
# assigning at the acquisition stage, where a missing value was instantly assigned the value 0 or -1.
# The problem is mainly dealing with missing prices (-1) and missing ratings (-1) for products.


def handle_data(dataframe, saveNoRatingDf=False, months=True, otherFeatures=True, format=True, platform=True, os=True,
                genre=True, brand=True, worthyColumn=True, fixPrices=True):
    handle_duplicates(dataframe)
    if months:
        handle_months(dataframe)
    if otherFeatures:
        handle_other_features(dataframe)
    if format:
        handle_format(dataframe)
    if platform:
        handle_platform(dataframe)
    if os:
        handle_operating_system(dataframe)
        handle_sub_operating_system(dataframe)
    if genre:
        handle_genre(dataframe)
        handle_sub_genre(dataframe)
    if brand:
        handle_brand(dataframe)
    if worthyColumn:
        dataframe = create_new_worthy_column_seperated_by_rating_x(dataframe, 4)
    if fixPrices:
        fix_missing_values_for_price_and_discount(dataframe)
    remove_outliers(dataframe)
    dataframe = remove_products_with_no_rating_and_save_them_to_csv(dataframe, saveNoRatingDf)
    # remove_columns_for_learning(df)
    dataframe.set_index('Name', inplace=True)
    return dataframe

print(handle_data(df).describe(include='all'))
print('\n\n\n')


# # Cancel remove_outliers function call to view the outliers
# boxplot(df, 'Description_size')






# TODO: Take care at machine-learning phase.
# ############################ Machine Learning ########################
#
# from sklearn.linear_model import LinearRegression
#
# # reg = LinearRegression()
# # reg.fit()
#
# # remove_columns_for_learning(df)
# #
# # X = df.drop('Worthy', axis=1).copy()
# # y = df['Worthy']
# #
# # print(X)
# # print(y)

