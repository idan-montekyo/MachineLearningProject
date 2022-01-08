import pandas as pd
import pandas as ps
import time
from AmazonPageScraping import scrape_single_game

### DISPLAY OPTIONS
# pd.set_option('display.max_rows', None)  # Default 60
pd.set_option('display.max_columns', None)  # Default 0
pd.set_option('display.width', None)  # Default 80
pd.set_option('display.max_colwidth', None)  # Default 50

### headers was Chrome/41.0.2228.0
headers = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

url_no_genre_headphones = 'https://www.amazon.com/Gaming-LVL50-Wired-Stereo-Headset-Console/dp/B07VD8H2SV/ref=' \
                          'sr_1_698?keywords=PC-compatible+Games&qid=1641677746&s=videogames&sr=1-698'
url_game = 'https://www.amazon.com/Madden-22-Standard-Steam-Online/dp/B09CDHZ1DD/ref=sr_1_1?keywords=' \
           'PC-compatible%2BGames&qid=1641063855&s=videogames&sr=1-1&th=1'


# # Check if the function filters non-game-urls. (such as headphones or controllers)
# scrape_single_game(url_game, [], headers)
# scrape_single_game(url_no_genre_headphones, [], headers)


allGameUrlsDf = pd.read_csv('completeGameUrlList.csv')
games7 = allGameUrlsDf.iloc[:, 7]
for i, game in enumerate(games7):
    if str(game) != 'nan':
        print(i, game, '\n')
