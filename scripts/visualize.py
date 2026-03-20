import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# ── 1. Load data ───────────────────────────────────────────────
df = pd.read_csv('data/campaigns.csv')

# ── 2. Summary metrics ─────────────────────────────────────────
summary = df.groupby('campaign').agg(
    open_rate=('email_opened', 'mean'),
    click_rate=('clicked_link', 'mean'),
    response_rate=('responded', 'mean'),
    avg_days=('days_to_respond', 'mean')
).round(3)

# ── 3. Build figure with 4 charts ─────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('A/B Test Results: Email Campaign Analysis', 
             fontsize=16, fontweight='bold', y=1.02)

colors = ['#4C72B0', '#DD8452']
campaigns = summary.index.tolist()

# Chart 1 — Funnel comparison
ax1 = axes[0, 0]
metrics = ['open_rate', 'click_rate', 'response_rate']
labels  = ['Open Rate', 'Click Rate', 'Response Rate']
x = range(len(metrics))
width = 0.35

bars_a = ax1.bar([i - width/2 for i in x], 
                  [summary.loc['A', m] for m in metrics], 
                  width, label='Campaign A', color=colors[0])
bars_b = ax1.bar([i + width/2 for i in x], 
                  [summary.loc['B', m] for m in metrics], 
                  width, label='Campaign B', color=colors[1])

ax1.set_title('Funnel Metrics: A vs B', fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(labels)
ax1.set_ylabel('Rate')
ax1.set_ylim(0, 0.8)
ax1.legend()

for bar in bars_a:
    ax1.text(bar.get_x() + bar.get_width()/2, 
             bar.get_height() + 0.01,
             f'{bar.get_height():.1%}', 
             ha='center', fontsize=9)
for bar in bars_b:
    ax1.text(bar.get_x() + bar.get_width()/2, 
             bar.get_height() + 0.01,
             f'{bar.get_height():.1%}', 
             ha='center', fontsize=9)

# Chart 2 — Response rate with significance
ax2 = axes[0, 1]
bars = ax2.bar(campaigns, summary['response_rate'], 
               color=colors, width=0.4)
ax2.set_title('Response Rate (p=0.0157 ✅)', fontweight='bold')
ax2.set_ylabel('Response Rate')
ax2.set_ylim(0, 0.25)
for bar in bars:
    ax2.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 0.005,
             f'{bar.get_height():.1%}',
             ha='center', fontsize=11, fontweight='bold')
ax2.axhline(y=0.096, color='gray', linestyle='--', 
            linewidth=1, label='Campaign A baseline')
ax2.legend()

# Chart 3 — Days to respond distribution
ax3 = axes[1, 0]
df_a = df[df['campaign'] == 'A']['days_to_respond']
df_b = df[df['campaign'] == 'B']['days_to_respond']
ax3.hist(df_a, bins=13, alpha=0.6, color=colors[0], label='Campaign A')
ax3.hist(df_b, bins=9,  alpha=0.6, color=colors[1], label='Campaign B')
ax3.set_title('Days to Respond Distribution', fontweight='bold')
ax3.set_xlabel('Days')
ax3.set_ylabel('Count')
ax3.legend()

# Chart 4 — Summary table
ax4 = axes[1, 1]
ax4.axis('off')
table_data = [
    ['Metric', 'Campaign A', 'Campaign B', 'Lift'],
    ['Open Rate',     '45.6%', '57.4%', '+11.8pp'],
    ['Click Rate',    '22.4%', '27.8%', '+5.4pp'],
    ['Response Rate', '9.6%',  '14.8%', '+5.2pp'],
    ['Avg Days',      '7.5',   '5.5',   '-2 days'],
    ['P-Value',       '—',     '0.016',  '✅ Sig.'],
]

table = ax4.table(cellText=table_data[1:],
                  colLabels=table_data[0],
                  cellLoc='center',
                  loc='center')
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.2, 2)
ax4.set_title('Summary Table', fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('outputs/ab_test_results.png', 
            bbox_inches='tight', dpi=150)
print("Chart saved to outputs/ab_test_results.png")
plt.show()