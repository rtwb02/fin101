import financedatabase as fd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8')
sns.set_palette("Set2")  # Using a more balanced color palette

# Define market cap ranking order
market_cap_order = ["Mega Cap", "Large Cap", "Mid Cap", "Small Cap", "Micro Cap", "Nano Cap"]

# Step 1: Load equities from financedatabase
print("Loading data from financedatabase...")
equities = fd.Equities()
all_equities = equities.select(country="United States")

# Handle data types
if isinstance(all_equities, dict):
    df = pd.DataFrame.from_dict(all_equities, orient='index')
elif isinstance(all_equities, pd.DataFrame):
    df = all_equities
elif hasattr(all_equities, '__iter__'):
    df = pd.DataFrame(all_equities)
else:
    raise ValueError(f"Unexpected data type from financedatabase: {type(all_equities)}")

# Step 2: Identify important columns
available_columns = df.columns.tolist()
sector_col = next((col for col in available_columns if 'sector' in col.lower()), None)
market_cap_col = next((col for col in available_columns if 'market_cap' in col.lower()), None)
industry_col = next((col for col in available_columns if 'industry' in col.lower()), None)
name_col = next((col for col in available_columns if 'name' in col.lower()), None)

if not all([sector_col, market_cap_col, name_col]):
    raise ValueError("Required columns (sector, market cap, name) not found.")

# Step 3: Clean and filter data
target_sectors = ['Financials', 'Industrials', 'Materials']
df_filtered = df[df[sector_col].isin(target_sectors)]

# Ensure market cap column exists and contains categorical labels
df_filtered = df_filtered[df_filtered[market_cap_col].notna()]
df_filtered[name_col] = df_filtered[name_col].fillna("Unknown")

# Convert market cap category to ordered categorical for proper sorting
df_filtered[market_cap_col] = pd.Categorical(df_filtered[market_cap_col], categories=market_cap_order, ordered=True)

# Step 4: Top 5 Companies by Market Cap in Each Sector
print("\nTop 5 Companies by Market Cap (Each Sector):")
for sector in target_sectors:
    sector_df = df_filtered[df_filtered[sector_col] == sector].sort_values(by=market_cap_col).head(5)
    
    print(f"\n{sector}")
    print("-" * 60)
    for _, row in sector_df.iterrows():
        name = row[name_col] if pd.notna(row[name_col]) else "Unknown"
        market_cap_category = row[market_cap_col]
        industry = row.get(industry_col, "N/A") if industry_col else "N/A"
        print(f"{name:<35} | {market_cap_category:<15} | {industry}")

# Step 5: Market Cap Distribution by Percentage
market_cap_distribution = df_filtered.groupby([sector_col, market_cap_col]).size().unstack().fillna(0)
market_cap_percentage = market_cap_distribution.div(market_cap_distribution.sum(axis=1), axis=0) * 100

# Print Percentage Data in Console
print("\nMarket Cap Distribution by Percentage:")
print(market_cap_percentage.round(2))

# Plot Market Cap Distribution
plt.figure(figsize=(12, 6))
ax = market_cap_percentage.plot(kind='bar', stacked=True, colormap="Set2", ax=plt.gca())

# Add percentage labels on top of the bars
for bar in ax.patches:
    height = bar.get_height()
    if height > 0:
        ax.annotate(f"{height:.1f}%", (bar.get_x() + bar.get_width() / 2, bar.get_y() + height),
                    ha='center', va='bottom', fontsize=10, color='black')

plt.title("Market Cap Distribution by Percentage (Per Sector)")
plt.xlabel("Sector")
plt.ylabel("Percentage (%)")
plt.xticks(rotation=45)
plt.legend(title="Market Cap Category")
plt.show()



