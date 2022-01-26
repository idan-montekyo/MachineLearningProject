import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from HandlingFunc import handle_data, create_new_worthy_column_separated_by_rating_x, boxplot
from scipy.stats import chi2_contingency
from colorama import Fore, Style


originalDataSet = pd.read_csv('../DataAcquisition/gamesDataSet.csv')
df = originalDataSet.copy()
df = handle_data(df, prices_fix_or_remove='fix', worthyColumn=True)
print('-------------------------- EDA --------------------------\n')
print(df.describe())

# Amount of games for either value 1 or 0 of 'Worthy' column.
print('\nAbove 4:', len(df[df['Final_rating'] >= 4]),
      ' - Below 4:', len(df[df['Final_rating'] < 4]) - len(df[df['Final_rating'] == -1]))


# Boxplot visualization to detect outlier values.
boxplot(df, 'Price')
boxplotFigure = plt.figure('BoxPlot visualization', facecolor='white', figsize=(9, 4.5))
plt.subplot(221), plt.title('Description_size - Original')
plt.boxplot(originalDataSet['Description_size']), plt.xticks([])
plt.subplot(222), plt.title('Description_size - After outliers removed')
plt.boxplot(df['Description_size']), plt.xticks([])
plt.subplot(223), plt.title('Number_of_ratings - Original')
plt.boxplot(originalDataSet['Number_of_ratings']), plt.xticks([])
plt.subplot(224), plt.title('Number_of_ratings - After outliers removed')
plt.boxplot(df['Number_of_ratings']), plt.xticks([])
plt.show()


# Pie Charts for 'Worthy' column, for either case 'Final_rating' is cut at 3.5 / 4 / 4.1 / 4.2
df_final_rating_cut_at_35 = (create_new_worthy_column_separated_by_rating_x(df, 3.5))['Worthy']
df_final_rating_cut_at_4 = (create_new_worthy_column_separated_by_rating_x(df, 4))['Worthy']
df_final_rating_cut_at_41 = (create_new_worthy_column_separated_by_rating_x(df, 4.1))['Worthy']
df_final_rating_cut_at_42 = (create_new_worthy_column_separated_by_rating_x(df, 4.2))['Worthy']

# (Pie Charts) Worthy distribution represented by percentage.
pieChartFigure = plt.figure('Pie Charts', facecolor='black', figsize=(6, 4.5))
plt.subplot(221), plt.title('Final_rating cut at 3.5', loc='center', color='white')
df_final_rating_cut_at_35.value_counts().plot(kind='pie', autopct='%.2f', colors=['crimson', 'lightcoral'],
                                              startangle=-60, textprops=dict(color='w'))
plt.subplot(222), plt.title('Final_rating cut at 4', loc='center', color='white')
df_final_rating_cut_at_4.value_counts().plot(kind='pie', autopct='%.2f', colors=['crimson', 'lightcoral'],
                                             startangle=-6.5, textprops=dict(color='w'))
plt.subplot(223), plt.title('Final_rating cut at 4.1', loc='center', color='white')
df_final_rating_cut_at_41.value_counts().plot(kind='pie', autopct='%.2f', colors=['lightcoral', 'crimson'],
                                              startangle=172.5, textprops=dict(color='w'))
plt.subplot(224), plt.title('Final_rating cut at 4.2', loc='center', color='white')
df_final_rating_cut_at_42.value_counts().plot(kind='pie', autopct='%.2f', colors=['lightcoral', 'crimson'],
                                              startangle=162.5, textprops=dict(color='w'))
plt.show()


# Cross-Tabulation line-plots to check dependencies for several features.
ct_month = pd.crosstab(df['Publication_month'], df['Worthy'], normalize='index')
ct_year = pd.crosstab(df[df['Publication_year'] > 0]['Publication_year'],
                      df[df['Publication_year'] > 0]['Worthy'], normalize='index')
ct_other_features = pd.crosstab(df['Other_features'], df['Worthy'], normalize='index')
ct_description_bullets = pd.crosstab(df['Description_bullets_num'], df['Worthy'], normalize='index')

# Source-subplots: https://stackoverflow.com/questions/50863575/pandas-bar-plot-using-subplots
# Source-legend: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.legend.html
# Source-title: https://stackoverflow.com/questions/25239933/how-to-add-title-to-subplots-in-matplotlib
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(9, 4))
ct_month.plot(ax=axes[0][0], kind='line', color=['pink', 'red'])
axes[0][0].title.set_text('Publication_month')
ct_year.plot(ax=axes[0][1], kind='line', color=['pink', 'red'])
axes[0][1].title.set_text('Publication_year')
axes[0][1].legend(title='Worthy', loc=1)
ct_other_features.plot(ax=axes[1][0], kind='line', color=['pink', 'red'])
axes[1][0].legend(title='Worthy', loc=1)
ct_description_bullets.plot(ax=axes[1][1], kind='line', color=['pink', 'red'])
axes[1][1].legend(title='Worthy', loc=1)
plt.show()


# Scatter plot representation of the connection between 'Worthy' value and other features.
scatterPlotFigure = plt.figure('Scatter Plots', facecolor='white', figsize=(9, 4.5))
plt.subplot(231), plt.title('5star')
plt.scatter(df['Worthy'], df['5star'], s=15, color='red', alpha=0.3), plt.xticks([0, 1])
plt.subplot(232), plt.title('Price')
plt.scatter(df['Worthy'], df['Price'], s=15, color='red', alpha=0.3), plt.xticks([0, 1])
plt.subplot(233), plt.title('Brand')
plt.scatter(df['Worthy'], df['Brand'], s=15, color='red', alpha=0.3), plt.xticks([0, 1])
plt.subplot(234), plt.title('1star')
plt.scatter(df['Worthy'], df['1star'], s=15, color='red', alpha=0.3), plt.xticks([0, 1])
plt.subplot(235), plt.title('Discount')
plt.scatter(df['Worthy'], df['Discount'], s=15, color='red', alpha=0.3), plt.xticks([0, 1])
plt.subplot(236), plt.title('Genre')
plt.scatter(df['Worthy'], df['Genre'], s=15, color='red', alpha=0.3), plt.xticks([0, 1])
plt.show()


# PairPlot visualization.
# Source: https://seaborn.pydata.org/generated/seaborn.pairplot.html
ppDf = df[df['Publication_year'] > 0].copy()
colReplacingDict = dict({'Number_of_ratings': 'Num_of_ratings', 'Publication_year': 'Year', 'Other_features': 'Other'})
ppDf.rename(columns=colReplacingDict, inplace=True)
pairplotCols = ['Worthy', 'Price', 'Num_of_ratings', 'Year', 'Other']
pairplotFigure = sns.pairplot(ppDf[pairplotCols], hue='Worthy')
pairplotFigure.fig.set_figwidth(9)
pairplotFigure.fig.set_figheight(4.5)
plt.show()


# Chi-square tests:
# Cross-Tabulation - this time, not normalized.
ct_price = pd.crosstab(df['Price'], df['Worthy'])
ct_discount = pd.crosstab(df['Discount'], df['Worthy'])
ct_final_rating = pd.crosstab(df['Final_rating'], df['Worthy'])
ct_num_of_ratings = pd.crosstab(df['Number_of_ratings'], df['Worthy'])
ct_5star = pd.crosstab(df['5star'], df['Worthy'])
ct_1star = pd.crosstab(df['1star'], df['Worthy'])
ct_brand = pd.crosstab(df['Brand'], df['Worthy'])
ct_genre = pd.crosstab(df['Genre'], df['Worthy'])
ct_month = pd.crosstab(df['Publication_month'], df['Worthy'])
ct_year = pd.crosstab(df[df['Publication_year'] > 0]['Publication_year'],
                      df[df['Publication_year'] > 0]['Worthy'])
ct_os = pd.crosstab(df['Operating_system'], df['Worthy'])
ct_format = pd.crosstab(df['Format'], df['Worthy'])
ct_platform = pd.crosstab(df['Platform'], df['Worthy'])
ct_other_features = pd.crosstab(df['Other_features'], df['Worthy'])
ct_description_bullets = pd.crosstab(df['Description_bullets_num'], df['Worthy'])

# Source-colored-text: https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
print(f'\n{Fore.BLUE}Chi-Square test for dependency:{Style.RESET_ALL} Test approved if Result < 0.05')
print(f'Dependency in feature - Price:{Fore.RED}', (chi2_contingency(ct_price)[1] < 0.05),
      f'{Style.RESET_ALL}->', chi2_contingency(ct_price)[1])
print(f'Dependency in feature - Discount:{Fore.RED}', (chi2_contingency(ct_discount)[1] < 0.05),
      f'{Style.RESET_ALL}->', chi2_contingency(ct_discount)[1])
print(f'Dependency in feature - Final-rating:{Fore.GREEN}', (chi2_contingency(ct_final_rating)[1] < 0.05),
      f'{Style.RESET_ALL}->', chi2_contingency(ct_final_rating)[1], '(Obviously...)')
print(f'Dependency in feature - Number-of-ratings:{Fore.GREEN}', (chi2_contingency(ct_num_of_ratings)[1] < 0.05),
      f'{Style.RESET_ALL}->', chi2_contingency(ct_num_of_ratings)[1])
print(f'Dependency in feature - 5-star:{Fore.GREEN}', (chi2_contingency(ct_5star)[1] < 0.05),
      f'{Style.RESET_ALL}->', chi2_contingency(ct_5star)[1])
print(f'Dependency in feature - 1-star:{Fore.GREEN}', (chi2_contingency(ct_1star)[1] < 0.05),
      f'{Style.RESET_ALL}->', chi2_contingency(ct_1star)[1])
print(f'Dependency in feature - Brand:{Fore.GREEN}', (chi2_contingency(ct_brand)[1] < 0.05),
      f'{Style.RESET_ALL}->', chi2_contingency(ct_brand)[1])
print(f'Dependency in feature - Genre:{Fore.GREEN}', (chi2_contingency(ct_genre)[1] < 0.05),
      f'{Style.RESET_ALL}->', chi2_contingency(ct_genre)[1])
print(f'Dependency in feature - Month:{Fore.GREEN}', (chi2_contingency(ct_month)[1] < 0.05),
      f'{Style.RESET_ALL}->', chi2_contingency(ct_month)[1])
print(f'Dependency in feature - Year:{Fore.GREEN}', (chi2_contingency(ct_year)[1] < 0.05),
      f'{Style.RESET_ALL}->', chi2_contingency(ct_year)[1])
print(f'Dependency in feature - Operating-system:{Fore.GREEN}', (chi2_contingency(ct_os)[1] < 0.05),
      f'{Style.RESET_ALL}->', chi2_contingency(ct_os)[1])
print(f'Dependency in feature - Format:{Fore.GREEN}', (chi2_contingency(ct_format)[1] < 0.05),
      f'{Style.RESET_ALL}->', chi2_contingency(ct_format)[1])
print(f'Dependency in feature - Platform:{Fore.GREEN}', (chi2_contingency(ct_platform)[1] < 0.05),
      f'{Style.RESET_ALL}->', chi2_contingency(ct_platform)[1])
print(f'Dependency in feature - Other-features:{Fore.GREEN}', (chi2_contingency(ct_other_features)[1] < 0.05),
      f'{Style.RESET_ALL}->', chi2_contingency(ct_other_features)[1])
print(f'Dependency in feature - Description-bullets:{Fore.GREEN}', (chi2_contingency(ct_description_bullets)[1] < 0.05),
      f'{Style.RESET_ALL}->', chi2_contingency(ct_description_bullets)[1])
