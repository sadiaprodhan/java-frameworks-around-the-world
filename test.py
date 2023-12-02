import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Create a DataFrame with the provided data
data = pd.DataFrame({
    'Framework': ['Spring', 'JSF'],
    'Frameworks_in_Asia': [11, 4 ],
    'StackOverflow_Questions_of_Asia': [30, 14 ]
})

# Calculate the correlation coefficient
correlation = data['Frameworks_in_Asia'].corr(data['StackOverflow_Questions_of_Asia'])

# Perform the linear regression analysis
X = data['Frameworks_in_Asia']
X = sm.add_constant(X)  # Add a constant (intercept) to the model
y = data['StackOverflow_Questions_of_Asia']
model = sm.OLS(y, X).fit()

# Get the regression results
intercept, slope = model.params['const'], model.params['Frameworks_in_Asia']

# Create a scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(data['Frameworks_in_Asia'], data['StackOverflow_Questions_of_Asia'], label='Data Points')
plt.plot(data['Frameworks_in_Asia'], intercept + slope * data['Frameworks_in_Asia'], color='red', label='Regression Line')
plt.xlabel('Frameworks in Asia')
plt.ylabel('StackOverflow Questions of Asia')
plt.title(f'Correlation: {correlation:.2f}')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

# Display regression results
print(model.summary())