import sys
import time
import pandas as pd
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn import svm, tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier

from sklearn.metrics import f1_score, confusion_matrix

# Source for ML algorithms - scikit-learn.org & as learned at Campus IL.


# Display options.
def display_options(maxRows=False):  # Done
    if maxRows:
        pd.set_option('display.max_rows', None)  # Default 60
    pd.set_option('display.max_columns', None)  # Default 0
    pd.set_option('display.width', None)  # Default 80
    pd.set_option('display.max_colwidth', None)  # Default 50


# Remove columns X from df.
def remove_columns_for_learning(df):  # Done
    df.set_index('Name', inplace=True)
    # Number of ratings stays because it can be a measurement of number of purchases, since only people who
    # purchased the product are allowed to rate it.
    colsToRemove = ['Discount', 'Final_rating', '5star', '4star', '3star', '2star', '1star', 'Description',
                    'Publication_month']
    df.drop(columns=colsToRemove, inplace=True)


# Split the dataset into training and target features.
def split_training_target_features(dataframe, target_feature: str):  # Done
    TRAINING_FEATURES = dataframe.columns[dataframe.columns != target_feature]
    TARGET_FEATURE = target_feature
    X = dataframe[TRAINING_FEATURES]
    y = dataframe[TARGET_FEATURE]

    return X, y


# Split the data into train and test datasets.
# Found that best results were given when we split to 70% train, 30% test.
def split_train_test(X, y):  # Done
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    print("\nTarget distribution in original dataset:\n{}".format(y.value_counts()))
    print("\nTarget distribution in the training set:\n{}\n".format(y_train.value_counts()))
    print("Target distribution in the test set:\n{}".format(y_test.value_counts()))

    return X_train, X_test, y_train, y_test


# Gets all the train and test datasets.
# Preforms Logistic-Regression process, and prints the model's accuracy.
def fit_predict_algos(alg: str, X_train, X_test, y_train, y_test, max_depth=0):  # Done
    if alg == 'Logistic Regression':
        clf_model = LogisticRegression(solver='lbfgs', max_iter=2500)
    elif alg == 'SVM':
        clf_model = svm.SVC()
    elif alg == 'KNN':
        clf_model = KNeighborsClassifier(n_neighbors=11)
    elif alg == 'Naive Bayes':
        clf_model = GaussianNB()
    elif alg == 'Decision Tree':
        clf_model = tree.DecisionTreeClassifier()
    elif alg == 'Adaboost':
        clf_model = AdaBoostClassifier(n_estimators=100, random_state=0)
    elif alg == 'Random Forest':
        if max_depth == 0:
            time.sleep(0.5)
            sys.exit('\nmax_depth must be above 0')
        clf_model = RandomForestClassifier(max_depth=max_depth, random_state=0)
    else:
        time.sleep(0.5)
        sys.exit('\n' + str(alg) + " is not a valid algorithm. Insert 'Logistic Regression' / 'SVM' / 'KNN' / "
                                   "'Naive Bayes' / 'Decision Tree' / 'Adaboost' / 'Random Forest'")

    clf_model.fit(X_train, y_train)
    y_pred = clf_model.predict(X_test)

    resDF = pd.DataFrame({"Actual": y_test, "Predicted": y_pred})
    resDF["correct"] = abs((resDF["Actual"] ^ resDF["Predicted"]) - 1)  # XOR - Sets to 1 if only one of two bits is 1

    if alg == 'KNN':
        print('\n' + str(alg) + ', n = 11')
    elif alg == 'Random Forest':
        print('\n' + str(alg) + ', max-depth =', max_depth)
    else:
        print('\n' + str(alg))

    print('Accuracy:', len(resDF[resDF["correct"] == 1]), '/', len(resDF), ' -> ',
          len(resDF[resDF["correct"] == 1]) / len(resDF))
    print('f1-score:', f1_score(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))


# Runs fit_predict_algos function for each one of the classifiers.
def run_all_fit_predict_algos(X_train, X_test, y_train, y_test):  # Done
    fit_predict_algos('Logistic Regression', X_train, X_test, y_train, y_test)
    fit_predict_algos('SVM', X_train, X_test, y_train, y_test)
    fit_predict_algos('KNN', X_train, X_test, y_train, y_test)
    fit_predict_algos('Naive Bayes', X_train, X_test, y_train, y_test)
    fit_predict_algos('Decision Tree', X_train, X_test, y_train, y_test)
    fit_predict_algos('Adaboost', X_train, X_test, y_train, y_test)
    fit_predict_algos('Random Forest', X_train, X_test, y_train, y_test, max_depth=2)
    fit_predict_algos('Random Forest', X_train, X_test, y_train, y_test, max_depth=5)
    # fit_predict_algos(9, X_train, X_test, y_train, y_test)
