import pandas as pd
import pandas as ps
import time
from AmazonPageScraping import scrape_loop_200_games_from_col_x_quarter_y

### DISPLAY OPTIONS
# pd.set_option('display.max_rows', None)  # Default 60
pd.set_option('display.max_columns', None)  # Default 0
pd.set_option('display.width', None)  # Default 80
pd.set_option('display.max_colwidth', None)  # Default 50

### Final_rating will be the y-value (tagging). probably above/below 3.5.
### Need to understand how to deal with 'Description'.

scrape_loop_200_games_from_col_x_quarter_y(0, 1)
