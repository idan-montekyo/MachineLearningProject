import pandas as pd


### Prints one link at a time in a different line to the terminal.
def print_list(my_list):
    for i in my_list:
        print(i)
    print("size =", len(my_list))


### List of 50 Amazon page urls, starting from 'startingPage'.
def get_100_pages_from_x1_to_50(startingPage):
    pages = []
    for index in range(startingPage, startingPage + 50):
        page = "https://www.amazon.com/s?k=PC-compatible+Games&i=videogames" + "&page=" + str(index)
        pages.append(page)

    return pages


### Returns DataFrame with all 400 pages (50x8).
def get_pages_1_to_400():
    pages_1_to_50 = get_100_pages_from_x1_to_50(1)
    pages_51_to_100 = get_100_pages_from_x1_to_50(51)
    pages_101_to_150 = get_100_pages_from_x1_to_50(101)
    pages_151_to_200 = get_100_pages_from_x1_to_50(151)
    pages_201_to_250 = get_100_pages_from_x1_to_50(201)
    pages_251_to_300 = get_100_pages_from_x1_to_50(251)
    pages_301_to_350 = get_100_pages_from_x1_to_50(301)
    pages_351_to_400 = get_100_pages_from_x1_to_50(351)

    pages_df = pd.DataFrame({'1_to_50': pages_1_to_50,
                             '51_to_100': pages_51_to_100,
                             '101_to_150': pages_101_to_150,
                             '151_to_200': pages_151_to_200,
                             '201_to_250': pages_201_to_250,
                             '251_to_300': pages_251_to_300,
                             '301_to_350': pages_301_to_350,
                             '351_to_400': pages_351_to_400})
    return pages_df


pages_df = get_pages_1_to_400()
# pages_df.to_csv('400pages_50x8.csv', index=False)


# ### DISPLAY OPTIONS
# # pd.set_option('display.max_rows', None)  # Default 60
# # pd.set_option('display.max_columns', None)  # Default 0
# # pd.set_option('display.width', None)  # Default 80
# pd.set_option('display.max_colwidth', None)  # Default 50
# print(pages_df.iloc[:, 2][45])
