import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ── 1. Load the data ──────────────────────────────────────────
df = pd.read_csv('data/campaigns.csv')

# ── 2. Basic overview ─────────────────────────────────────────
print("Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nData types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isnull().sum())

# ── 3. Response rates by campaign ─────────────────────────────
summary = df.groupby('campaign').agg(
    total_candidates=('candidate_id', 'count'),
    open_rate=('email_opened', 'mean'),
    click_rate=('clicked_link', 'mean'),
    response_rate=('responded', 'mean')
).round(3)

print("\nCampaign Summary:")
print(summary)

# ── 4. Visualize response rates ───────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(12, 5))
fig.suptitle('Campaign A vs Campaign B', fontsize=14)

metrics = ['open_rate', 'click_rate', 'response_rate']
titles  = ['Email Open Rate', 'Link Click Rate', 'Response Rate']
colors  = ['#4C72B0', '#DD8452']

for ax, metric, title in zip(axes, metrics, titles):
    ax.bar(summary.index, summary[metric], color=colors)
    ax.set_title(title)
    ax.set_ylabel('Rate')
    ax.set_ylim(0, 1)
    for i, val in enumerate(summary[metric]):
        ax.text(i, val + 0.01, f'{val:.1%}', ha='center', fontsize=11)

plt.tight_layout()
plt.savefig('outputs/campaign_comparison.png')
print("\nChart saved to outputs/campaign_comparison.png")
plt.show()