import pandas as pd
import numpy as np
from HandlingAFunc import *
# Source: https://stackoverflow.com/questions/24644656/how-to-print-pandas-dataframe-without-index

### DISPLAY OPTIONS
# pd.set_option('display.max_rows', None)  # Default 60
pd.set_option('display.max_columns', None)  # Default 0
pd.set_option('display.width', None)  # Default 80
pd.set_option('display.max_colwidth', None)  # Default 50


### Final_rating will be the y-value (tagging). probably above/below 4.
### Need to understand how to deal with 'Description'.


originalDataSet = (pd.read_csv('../DataAcquisition/gamesDataSet.csv'))
df = originalDataSet.copy()


# # At first, using info() and describe() functions, we can see we have no missing-values, due to the strict
# # assigning at the acquisition stage, where a missing value was instantly assigned the value 0 or -1.
# print(originalDataSet.info())
# print(originalDataSet.describe())
# # The problem is mainly dealing with missing prices (-1) and missing ratings (-1) for products.


######################################## HANDLING-A STARTS HERE #######################################################
handle_duplicates(df)
handle_months(df)
handle_other_features(df)
handle_format(df)
handle_platform(df)
handle_operating_system(df)
handle_sub_operating_system(df)
handle_genre(df)
handle_sub_genre(df)
handle_brand(df)
df = create_new_worthy_column_seperated_by_rating_x(df, 4)
fix_missing_values_for_price_and_discount(df)
df.set_index('Name', inplace=True)


# print(df['Worthy'].value_counts(), '\nSize = ', len(df['Worthy'].value_counts()), '\n\n')


print(df.info())
print('\n\n\n')
print(df.describe())
print('\n\n\n')
print(df)
# for col in df.columns.to_list():
#     print(col)


