import pandas as pd
import numpy as np
from re import search
import matplotlib.pyplot as plt


# Display options.
def display_options(maxRows=False):
    if maxRows:
        pd.set_option('display.max_rows', None)  # Default 60
    pd.set_option('display.max_columns', None)  # Default 0
    pd.set_option('display.width', None)  # Default 80
    pd.set_option('display.max_colwidth', None)  # Default 50


# Remove all duplicated products, and resetting the indexes.
# Before - 2428, after - 2215, dropped - 213.
def handle_duplicates(df):  # Done
    df.drop_duplicates(keep='first', inplace=True)
    df.index = np.arange(0, len(df))


# Convert object 'month' to int64 (0 means missing).
# Source: https://stackoverflow.com/questions/37625334/python-pandas-convert-month-int-to-month-name
def handle_months(df):  # Done
    monthToInteger = {'0': 0, 'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7,
                      'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    df['Publication_month'] = df['Publication_month'].apply(lambda x: monthToInteger[x])


# Convert 'Other_features' column to a binary column representing if the product has another feature or not.
# Got 73 products with an extra feature (1), and 2355 without (0).
def handle_other_features(df):  # Done
    df.loc[df['Other_features'] == '0', 'Other_features'] = 0
    df.loc[df['Other_features'] != 0, 'Other_features'] = 1
    df['Other_features'] = df['Other_features'].astype('int64')


# Convert 'Format' feature to numeric data.
# Source: https://stackoverflow.com/questions/39275533/select-row-from-a-dataframe-based-on-the-type-of-the-objecti-e-str
def handle_format(df):  # Done
    df.loc[df['Format'] == '0', 'Format'] = 0
    df.loc[df['Format'] == 'CD-ROM', 'Format'] = 1
    df.loc[df['Format'] == 'DVD-ROM', 'Format'] = 2
    df.loc[df['Format'] == 'CD', 'Format'] = 3
    df.loc[np.logical_or(df['Format'] == 'CD-ROM, DVD-ROM', df['Format'] == 'DVD-ROM, CD-ROM'), 'Format'] = 4
    df.loc[df['Format'].apply(lambda x: isinstance(x, str)), 'Format'] = 5
    df['Format'] = df['Format'].astype('int64')


# Convert 'Platform' feature to numeric data.
def handle_platform(df):  # Done
    df['Platform'] = df['Platform'].str.lower()
    df['Platform'].replace({'_': ' ', '-': ' ', ';': ' ', '/': ' ', '&': ' ',
                            ', ': ' ', ' , ': ' ', ';, ': ' ', '  ': ' ', '   ': ' '}, regex=True, inplace=True)
    df.loc[df['Platform'] == '0', 'Platform'] = 0
    df.loc[df['Platform'].str.contains('pc', regex=True, na=False), 'Platform'] = 1
    df.loc[df['Platform'].str.contains('windows', regex=True, na=False), 'Platform'] = 2
    df.loc[df['Platform'].str.contains('mac', regex=True, na=False), 'Platform'] = 3
    df.loc[df['Platform'].str.contains('playstation', regex=True, na=False), 'Platform'] = 4
    df.loc[df['Platform'].str.contains('psp', regex=True, na=False), 'Platform'] = 4
    df.loc[df['Platform'].str.contains('xbox', regex=True, na=False), 'Platform'] = 5
    df.loc[df['Platform'].apply(lambda x: isinstance(x, str)), 'Platform'] = 6
    df['Platform'] = df['Platform'].astype('int64')


# Convert 'Platform' feature to numeric data.
# 0: '0', 1: PC, 2: PC, Mac, 3: PC, Windows, 4: Windows, 5: includes PlayStation,
# 6: includes Xbox, 7: includes Mac, 8: includes PC, 9: other
def handle_platform_second_option_not_in_use(df):  # Done - not in use.
    df['Platform'] = df['Platform'].str.lower()
    df['Platform'].replace({'_': ' ', '-': ' ', ';': ' ', '/': ' ', '&': ' ',
                            ', ': ' ', ' , ': ' ', ';, ': ' ', '  ': ' ', '   ': ' '}, regex=True, inplace=True)

    df.loc[df['Platform'] == '0', 'Platform'] = 0
    df.loc[np.logical_or(df['Platform'] == 'pc', df['Platform'] == 'pc pc'), 'Platform'] = 1
    df.loc[np.logical_or(df['Platform'] == 'pc mac', df['Platform'] == 'mac pc'), 'Platform'] = 2
    df.loc[np.logical_or(df['Platform'] == 'pcmac', df['Platform'] == 'pc mac mac'), 'Platform'] = 2
    df.loc[df['Platform'] == 'pc  mac', 'Platform'] = 2
    df.loc[np.logical_or(df['Platform'] == 'pc windows', df['Platform'] == 'pc windows 7'), 'Platform'] = 3
    df.loc[np.logical_or(df['Platform'] == 'pc windows xp', df['Platform'] == 'pc windows 8'), 'Platform'] = 3
    df.loc[np.logical_or(df['Platform'] == 'windows xp vista pc', df['Platform'] == 'windows pc'), 'Platform'] = 3
    df.loc[np.logical_or(df['Platform'] == 'win xp vista pc win 7', df['Platform'] == 'pc pc windows'), 'Platform'] = 3
    df.loc[np.logical_or(df['Platform'] == 'pc windows vista windows xp windows 8 windows 7 windows 10',
                         df['Platform'] == 'pc windows vista'), 'Platform'] = 3
    df.loc[np.logical_or(df['Platform'] == 'windows', df['Platform'] == 'windows 7'), 'Platform'] = 4
    df.loc[np.logical_or(df['Platform'] == 'windows ', df['Platform'] == 'windows xp 7'), 'Platform'] = 4
    df.loc[np.logical_or(df['Platform'] == 'playstation 4', df['Platform'] == 'playstation 3 pc pc'), 'Platform'] = 5
    df.loc[np.logical_or(df['Platform'] == 'playstation 3', df['Platform'] == '14210711 playstation 3'), 'Platform'] = 5
    df.loc[np.logical_or(df['Platform'] == 'playstation 3 pc windows 98',
                         df['Platform'] == 'playstation 4 ps4 playstation 4'), 'Platform'] = 5
    df.loc[np.logical_or(df['Platform'] == 'pc playstation', df['Platform'] == 'playstation 3 pc mac'), 'Platform'] = 5
    df.loc[np.logical_or(df['Platform'] == 'playstation 3 pc windows 8',
                         df['Platform'] == 'playstation 3 pc windows xp mac'), 'Platform'] = 5
    df.loc[np.logical_or(df['Platform'] == 'playstation 3 pc pc mac',
                         df['Platform'] == 'playstation 3 pc windows 7'), 'Platform'] = 5
    df.loc[np.logical_or(df['Platform'] == 'sony psp playstation portable',
                         df['Platform'] == 'sony psp nintendo switch'), 'Platform'] = 5
    df.loc[np.logical_or(df['Platform'] == 'xbox one', df['Platform'] == 'xbox series x'), 'Platform'] = 6
    df.loc[np.logical_or(df['Platform'] == 'xbox one xbox one', df['Platform'] == 'xbox'), 'Platform'] = 6
    df.loc[np.logical_or(df['Platform'] == 'xbox one xbox 360',
                         df['Platform'] == 'microsoft xbox 360  xbox 360'), 'Platform'] = 6
    df.loc[np.logical_or(df['Platform'] == 'mac', df['Platform'] == 'macintosh pcmac windows'), 'Platform'] = 7
    df.loc[np.logical_or(df['Platform'] == 'windows 7   vista   xp mac os x 10.5+',
                         df['Platform'] == 'pc linux mac'), 'Platform'] = 7
    df.loc[np.logical_or(df['Platform'] == 'unix pc linux mac',
                         df['Platform'] == 'mac intel core duo 1.6ghz pc 1.2ghz or faster'), 'Platform'] = 7
    df.loc[np.logical_or(df['Platform'] == 'unix pc linux', df['Platform'] == 'pc commodore amiga'), 'Platform'] = 8
    df.loc[np.logical_or(df['Platform'] == 'pc electronic games', df['Platform'] == 'pc nintendo wii'), 'Platform'] = 8
    df.loc[np.logical_or(df['Platform'] == 'pc linux', df['Platform'] == 'pc disc'), 'Platform'] = 8
    df.loc[np.logical_or(df['Platform'] == 'pc gamecube', df['Platform'] == 'pc dos'), 'Platform'] = 8
    df.loc[np.logical_or(df['Platform'] == 'pc dvd rom', df['Platform'] == 'sega cd pc'), 'Platform'] = 8
    df.loc[df['Platform'].apply(lambda x: isinstance(x, str)), 'Platform'] = 9
    df['Platform'] = df['Platform'].astype('int64')


# Convert 'Operating_system' feature to numeric data.
def handle_operating_system(df):  # Done
    df.loc[df['Operating_system'] == '0', 'Operating_system'] = 0
    df.loc[df['Operating_system'] == 'Windows Vista', 'Operating_system'] = 1
    df.loc[df['Operating_system'] == 'Windows XP', 'Operating_system'] = 2
    df.loc[df['Operating_system'] == 'Windows ME', 'Operating_system'] = 3
    df.loc[df['Operating_system'] == 'Windows 8', 'Operating_system'] = 4
    df.loc[df['Operating_system'] == 'Windows 10', 'Operating_system'] = 5
    df.loc[df['Operating_system'] == 'Windows 8.1', 'Operating_system'] = 6
    df.loc[df['Operating_system'] == 'Windows', 'Operating_system'] = 7
    df.loc[df['Operating_system'] == 'Windows XP Home Edition', 'Operating_system'] = 8
    df.loc[df['Operating_system'] == 'Windows 7', 'Operating_system'] = 9
    df.loc[df['Operating_system'] == 'Windows NT', 'Operating_system'] = 10
    df.loc[df['Operating_system'] == 'Windows 95', 'Operating_system'] = 11
    df.loc[df['Operating_system'] == 'Mac OS X', 'Operating_system'] = 12
    df.loc[df['Operating_system'] == 'Macintosh', 'Operating_system'] = 13
    df.loc[df['Operating_system'] == 'PC', 'Operating_system'] = 14
    df.loc[df['Operating_system'] == 'Unix', 'Operating_system'] = 15
    df.loc[df['Operating_system'] == 'Playstation_4', 'Operating_system'] = 16
    df.loc[df['Operating_system'].apply(lambda x: isinstance(x, str)), 'Operating_system'] = 17
    df['Operating_system'] = df['Operating_system'].astype('int64')


# Convert 'Sub_operating_system' feature to numeric data.
def handle_sub_operating_system(df):  # Done
    df.loc[df['Sub_operating_system'] == '0', 'Sub_operating_system'] = 0
    df.loc[df['Sub_operating_system'] == ' Windows XP', 'Sub_operating_system'] = 1
    df.loc[df['Sub_operating_system'] == ' Windows Vista', 'Sub_operating_system'] = 2
    df.loc[df['Sub_operating_system'] == ' Windows 7', 'Sub_operating_system'] = 3
    df.loc[df['Sub_operating_system'] == ' Windows 95', 'Sub_operating_system'] = 4
    df.loc[df['Sub_operating_system'] == ' Windows 8', 'Sub_operating_system'] = 5
    df.loc[df['Sub_operating_system'] == ' Windows 2000', 'Sub_operating_system'] = 6
    df.loc[df['Sub_operating_system'] == ' Windows 98', 'Sub_operating_system'] = 7
    df.loc[df['Sub_operating_system'] == ' Windows', 'Sub_operating_system'] = 8
    df.loc[df['Sub_operating_system'] == ' Windows 10', 'Sub_operating_system'] = 9
    df.loc[df['Sub_operating_system'] == ' Windows XP Professional Edition', 'Sub_operating_system'] = 10
    df.loc[df['Sub_operating_system'] == ' Windows ME', 'Sub_operating_system'] = 11
    df.loc[df['Sub_operating_system'] == ' VISTA', 'Sub_operating_system'] = 12
    df.loc[df['Sub_operating_system'] == ' Macintosh', 'Sub_operating_system'] = 13
    df.loc[df['Sub_operating_system'] == ' Mac OS X 10.4 Tiger', 'Sub_operating_system'] = 14
    df.loc[df['Sub_operating_system'].apply(lambda x: isinstance(x, str)), 'Sub_operating_system'] = 15
    df['Sub_operating_system'] = df['Sub_operating_system'].astype('int64')


# Convert 'Genre' feature to numeric data. (Genre can not have value '0').
# Source-replace: https://stackoverflow.com/questions/42331992/replace-part-of-the-string-in-pandas-data-frame
# Source-contains: https://stackoverflow.com/questions/15325182/how-to-filter-rows-in-pandas-by-regex/48884429
# Source-val-name: https://moonbooks.org/Articles/How-to-extract-the-value-names-and-counts-from-valuecounts-in-pandas-/
def handle_genre(df):  # Done
    df['Genre'] = df['Genre'].str.lower()
    df['Genre'].replace({'_': ' ', '-': ' ', ';': ' ', '/': ' ', '&': ' '}, regex=True, inplace=True)

    df.loc[df['Genre'].str.contains('action', regex=True, na=False), 'Genre'] = 1
    df.loc[df['Genre'].str.contains('adventure', regex=True, na=False), 'Genre'] = 2
    df.loc[df['Genre'].str.contains('role', regex=True, na=False), 'Genre'] = 3
    df.loc[df['Genre'].str.contains('strategy', regex=True, na=False), 'Genre'] = 4
    df.loc[df['Genre'].str.contains('puzzle', regex=True, na=False), 'Genre'] = 5
    df.loc[df['Genre'].str.contains('seek and find', regex=True, na=False), 'Genre'] = 6
    df.loc[df['Genre'].str.contains('simulation', regex=True, na=False), 'Genre'] = 7
    df.loc[df['Genre'].str.contains('arcade', regex=True, na=False), 'Genre'] = 8
    df.loc[df['Genre'].str.contains('sports', regex=True, na=False), 'Genre'] = 9
    df.loc[df['Genre'].str.contains('card', regex=True, na=False), 'Genre'] = 10
    df.loc[df['Genre'].str.contains('trivia', regex=True, na=False), 'Genre'] = 11
    df.loc[df['Genre'].str.contains('casino', regex=True, na=False), 'Genre'] = 12
    df.loc[df['Genre'].str.contains('board', regex=True, na=False), 'Genre'] = 13
    df.loc[df['Genre'].str.contains('racing', regex=True, na=False), 'Genre'] = 14
    df.loc[df['Genre'].str.contains('time', regex=True, na=False), 'Genre'] = 15
    df.loc[df['Genre'].str.contains('ball', regex=True, na=False), 'Genre'] = 16
    df.loc[df['Genre'].str.contains('soccer', regex=True, na=False), 'Genre'] = 16
    df.loc[df['Genre'].str.contains('golf', regex=True, na=False), 'Genre'] = 16
    df.loc[df['Genre'].str.contains('hockey', regex=True, na=False), 'Genre'] = 16
    df.loc[df['Genre'].str.contains('child', regex=True, na=False), 'Genre'] = 17
    df.loc[df['Genre'].str.contains('kid', regex=True, na=False), 'Genre'] = 17
    df.loc[df['Genre'].str.contains('war', regex=True, na=False), 'Genre'] = 18
    df.loc[df['Genre'].str.contains('music', regex=True, na=False), 'Genre'] = 19
    df.loc[df['Genre'].apply(lambda x: isinstance(x, str)), 'Genre'] = 20
    df['Genre'] = df['Genre'].astype('int64')
    # index = 1
    # for i,name in enumerate(df['Genre'].value_counts().index.tolist()):
    #     if df['Genre'].value_counts().tolist()[i] >= 5:  # amount of games with the specific genre
    #         df.loc[df['Genre'] == name, 'Genre'] = index
    #         index += 1
    #
    # df.loc[df['Genre'].apply(lambda x: isinstance(x, str)), 'Genre'] = index
    # df['Genre'] = df['Genre'].astype('int64')


# Convert 'Sub-Genre' feature to numeric data.
def handle_sub_genre(df):  # Done
    df['Sub-Genre'] = df['Sub-Genre'].str.lower()
    df['Sub-Genre'].replace({'_': ' ', '-': ' ', ';': ' ', '/': ' ', '&': ' '}, regex=True, inplace=True)

    df.loc[df['Sub-Genre'] == '0', 'Sub-Genre'] = 0
    df.loc[df['Sub-Genre'].str.contains('adventure', regex=True, na=False), 'Sub-Genre'] = 1
    df.loc[df['Sub-Genre'].str.contains('strategy', regex=True, na=False), 'Sub-Genre'] = 2
    df.loc[df['Sub-Genre'].str.contains('shoot', regex=True, na=False), 'Sub-Genre'] = 3
    df.loc[df['Sub-Genre'].str.contains('simulation', regex=True, na=False), 'Sub-Genre'] = 4
    df.loc[df['Sub-Genre'].str.contains('action', regex=True, na=False), 'Sub-Genre'] = 5
    df.loc[df['Sub-Genre'].str.contains('sport', regex=True, na=False), 'Sub-Genre'] = 6
    df.loc[df['Sub-Genre'].str.contains('racing', regex=True, na=False), 'Sub-Genre'] = 7
    df.loc[df['Sub-Genre'].str.contains('role', regex=True, na=False), 'Sub-Genre'] = 8
    df.loc[df['Sub-Genre'].str.contains('puzzle', regex=True, na=False), 'Sub-Genre'] = 9
    df.loc[df['Sub-Genre'].str.contains('hunt', regex=True, na=False), 'Sub-Genre'] = 10
    df.loc[df['Sub-Genre'].str.contains('arcade', regex=True, na=False), 'Sub-Genre'] = 11
    df.loc[df['Sub-Genre'].str.contains('seek', regex=True, na=False), 'Sub-Genre'] = 12
    df.loc[df['Sub-Genre'].str.contains('casino', regex=True, na=False), 'Sub-Genre'] = 13
    df.loc[df['Sub-Genre'].apply(lambda x: isinstance(x, str)), 'Sub-Genre'] = 14
    df['Sub-Genre'] = df['Sub-Genre'].astype('int64')
    # index = 0
    # for i,name in enumerate(df['Sub-Genre'].value_counts().index.tolist()):
    #     if df['Sub-Genre'].value_counts().tolist()[i] >= 3:  # amount of games with the specific sub_genre
    #         df.loc[df['Sub-Genre'] == name, 'Sub-Genre'] = index
    #         index += 1
    #
    # df.loc[df['Sub-Genre'].apply(lambda x: isinstance(x, str)), 'Sub-Genre'] = index
    # df['Sub-Genre'] = df['Sub-Genre'].astype('int64')


# Convert 'Brand' feature to numeric data.
def handle_brand(df):  # Done
    df['Brand'] = df['Brand'].str.lower()
    df['Brand'].replace({'_': ' ', '-': ' ', ';': ' ', '/': ' ', '&': ' '}, regex=True, inplace=True)
    index = 0
    for i,name in enumerate(df['Brand'].value_counts().index.tolist()):
        if df['Brand'].value_counts().tolist()[i] >= 3:  # amount of games with the specific brand
            df.loc[df['Brand'] == name, 'Brand'] = index
            index += 1

    df.loc[df['Brand'].apply(lambda x: isinstance(x, str)), 'Brand'] = index
    df['Brand'] = df['Brand'].astype('int64')


# Create a new binary-column to classify whether the product is worth buying.
# Based on the question if Final-rating value >= or < value of x.
def create_new_worthy_column_seperated_by_rating_x(df, x):  # Done
    df.loc[df['Final_rating'] >= x, 'Worthy'] = 1
    df.loc[df['Final_rating'] < x, 'Worthy'] = 0
    df.loc[df['Final_rating'] == -1, 'Worthy'] = -1
    df['Worthy'] = df['Worthy'].astype('int64')
    cols = df.columns.tolist()
    cols = cols[:3] + cols[-1:] + cols[3:-1]
    rearrangedDf = df[cols]
    return rearrangedDf


# Assign mean value to missing rows - only out of valid rows with full data.
def fix_missing_values_for_price_and_discount(df):  # Done
    noPriceDf = df[df['Price'] == -1].copy()
    noRatingDf = df[df['Final_rating'] == -1].copy()

    indexesToRemove = set(noPriceDf.index.append(noRatingDf.index))
    nonMissingDataDf = df.drop(indexesToRemove, axis=0).copy()

    nonMissingDataDfMeanPrice = nonMissingDataDf['Price'].mean()
    nonMissingDataDfMeanDiscount = nonMissingDataDf['Discount'].mean()

    df.loc[df['Price'] == -1, 'Price'] = nonMissingDataDfMeanPrice
    df.loc[df['Discount'] == -1, 'Discount'] = nonMissingDataDfMeanDiscount


# Remove products with outlier values
def remove_outliers(df):  # Done
    outlierRatings = df[df['Number_of_ratings'] > 50000].copy()
    outlierDescriptionSize = df[df['Description_size'] > 500].copy()

    indexesToRemove = set(outlierRatings.index.append(outlierDescriptionSize.index))
    df.drop(indexesToRemove, axis=0, inplace=True)


# Remove no-rating products.
def remove_products_with_no_rating_and_save_them_to_csv(df, save=False):  # Done
    noRatingDf = df[df['Final_rating'] == -1].copy()

    if save:
        noRatingDf.to_csv('ProductsWithNoRatingDf.csv')

    # indexesToRemove = set(noRatingDf.index)
    # df.drop(indexesToRemove, axis=0, inplace=True)
    return df[df['Final_rating'] > -1]


# TODO: complete remove-columns function.
# Remove columns X from df.
def remove_columns_for_learning(df):  # not done
    colsToRemove = ['Final_rating', '4star', '3star', '2star', '1star', 'Description']  # '5star'
    df.drop(columns=colsToRemove, inplace=True)


# Show boxplot to detect outliers.
def boxplot(df, col=''):  # Done
    if col in df.columns.to_list():
        fig = plt.figure(figsize=(5, 3))
        plt.boxplot(df[col])
        plt.show()
    else:
        print('No such column in this DataFrame.')

