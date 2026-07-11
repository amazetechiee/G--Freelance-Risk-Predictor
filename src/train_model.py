import os, pickle, pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def run_train():
    df = pd.read_csv("data/cleaned_data.csv")

    # Replicate engineered features exactly
    df["daily_burn_rate"] = df["total_budget_inr"] / df["duration_days"]
    expected_market_rate = df["duration_days"] * (500 + (df["developer_experience_years"] * 400))
    df["financial_buffer_ratio"] = df["total_budget_inr"] / expected_market_rate
    df["experience_density"] = df["developer_experience_years"] / df["duration_days"]

    feature_cols = ["developer_experience_years", "duration_days", "total_budget_inr", "daily_burn_rate", "financial_buffer_ratio", "experience_density"]
    X = df[feature_cols]
    y = df["delivery_risk_label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=150, max_depth=10, random_state=42, class_weight="balanced")
    model.fit(X_train, y_train)

    os.makedirs("models", exist_ok=True)
    with open("models/model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("✅ Advanced Model trained via script execution.")

if __name__ == '__main__':
    run_train()