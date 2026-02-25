import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

data = pd.read_csv("placement_data.csv")

X = data.drop("Placed", axis=1)
y = data["Placed"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LogisticRegression()
model.fit(X_train, y_train)

def predict_placement(input_data):
    prediction = model.predict([input_data])
    return prediction[0]