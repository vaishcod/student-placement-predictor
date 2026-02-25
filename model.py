import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load data
data = pd.read_csv("placement_data.csv")

X = data.drop("Placed", axis=1)
y = data["Placed"]

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Better model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)

def predict_placement(input_data):
    prediction = model.predict([input_data])[0]
    probability = model.predict_proba([input_data])[0][1]
    return prediction, probability, accuracy