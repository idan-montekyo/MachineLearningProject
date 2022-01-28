from MachineLearningFunc import *

display_options(maxRows=False)

# Reading the reduced dataset we already handled - the one that excludes products without price.
originalReducedDataSet = pd.read_csv('../DataHandling/HandledReducedDataSet.csv')
df = originalReducedDataSet.copy()
remove_columns_for_learning(df)

X, y = split_training_target_features(df, 'Worthy')
X_train, X_test, y_train, y_test = split_train_test(X, y)

# I've tried improving the model by scaling the data (StandardScaler, MinMaxScaler).
# The results were worse, so I decided to move on without scaling.
# Scaling code is deleted for serving no purpose.

# Run the best performance algorithm (Random Forest with max_depth=5) or run all algorithms by calling the second func.
fit_predict_algos('Random Forest', X_train, X_test, y_train, y_test, max_depth=5)
# run_all_fit_predict_algos(X_train, X_test, y_train, y_test)
