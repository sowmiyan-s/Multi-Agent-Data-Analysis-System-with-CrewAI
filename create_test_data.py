import pandas as pd
import numpy as np

# Create a sample production-like dataset
np.random.seed(42)
n_rows = 100

data = {
    'Date': pd.date_range(start='2023-01-01', periods=n_rows, freq='D'),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], n_rows),
    'Marketing_Spend': np.random.normal(5000, 1000, n_rows),
    'Sales': np.zeros(n_rows),
    'Satisfaction_Score': np.random.uniform(1, 10, n_rows),
    'Product_Category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Beauty'], n_rows)
}

# Add correlation: Sales = 2.5 * Marketing_Spend + random noise
data['Sales'] = 2.5 * data['Marketing_Spend'] + np.random.normal(0, 500, n_rows)

# Add some missing values
data['Satisfaction_Score'][10:15] = np.nan

# Add some outliers
data['Sales'][50] = 50000 # High outlier
data['Sales'][51] = 100    # Low outlier

df = pd.DataFrame(data)
df.to_csv('data/test_production_data.csv', index=False)
print("Sample dataset 'data/test_production_data.csv' created successfully.")
