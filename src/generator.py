"""
src/generator.py
Generates raw, anomaly-ridden synthetic contract data to simulate real-world data engineering challenges.
"""


# version 1
import os
import random
import numpy as np
import pandas as pd

def generate_raw_dataset(num_rows=1500, output_path="data/raw_contracts.csv"):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    np.random.seed(42)
    random.seed(42)
    
    data = []
    
    tech_stacks = ["Fullstack web", "frontend REACT", "backend python", "Mobile App", "DevOps", "Data engineering"]
    
    for i in range(num_rows):
        # 1. Features
        experience = int(np.random.exponential(scale=3)) + 1  # 1 to 15+ years
        experience = min(experience, 20)
        
        duration_days = random.randint(10, 180)
        
        # Base budget calculation driven by experience and duration
        base_budget = duration_days * (500 + (experience * 400))
        # Add variance
        budget = int(base_budget * random.uniform(0.6, 1.5))
        
        tech_stack = random.choice(tech_stacks)
        
        # 2. Ground Truth Risk Logic (Deterministic with some noise)
        daily_rate = budget / duration_days
        
        # High risk factors: Underpriced projects, low experience for long durations
        risk_score = 0.0
        if daily_rate < 500:
            risk_score += 0.6
        if experience < 3 and duration_days > 90:
            risk_score += 0.4
        if budget < 15000:
            risk_score += 0.3
            
        risk_score += random.uniform(-0.2, 0.2)
        # Binary target: 1 = High Risk/Failed Delivery, 0 = Safe Track/Passed
        risk_label = 1 if risk_score > 0.45 else 0
        
        # 3. Injecting Synthetic Data Anomalies & Imperfections (Bugs)
        # Anomaly A: Inconsistent/Messy Casing
        if random.random() < 0.3:
            tech_stack = tech_stack.lower()
        elif random.random() < 0.2:
            tech_stack = tech_stack.upper()
            
        # Anomaly B: Out-of-bound / Negative values
        if random.random() < 0.05:
            budget = -budget
        if random.random() < 0.03:
            duration_days = -duration_days
            
        # Anomaly C: Inject NaN Values (Missing Values)
        budget_val = np.nan if random.random() < 0.05 else budget
        duration_val = np.nan if random.random() < 0.04 else duration_days
        experience_val = np.nan if random.random() < 0.03 else experience
        
        data.append({
            "contract_id": f"CON-{1000 + i}",
            "developer_experience_years": experience_val,
            "tech_stack_category": tech_stack,
            "duration_days": duration_val,
            "total_budget_inr": budget_val,
            "delivery_risk_label": risk_label
        })
        
    df = pd.DataFrame(data)
    
    # Anomaly D: Inject explicit row duplicates
    duplicates = df.sample(n=30, random_state=42)
    df = pd.concat([df, duplicates], ignore_index=True)
    shuffled_df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    shuffled_df.to_csv(output_path, index=False)
    print(f"✅ Successfully generated raw dataset with intentional anomalies at: '{output_path}'")
    print(f"📊 Total Shape generated (including duplicates): {shuffled_df.shape}")

if __name__ == "__main__":
    generate_raw_dataset()