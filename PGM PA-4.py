import pandas as pd

# Define the joint distribution as a DataFrame
data = {
    'A': ['T', 'T', 'T', 'T', 'T', 'T', 'T', 'T', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F'],
    'B': ['T', 'T', 'T', 'T', 'F', 'F', 'F', 'F', 'T', 'T', 'T', 'T', 'F', 'F', 'F', 'F'],
    'C': ['T', 'T', 'F', 'F', 'T', 'T', 'F', 'F', 'T', 'T', 'F', 'F', 'T', 'T', 'F', 'F'],
    'D': ['T', 'F', 'T', 'F', 'T', 'F', 'T', 'F', 'T', 'F', 'T', 'F', 'T', 'F', 'T', 'F'],
    'P(A,B,C,D)': [0.0448, 0.0252, 0.0112, 0.0588, 0.0144, 0.0144, 0.0096, 0.0216,
                   0.1024, 0.0576, 0.0256, 0.1344, 0.1152, 0.1152, 0.0768, 0.1728]
}

df = pd.DataFrame(data)

# Calculate marginal probabilities
marginal_probs = {
    'A': df.groupby('A')['P(A,B,C,D)'].sum(),
    'B': df.groupby('B')['P(A,B,C,D)'].sum(),
    'C': df.groupby('C')['P(A,B,C,D)'].sum(),
    'D': df.groupby('D')['P(A,B,C,D)'].sum(),
}

# Calculate conditional probabilities
conditional_probs = {
    'A|B': df.groupby(['A', 'B'])['P(A,B,C,D)'].sum() / marginal_probs['B'],
    'C|B': df.groupby(['C', 'B'])['P(A,B,C,D)'].sum() / marginal_probs['B'],
    'A|C': df.groupby(['A', 'C'])['P(A,B,C,D)'].sum() / marginal_probs['C'],
    'D|C': df.groupby(['D', 'C'])['P(A,B,C,D)'].sum() / marginal_probs['C'],
}

# Check for independence
independence_tests = {
    'A&B': (marginal_probs['A'] * marginal_probs['B']).sum() == (df['P(A,B,C,D)'][(df['A'] == 'T') & (df['B'] == 'T')].sum() + df['P(A,B,C,D)'][(df['A'] == 'F') & (df['B'] == 'F')].sum()),
    'A&C': (marginal_probs['A'] * marginal_probs['C']).sum() == (df['P(A,B,C,D)'][(df['A'] == 'T') & (df['C'] == 'T')].sum() + df['P(A,B,C,D)'][(df['A'] == 'F') & (df['C'] == 'F')].sum()),
    'A&C|B': ((conditional_probs['A|B'] * marginal_probs['B']).sum() == (marginal_probs['A'] * marginal_probs['C']).sum()),
    'A&D': (marginal_probs['A'] * marginal_probs['D']).sum() == (df['P(A,B,C,D)'][(df['A'] == 'T') & (df['D'] == 'T')].sum() + df['P(A,B,C,D)'][(df['A'] == 'F') & (df['D'] == 'F')].sum()),
    'A&D|C': ((conditional_probs['A|C'] * marginal_probs['C']).sum() == (marginal_probs['A'] * marginal_probs['D']).sum())
}

# Print results
print("Independence tests:")
for key, value in independence_tests.items():
    print(f"{key}: {'Yes' if value else 'No'}")
