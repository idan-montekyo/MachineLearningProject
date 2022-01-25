import pandas as pd
from AmazonPageScraping import scrape_loop_200_games_from_col_x_quarter_y, get_source_code_from_selenium

### DISPLAY OPTIONS
# pd.set_option('display.max_rows', None)  # Default 60
pd.set_option('display.max_columns', None)  # Default 0
pd.set_option('display.width', None)  # Default 80
pd.set_option('display.max_colwidth', None)  # Default 50

### Final_rating will be the y-value (tagging). probably above/below 4.
### Need to understand how to deal with 'Description'.


### Gets a boolean value. If True, saves full DataSet as a Csv file.
### Concatenates all 8 parts of the data, and returns the complete Games-DataSet.
def get_full_games_data_set(saveAsCsv=False):
    games0 = pd.read_csv('incompleteDatasets/dataset_0.csv')
    games1 = pd.read_csv('incompleteDatasets/dataset_1.csv')
    games2 = pd.read_csv('incompleteDatasets/dataset_2.csv')
    games3 = pd.read_csv('incompleteDatasets/dataset_3.csv')
    games4 = pd.read_csv('incompleteDatasets/dataset_4.csv')
    games5 = pd.read_csv('incompleteDatasets/dataset_5.csv')
    games6 = pd.read_csv('incompleteDatasets/dataset_6.csv')
    games7 = pd.read_csv('incompleteDatasets/dataset_7.csv')

    gamesDataSet = pd.concat([games0, games1, games2, games3, games4, games5, games6, games7])

    if saveAsCsv:
        gamesDataSet.to_csv('gamesDataSet.csv', index=False)
        print('Data set saved successfully.')

    return gamesDataSet


# scrape_loop_200_games_from_col_x_quarter_y(x_from_0_to_7, y_from_1_to_4)

# gamesDataSet = get_full_games_data_set(False)
gamesDataSet = pd.read_csv('gamesDataSet.csv')
