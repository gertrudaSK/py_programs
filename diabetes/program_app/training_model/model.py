import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

df = pd.read_csv('diabetes_data.csv')

right_data = df[['Age', 'Gender', 'class']]


def replace_gender(x):
    if x == "Male":
        return 1
    elif x == "Female":
        return 0


right_data['Gender'] = right_data['Gender'].apply(replace_gender)

left_data = df.drop(['Age', 'Gender', 'class'], axis=1)


def replace_data(x):
    if x == "Yes":
        return 1
    elif x == "No":
        return 0


left_data = left_data.applymap(replace_data)

data = right_data.join(left_data)

feature_cols = ['Age', 'Gender', 'Polyuria', 'Polydipsia',
                'sudden weight loss',
                'weakness', 'Polyphagia', 'Genital thrush', 'visual blurring',
                'Itching', 'Irritability', 'delayed healing',
                'partial paresis',
                'muscle stiffness', 'Alopecia', 'Obesity']

X = data[feature_cols]
y = data['class']

X_train, X_test, y_train, y_test = \
    train_test_split(X, y, test_size=0.4, random_state=42)

rfc = RandomForestClassifier(n_estimators=1000).fit(X_train, y_train)

joblib.dump(rfc, "random_forest.joblib")
