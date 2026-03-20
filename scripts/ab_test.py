import pandas as pd
from scipy.stats import chi2_contingency

# ── 1. Load data ───────────────────────────────────────────────
df = pd.read_csv('data/campaigns.csv')

# ── 2. Build contingency table ─────────────────────────────────
#    A contingency table counts outcomes for each group
#    Rows = campaign, Columns = responded yes/no

campaign_a = df[df['campaign'] == 'A']['responded']
campaign_b = df[df['campaign'] == 'B']['responded']

responded_a     = campaign_a.sum()
not_responded_a = len(campaign_a) - responded_a
responded_b     = campaign_b.sum()
not_responded_b = len(campaign_b) - responded_b

contingency_table = [
    [responded_a, not_responded_a],
    [responded_b, not_responded_b]
]

print("Contingency Table:")
print(f"Campaign A — Responded: {responded_a}, Did not: {not_responded_a}")
print(f"Campaign B — Responded: {responded_b}, Did not: {not_responded_b}")

# ── 3. Run chi-square test ─────────────────────────────────────
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

print(f"\nChi-Square Statistic : {chi2:.4f}")
print(f"P-Value              : {p_value:.4f}")
print(f"Degrees of Freedom   : {dof}")

# ── 4. Interpret results ───────────────────────────────────────
alpha = 0.05
print(f"\nSignificance Level   : {alpha}")

if p_value < alpha:
    print("\n✅ Result: STATISTICALLY SIGNIFICANT")
    print("We reject the null hypothesis.")
    print("Campaign B has a genuinely higher response rate than Campaign A.")
else:
    print("\n❌ Result: NOT STATISTICALLY SIGNIFICANT")
    print("We fail to reject the null hypothesis.")
    print("The difference could be due to random chance.")

# ── 5. Practical significance ──────────────────────────────────
rate_a = responded_a / len(campaign_a)
rate_b = responded_b / len(campaign_b)
lift   = (rate_b - rate_a) / rate_a * 100

print(f"\nResponse Rate A : {rate_a:.1%}")
print(f"Response Rate B : {rate_b:.1%}")
print(f"Lift            : +{lift:.1f}% improvement with Campaign B")