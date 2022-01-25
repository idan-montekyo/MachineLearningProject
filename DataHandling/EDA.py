import pandas as pd
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import seaborn as sns
from DataHandling import handle_data
from HandlingFunc import create_new_worthy_column_seperated_by_rating_x


originalDataSet = (pd.read_csv('../DataAcquisition/gamesDataSet.csv'))
df = originalDataSet.copy()
df = handle_data(df, worthyColumn=False)
print('-------------------------- EDA --------------------------\n')
print(df.describe())

print('\nAbove 4.2:', len(df[df['Final_rating'] >= 4.2]),
      ' - Below 4.2:', len(df[df['Final_rating'] < 4.2]) - len(df[df['Final_rating'] == -1]))
print('\nAbove 4.1:', len(df[df['Final_rating'] >= 4.1]),
      ' - Below 4.1:', len(df[df['Final_rating'] < 4.1]) - len(df[df['Final_rating'] == -1]))
print('\nAbove 4:', len(df[df['Final_rating'] >= 4]),
      ' - Below 4:', len(df[df['Final_rating'] < 4]) - len(df[df['Final_rating'] == -1]))
print('\nAbove 3.5:', len(df[df['Final_rating'] >= 3.5]),
      ' - Below 3.5:', len(df[df['Final_rating'] < 3.5]) - len(df[df['Final_rating'] == -1]))


df_final_rating_cut_at_35 = (create_new_worthy_column_seperated_by_rating_x(df, 3.5))['Worthy']
df_final_rating_cut_at_4 = (create_new_worthy_column_seperated_by_rating_x(df, 4))['Worthy']
df_final_rating_cut_at_41 = (create_new_worthy_column_seperated_by_rating_x(df, 4.1))['Worthy']
df_final_rating_cut_at_42 = (create_new_worthy_column_seperated_by_rating_x(df, 4.2))['Worthy']


# Pie Charts for 'Worthy' column, for either case 'Final_rating' is cut at 3.5 / 4 / 4.1 / 4.2
# Worthy distribution represented by percentage.
mylabels = [1, 0]
PieChartFigure = plt.figure('Pie Charts', facecolor='black', figsize=(6, 4.5))
plt.subplot(221)
plt.title('Final_rating cut at 3.5', loc='center', color='white')
df_final_rating_cut_at_35.value_counts().plot(kind='pie', autopct='%.2f', colors=['crimson', 'lightcoral'],
                                              startangle=-60, textprops=dict(color='w'))
plt.subplot(222)
plt.title('Final_rating cut at 4', loc='center', color='white')
df_final_rating_cut_at_4.value_counts().plot(kind='pie', autopct='%.2f', colors=['crimson', 'lightcoral'],
                                             startangle=-6.5, textprops=dict(color='w'))
plt.subplot(223)
plt.title('Final_rating cut at 4.1', loc='center', color='white')
df_final_rating_cut_at_41.value_counts().plot(kind='pie', autopct='%.2f', colors=['lightcoral', 'crimson'],
                                              startangle=172.5, textprops=dict(color='w'))
plt.subplot(224)
plt.title('Final_rating cut at 4.2', loc='center', color='white')
df_final_rating_cut_at_42.value_counts().plot(kind='pie', autopct='%.2f', colors=['lightcoral', 'crimson'],
                                              startangle=162.5, textprops=dict(color='w'))
plt.show()



# TODO: Check if needed. If yes, need to choose 5-7 main columns to run on. (binDf is redundant)
# ############################ Scatter Matrix ########################
#
# binDf = df[df['Worthy'] > -1]
#
# plt.scatter(binDf['Worthy'], binDf['Description_size'])
# plt.show()
#
# scatter = binDf.drop(['Description', '5star', '4star', '3star', '2star', '1star', 'Final_rating',
#                       'Sub_operating_system', 'Sub-Genre', 'Publication_day', 'Publication_year'], axis=1)
# pd.plotting.scatter_matrix(scatter)
# plt.show()