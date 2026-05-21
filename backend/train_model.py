import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

def train_model():
    data_path = 'backend/synthetic_placement_data.csv'
    if not os.path.exists(data_path):
        print("Data file not found!")
        return

    df = pd.read_csv(data_path)
    
    X = df.drop('Placed', axis=1)
    y = df['Placed']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Using RandomForest for better robustness
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    with open('backend/placement_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("Model saved to backend/placement_model.pkl")

if __name__ == "__main__":
    train_model()
