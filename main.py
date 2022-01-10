import pandas as pd
import pandas as ps
import time
from AmazonPageScraping import scrape_single_game

### DISPLAY OPTIONS
# pd.set_option('display.max_rows', None)  # Default 60
pd.set_option('display.max_columns', None)  # Default 0
pd.set_option('display.width', None)  # Default 80
pd.set_option('display.max_colwidth', None)  # Default 50


def get_all_games():
    allGameUrlsDf = pd.read_csv('completeGameUrlList.csv')
    gamesDfColumn0 = allGameUrlsDf.iloc[:, 0]
    gamesDfColumn1 = allGameUrlsDf.iloc[:, 1]
    gamesDfColumn2 = allGameUrlsDf.iloc[:, 2]
    gamesDfColumn3 = allGameUrlsDf.iloc[:, 3]
    gamesDfColumn4 = allGameUrlsDf.iloc[:, 4]
    gamesDfColumn5 = allGameUrlsDf.iloc[:, 5]
    gamesDfColumn6 = allGameUrlsDf.iloc[:, 6]
    gamesDfColumn7 = allGameUrlsDf.iloc[:, 7]
    # for i, game in enumerate(gamesDfColumn7):
    #     if str(game) != 'nan':
    #         print(i, game, '\n')

    return [gamesDfColumn0, gamesDfColumn1, gamesDfColumn2, gamesDfColumn3,
            gamesDfColumn4, gamesDfColumn5, gamesDfColumn6, gamesDfColumn7]

allGamesList = get_all_games()


### Lists (columns of the Data-Frame)
name = []
price = []
discount = []
final_rating = []
number_of_ratings = []
number_of_5star = []
number_of_4star = []
number_of_3star = []
number_of_2star = []
number_of_1star = []
brand = []
genre = []
sub_genre = []
publication_day = []
publication_month = []
publication_year = []
operating_system = []
sub_operating_system = []
format = []
platform = []
other = []
product_description = []


urls = allGamesList[0].iloc[:10]
rejectedGamesList = []
for index, url in enumerate(urls):
    # if index > 0:
    print('\n------------------------------------', index, '------------------------------------\n')
    scrape_single_game(url, rejectedGamesList,
                       name, price, discount, final_rating, number_of_ratings,
                       number_of_5star, number_of_4star, number_of_3star, number_of_2star, number_of_1star,
                       brand, genre, sub_genre, publication_day, publication_month, publication_year,
                       operating_system, sub_operating_system, format, platform, other, product_description)

print(len(name))
print(len(product_description))
print()
print('Rejected games list:')
for rej in rejectedGamesList:
    print(rej)

### Final_rating will be the y-value (tagging). probably above/below 3.5.
### Amount of stars will probably not be part of the learning.
### Need to understand how to deal with 'Description'.
### Other_features might be redundant.
df = pd.DataFrame({'Name': name,
                   'Price': price,
                   'Discount': discount,
                   'Final_rating': final_rating,
                   'Number_of_ratings': number_of_ratings,
                   '5star': number_of_5star,
                   '4star': number_of_4star,
                   '3star': number_of_3star,
                   '2star': number_of_2star,
                   '1star': number_of_1star,
                   'Brand': brand,
                   'Genre': genre,
                   'Sub-Genre': sub_genre,
                   'Publication_day': publication_day,
                   'Publication_month': publication_month,
                   'Publication_year': publication_year,
                   'Operating_system': operating_system,
                   'Sub_operating_system': sub_operating_system,
                   'Format': format,
                   'Platform': platform,
                   'Other_features': other,
                   'Description': product_description})

print(df)