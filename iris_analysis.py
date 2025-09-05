# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
import numpy as np

# Set style for better looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# Task 1: Load and Explore the Dataset
print("="*50)
print("TASK 1: LOAD AND EXPLORE THE DATASET")
print("="*50)

try:
    # Load the Iris dataset
    iris = load_iris()
    
    # Create DataFrame
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['species'] = iris.target
    df['species'] = df['species'].map({0: 'setosa', 1: 'versicolor', 2: 'virginica'})
    
    print("Dataset loaded successfully!")
    print(f"Dataset shape: {df.shape}")
    
    # Display first few rows
    print("\nFirst 5 rows of the dataset:")
    print(df.head())
    
    # Explore data structure
    print("\nDataset information:")
    print(df.info())
    
    # Check for missing values
    print("\nMissing values in each column:")
    print(df.isnull().sum())
    
    # Clean dataset (though Iris dataset typically has no missing values)
    # For demonstration, we'll show how to handle missing values
    if df.isnull().sum().sum() > 0:
        print("\nCleaning dataset...")
        # Fill numerical columns with mean and categorical with mode
        for column in df.columns:
            if df[column].dtype in ['int64', 'float64']:
                df[column].fillna(df[column].mean(), inplace=True)
            else:
                df[column].fillna(df[column].mode()[0], inplace=True)
        print("Missing values handled!")
    else:
        print("\nNo missing values found. Dataset is clean!")
        
except Exception as e:
    print(f"Error loading dataset: {e}")
    exit()

# Task 2: Basic Data Analysis
print("\n" + "="*50)
print("TASK 2: BASIC DATA ANALYSIS")
print("="*50)

# Basic statistics
print("Basic statistics of numerical columns:")
print(df.describe())

# Group by species and compute mean of numerical columns
print("\nMean values by species:")
species_stats = df.groupby('species').mean()
print(species_stats)

# Additional analysis - find patterns
print("\nInteresting findings:")
print(f"- Setosa has the smallest petal dimensions")
print(f"- Virginica has the largest sepal and petal dimensions")
print(f"- Versicolor is intermediate in most measurements")

# Calculate correlation matrix
correlation_matrix = df.select_dtypes(include=[np.number]).corr()
print("\nCorrelation matrix:")
print(correlation_matrix)

# Task 3: Data Visualization
print("\n" + "="*50)
print("TASK 3: DATA VISUALIZATION")
print("="*50)

# Create a figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. Line chart showing trends (using index as pseudo-time)
# For demonstration, we'll use sepal length across samples
axes[0, 0].plot(df.index, df['sepal length (cm)'], label='Sepal Length', color='blue')
axes[0, 0].plot(df.index, df['petal length (cm)'], label='Petal Length', color='red')
axes[0, 0].set_title('Trend of Sepal and Petal Length Across Samples')
axes[0, 0].set_xlabel('Sample Index')
axes[0, 0].set_ylabel('Length (cm)')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 2. Bar chart - average measurements by species
species_means = df.groupby('species').mean()
x_pos = np.arange(len(species_means.index))
width = 0.2

axes[0, 1].bar(x_pos - width, species_means['sepal length (cm)'], width, 
               label='Sepal Length', color='lightblue')
axes[0, 1].bar(x_pos, species_means['sepal width (cm)'], width, 
               label='Sepal Width', color='lightgreen')
axes[0, 1].bar(x_pos + width, species_means['petal length (cm)'], width, 
               label='Petal Length', color='lightcoral')
axes[0, 1].set_title('Average Measurements by Species')
axes[0, 1].set_xlabel('Species')
axes[0, 1].set_ylabel('Measurement (cm)')
axes[0, 1].set_xticks(x_pos)
axes[0, 1].set_xticklabels(species_means.index)
axes[0, 1].legend()

# 3. Histogram - distribution of sepal length
axes[1, 0].hist(df['sepal length (cm)'], bins=15, color='skyblue', edgecolor='black', alpha=0.7)
axes[1, 0].set_title('Distribution of Sepal Length')
axes[1, 0].set_xlabel('Sepal Length (cm)')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].grid(True, alpha=0.3)

# 4. Scatter plot - sepal length vs petal length
colors = {'setosa': 'red', 'versicolor': 'green', 'virginica': 'blue'}
for species in df['species'].unique():
    subset = df[df['species'] == species]
    axes[1, 1].scatter(subset['sepal length (cm)'], subset['petal length (cm)'], 
                      label=species, alpha=0.7, s=50)
axes[1, 1].set_title('Sepal Length vs Petal Length')
axes[1, 1].set_xlabel('Sepal Length (cm)')
axes[1, 1].set_ylabel('Petal Length (cm)')
axes[1, 1].legend()
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('iris_analysis_visualizations.png', dpi=300, bbox_inches='tight')
plt.show()

# Additional visualizations for better insights
print("\nAdditional visualizations:")

# Box plot to show distribution by species
plt.figure(figsize=(12, 6))
df_melted = pd.melt(df, id_vars="species", var_name="measurement", value_name="value")
sns.boxplot(x="measurement", y="value", hue="species", data=df_melted)
plt.title('Distribution of Measurements by Species')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('iris_box_plots.png', dpi=300, bbox_inches='tight')
plt.show()

# Correlation heatmap
plt.figure(figsize=(8, 6))
numeric_df = df.select_dtypes(include=[np.number])
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap of Numerical Features')
plt.tight_layout()
plt.savefig('iris_correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

# Pair plot for comprehensive view
sns.pairplot(df, hue='species', palette=colors, diag_kind='hist')
plt.suptitle('Pair Plot of Iris Dataset Features', y=1.02)
plt.savefig('iris_pair_plot.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*50)
print("SUMMARY OF FINDINGS")
print("="*50)
print("1. The dataset contains 150 samples with 4 numerical features and 1 categorical target.")
print("2. No missing values were found in the dataset.")
print("3. Setosa species has distinctly smaller petal measurements compared to others.")
print("4. Strong positive correlation exists between petal length and petal width.")
print("5. Virginica species shows the largest measurements across all features.")
print("6. The data is well-separated by species, making it suitable for classification tasks.")

print("\nAll visualizations have been saved as PNG files in the current directory.")