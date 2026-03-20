import pandas as pd
import numpy as np

np.random.seed(42)
n = 1000

data = pd.DataFrame({
    'candidate_id': range(1, n + 1),
    'campaign': ['A'] * 500 + ['B'] * 500,
    'email_opened': (
        list(np.random.binomial(1, 0.45, 500)) +
        list(np.random.binomial(1, 0.55, 500))
    ),
    'clicked_link': (
        list(np.random.binomial(1, 0.20, 500)) +
        list(np.random.binomial(1, 0.28, 500))
    ),
    'responded': (
        list(np.random.binomial(1, 0.10, 500)) +
        list(np.random.binomial(1, 0.15, 500))
    ),
    'days_to_respond': (
        list(np.random.randint(1, 14, 500)) +
        list(np.random.randint(1, 10, 500))
    )
})

data.to_csv('data/campaigns.csv', index=False)
print("Dataset created! Shape:", data.shape)
print(data.head())