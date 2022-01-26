import pandas as pd
from HandlingFunc import *


display_options(maxRows=False)
originalDataSet = pd.read_csv('../DataAcquisition/gamesDataSet.csv')
df = originalDataSet.copy()

# At first, using info() and describe() functions, we can see we have no missing-values, due to the strict
# assigning at the acquisition stage, where a missing value was instantly assigned the value 0 or -1.
# The problem is mainly dealing with missing prices (-1) and missing ratings (-1) for products.

df = handle_data(df, prices_fix_or_remove='fix')
print(df.describe(include='all'))
print('\n\n\n')

# At the end of the Data-Handling process, we end up with 2046 products -
# - assuming we do not delete products without price.
print(df)
# Saved df with and without no-price products.
# Also saved a dataset of no-price products, and no-rating products.


# handle_data function step by step:
# 1. Remove all duplicated products.
# 2. Convert 'Publication_month' to numbers.
# 3. Convert 'Other_features' to a binary column, by whether there is an extra feature or not.
# 4. Convert all Object-types (string variables) to categories represented as integers.
#    That includes: Format,
#                   Platform,
#                   Operating-System,
#                   Sub-Operating-System,
#                   Genre,
#                   Sub-Genre,
#                   Brand.
# 5. Create a new binary 'Worthy' column, to classify whether or not the product is worth buying.
#    This column is determined by 'Final_rating' value. 4 or above = 1, below 4 = 0.
# 6. Handle missing price. Here we got two options:
#    6.1. In each product with no price, assign the mean value of the products that do contain a price.
#    6.2. Remove all products with no price.
#    - The decision will be made later on, at the Machine-Learning phase, to see which option brings better results.
# 7. Remove outliers.
#    After examining irregular values for certain features, only certain products were removed.
# 8. Remove all products with no ratings.
#    These products will have no use since the model is supposed to predict certain rating range,
#    and we want to verify it later on.
# !! A nice edition to the project might be coming back to the no-rating-products after the project is finished,
#    and try to predict products with no rating given.
# 9. Set 'Name' column as the Data-Frame's index, instead of numbers 0 to DF-length.
