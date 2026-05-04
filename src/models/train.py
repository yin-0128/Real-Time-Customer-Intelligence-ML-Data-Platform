import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import mlflow
import mlflow.sklearn
import joblib
import os

def generate_mock_data(n_samples=1000):
    np.random.seed(42)
    data = {
        'user_id': range(1, n_samples + 1),
        'days_active': np.random.randint(1, 365, size=n_samples),
        'total_events': np.random.randint(10, 500, size=n_samples),
        'avg_event_value': np.random.uniform(5.0, 200.0, size=n_samples),
        'churn': np.random.choice([0, 1], size=n_samples, p=[0.8, 0.2])
    }
    return pd.DataFrame(data)

def train_model():
    print("Generating mock data for training...")
    df = generate_mock_data()
    
    X = df[['days_active', 'total_events', 'avg_event_value']]
    y = df['churn']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest model...")
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("churn_prediction")
    
    with mlflow.start_run():
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        
        print(f"Model Accuracy: {acc:.4f}")
        print("Classification Report:\n", classification_report(y_test, preds))
        
        mlflow.log_param("n_estimators", 100)
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(model, "model")
        
        # Save model artifact manually as well
        os.makedirs("artifacts", exist_ok=True)
        joblib.dump(model, "artifacts/churn_model.pkl")
        print("Model artifact saved to artifacts/churn_model.pkl")

if __name__ == "__main__":
    train_model()
