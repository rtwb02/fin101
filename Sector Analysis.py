import financedatabase as fd
import pandas as pd
import matplotlib.pyplot as plt
import squarify
import numpy as np

try:
    equities = fd.Equities()
    print("Loading equity data... (this may take a minute)")
    
    all_equities = equities.select()
    print(f"Type of all_equities: {type(all_equities)}")
    
    # Handle different data types from API
    if isinstance(all_equities, dict):
        df = pd.DataFrame.from_dict(all_equities, orient='index')
    elif isinstance(all_equities, pd.DataFrame):
        df = all_equities
    elif hasattr(all_equities, '__iter__'):
        df = pd.DataFrame(all_equities)
    else:
        raise ValueError(f"Unexpected data type: {type(all_equities)}")
    
    print(f"Total companies loaded: {len(df)}")
    print("Data columns:", df.columns.tolist())
    print("First few rows:")
    print(df.head())
    
except Exception as e:
    print(f"Error loading data: {e}")
    print("Creating sample data for demonstration...")
    
    sample_data = {
        'country': ['United States', 'China', 'Japan', 'United Kingdom', 'Canada'] * 200,
        'sector': ['Technology', 'Healthcare', 'Financial Services', 'Energy', 'Consumer Discretionary'] * 200,
        'industry': ['Software', 'Pharmaceuticals', 'Banks', 'Oil & Gas', 'Retail'] * 200,
        'name': [f'Company_{i}' for i in range(1000)]
    }
    df = pd.DataFrame(sample_data)
    print("Using sample data for demonstration")

print("\nCleaning data...")

available_columns = df.columns.tolist()
print(f"Available columns: {available_columns}")

# Find column names that match our needs
country_col = None
sector_col = None

for col in available_columns:
    if 'country' in col.lower():
        country_col = col
    elif 'sector' in col.lower():
        sector_col = col

if not country_col or not sector_col:
    print("Warning: Required columns not found. Available columns:", available_columns)
    if len(available_columns) >= 2:
        country_col = available_columns[0]
        sector_col = available_columns[1]
        print(f"Using {country_col} as country and {sector_col} as sector")

if country_col and sector_col:
    initial_count = len(df)
    df = df.dropna(subset=[country_col, sector_col])
    df = df[df[sector_col] != '']
    
    print(f"Removed {initial_count - len(df)} rows with missing data")
    print(f"Final dataset size: {len(df)} companies")
    
    # Global sector analysis
    sector_counts = df[sector_col].value_counts().head(10)
    
    plt.figure(figsize=(12, 10))
    colors = plt.cm.Set3(np.linspace(0, 1, len(sector_counts)))
    plt.pie(sector_counts.values, 
            labels=sector_counts.index, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            textprops={'fontsize': 10})
    plt.title('Top 10 Sectors by Number of Companies Globally', fontsize=16)
    plt.axis('equal')
    plt.show()
    
    # Global country analysis
    country_counts = df[country_col].value_counts().head(10)
    
    plt.figure(figsize=(12, 10))
    colors = plt.cm.Pastel1(np.linspace(0, 1, len(country_counts)))
    plt.pie(country_counts.values, 
            labels=country_counts.index, 
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            textprops={'fontsize': 10})
    plt.title('Top 10 Countries by Number of Companies', fontsize=16)
    plt.axis('equal')
    plt.show()
    
    # Country breakdown for top 3 sectors
    top_3_sectors = sector_counts.head(3).index.tolist()
    
    for i, sector in enumerate(top_3_sectors, 1):
        sector_df = df[df[sector_col] == sector]
        sector_country_counts = sector_df[country_col].value_counts().head(10)
        
        plt.figure(figsize=(12, 10))
        colors = plt.cm.tab20(np.linspace(0, 1, len(sector_country_counts)))
        wedges, texts, autotexts = plt.pie(sector_country_counts.values,
                                          labels=sector_country_counts.index,
                                          autopct='%1.1f%%',
                                          startangle=90,
                                          colors=colors,
                                          textprops={'fontsize': 9})
        
        plt.title(f'Country Distribution for Sector: {sector}', fontsize=16)
        plt.axis('equal')
        plt.show()
        
        # Industry breakdown within sector
        industry_col = None
        for col in available_columns:
            if 'industry' in col.lower():
                industry_col = col
                break
        
        if industry_col and industry_col in sector_df.columns:
            top_industries = sector_df[industry_col].value_counts().head(8)
            
            plt.figure(figsize=(10, 8))
            colors = plt.cm.Accent(np.linspace(0, 1, len(top_industries)))
            plt.pie(top_industries.values,
                    labels=top_industries.index,
                    autopct='%1.1f%%',
                    startangle=90,
                    colors=colors,
                    textprops={'fontsize': 9})
            plt.title(f'Top Industries in {sector} Sector', fontsize=14)
            plt.axis('equal')
            plt.show()
            
            print(f"\nIndustry breakdown for '{sector}' sector:")
            for idx, (industry, count) in enumerate(top_industries.items()):
                percent = (count / len(sector_df)) * 100
                print(f"{idx+1}. {industry}: {count} companies ({percent:.1f}%)")
        
        print("\n" + "-"*80 + "\n")
    
    # Overall sector distribution
    plt.figure(figsize=(10, 10))
    sector_counts_all = df[sector_col].value_counts()
    plt.pie(sector_counts_all.head(10), 
            labels=sector_counts_all.head(10).index, 
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 9})
    plt.title('Global Sector Distribution (Top 10)')
    plt.show()
    
    # Country-specific analysis function
    def analyze_country(country_name):
        country_df = df[df[country_col] == country_name]
        
        if len(country_df) == 0:
            print(f"No data found for {country_name}")
            return
        
        print(f"\nAnalyzing {country_name} - {len(country_df)} companies")
        
        sector_counts = country_df[sector_col].value_counts()
        
        if len(sector_counts) > 0:
            plt.figure(figsize=(15, 10))
            squarify.plot(sizes=sector_counts.values,
                          label=[f"{s}\n({c} companies)" for s, c in zip(sector_counts.index, sector_counts.values)],
                          alpha=0.8,
                          text_kwargs={'fontsize':10})
            plt.title(f'Sector Distribution in {country_name}', fontsize=18)
            plt.axis('off')
            plt.show()
        
        industry_col = None
        for col in available_columns:
            if 'industry' in col.lower():
                industry_col = col
                break
        
        if industry_col:
            for sector in sector_counts.head(3).index:
                sector_df = country_df[country_df[sector_col] == sector]
                industry_counts = sector_df[industry_col].value_counts().head(8)
                
                if len(industry_counts) > 0:
                    plt.figure(figsize=(10, 8))
                    colors = plt.cm.Set2(np.linspace(0, 1, len(industry_counts)))
                    plt.pie(industry_counts.values,
                            labels=industry_counts.index,
                            autopct='%1.1f%%',
                            startangle=90,
                            colors=colors,
                            textprops={'fontsize': 9})
                    plt.title(f'{country_name}: {sector} Industry Breakdown', fontsize=14)
                    plt.axis('equal')
                    plt.show()
    
    # Run analysis
    top_countries = country_counts.head(10).index.tolist()
    
    print("\nTop 10 countries with most companies:")
    for i, country in enumerate(top_countries, 1):
        count = country_counts[country]
        print(f"{i}. {country} ({count} companies)")
    
    print(f"\nRunning detailed analysis for top country: {top_countries[0]}")
    analyze_country(top_countries[0])
    
else:
    print("Could not identify required columns for analysis")
    print("Please check the data structure and column names")