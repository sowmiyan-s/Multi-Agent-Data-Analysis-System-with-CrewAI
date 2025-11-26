import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
data = pd.read_csv('data/cleaned_csv.csv')

# Plot 1: Scatter plot
plt.figure(figsize=(10,6))
sns.scatterplot(x='age', y='income', data=data)
plt.title('Scatter Plot of Age vs Income')
plt.xlabel('Age')
plt.ylabel('Income')
plt.show()

# Plot 2: Bar plot
plt.figure(figsize=(10,6))
sns.barplot(x='gender', y='income', data=data)
plt.title('Bar Plot of Gender vs Income')
plt.xlabel('Gender')
plt.ylabel('Income')
plt.show()

# Plot 3: Histogram
plt.figure(figsize=(10,6))
sns.histplot(x='age', data=data, kde=True)
plt.title('Histogram of Age')
plt.xlabel('Age')
plt.ylabel('Count')
plt.show()

# Plot 4: Box plot
plt.figure(figsize=(10,6))
sns.boxplot(x='gender', y='income', data=data)
plt.title('Box Plot of Gender vs Income')
plt.xlabel('Gender')
plt.ylabel('Income')
plt.show()

# Plot 5: Heatmap
plt.figure(figsize=(10,6))
sns.kdeplot(x='age', y='income', data=data, cmap='Blues', shade=True, shade_lowest=False)
plt.title('Heatmap of Age vs Income')
plt.xlabel('Age')
plt.ylabel('Income')
plt.show()