

### Final_rating will be the y-value (tagging). probably above/below 4.
### Need to understand how to deal with 'Description'.



# TODO: complete remove-columns function.
# Remove columns X from df.
def remove_columns_for_learning(df):  # not done
    colsToRemove = ['Final_rating', '4star', '3star', '2star', '1star', 'Description']  # '5star'
    df.drop(columns=colsToRemove, inplace=True)



# TODO: Take care at machine-learning phase.
# ############################ Machine Learning ########################
#
# from sklearn.linear_model import LinearRegression
#
# # reg = LinearRegression()
# # reg.fit()
#
# # remove_columns_for_learning(df)
# #
# # X = df.drop('Worthy', axis=1).copy()
# # y = df['Worthy']
# #
# # print(X)
# # print(y)