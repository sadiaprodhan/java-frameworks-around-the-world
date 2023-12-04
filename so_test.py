import pandas as pd
import matplotlib.pyplot as plt

# Sample data for framework usage in continents
framework_usage_data = {
    'Continent': ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America'],
    'Framework_1': [20, 50, 45, 60, 15, 5],  # Replace with actual framework usage data
    'Framework_2': [15, 40, 35, 50, 10, 3],  # Replace with actual framework usage data
    'Framework_3': [10, 30, 25, 40, 5, 2]  # Replace with actual framework usage data
}

# Sample data for Stack Overflow activity in continents
stackoverflow_activity_data = {
    'Continent': ['Africa', 'Asia', 'Europe', 'North America', 'Oceania', 'South America'],
    'Framework_1_SO': [200, 600, 550, 700, 150, 50],  # Replace with actual SO activity data
    'Framework_2_SO': [150, 500, 450, 600, 100, 30],  # Replace with actual SO activity data
    'Framework_3_SO': [100, 300, 250, 400, 50, 20]  # Replace with actual SO activity data
}

# Convert the data to DataFrames
framework_df = pd.DataFrame(framework_usage_data)
stackoverflow_df = pd.DataFrame(stackoverflow_activity_data)

# Normalize the data to calculate proportions
normalized_framework_df = framework_df.set_index('Continent').div(framework_df.set_index('Continent').sum(axis=1), axis=0)
normalized_stackoverflow_df = stackoverflow_df.set_index('Continent').div(stackoverflow_df.set_index('Continent').sum(axis=1), axis=0)

# Plotting the comparison
fig, axs = plt.subplots(2, 3, figsize=(15, 10))

for i, col in enumerate(normalized_framework_df.columns):
    axs[0, i].bar(normalized_framework_df.index, normalized_framework_df[col], alpha=0.7, label=f'Framework {i+1} Usage')
    axs[0, i].set_title(f'Proportional Framework {i+1} Usage')

for i, col in enumerate(normalized_stackoverflow_df.columns):
    axs[1, i].bar(normalized_stackoverflow_df.index, normalized_stackoverflow_df[col], alpha=0.7, color='orange', label=f'Framework {i+1} SO Activity')
    axs[1, i].set_title(f'Proportional Framework {i+1} SO Activity')

for ax in axs.flat:
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.legend()

plt.tight_layout()
plt.show()