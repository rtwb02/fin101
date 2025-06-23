import financedatabase as fd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8')
sns.set_palette("Set2")

# Define market cap ranking order
market_cap_order = ["Mega Cap", "Large Cap", "Mid Cap", "Small Cap", "Micro Cap", "Nano Cap"]

def load_and_process_data(countries=None):
    """Load and process equity data from financedatabase"""
    print(f"Loading data from financedatabase for countries: {countries if countries else 'All countries'}...")
    equities = fd.Equities()
    
    if countries:
        if isinstance(countries, str):
            all_equities = equities.select(country=countries)
        else:
            all_equities = {}
            for country in countries:
                try:
                    country_data = equities.select(country=country)
                    if isinstance(country_data, dict):
                        all_equities.update(country_data)
                except:
                    print(f"Warning: Could not load data for {country}")
    else:
        all_equities = equities.select()
    
    # Handle data types
    if isinstance(all_equities, dict):
        df = pd.DataFrame.from_dict(all_equities, orient='index')
    elif isinstance(all_equities, pd.DataFrame):
        df = all_equities
    elif hasattr(all_equities, '__iter__'):
        df = pd.DataFrame(all_equities)
    else:
        raise ValueError(f"Unexpected data type from financedatabase: {type(all_equities)}")
    
    return df

def identify_columns(df):
    """Identify important columns in the dataframe"""
    available_columns = df.columns.tolist()
    print(f"Available columns: {available_columns}")
    
    sector_col = next((col for col in available_columns if 'sector' in col.lower()), None)
    market_cap_col = next((col for col in available_columns if 'market_cap' in col.lower() or 'marketcap' in col.lower()), None)
    industry_col = next((col for col in available_columns if 'industry' in col.lower()), None)
    name_col = next((col for col in available_columns if 'name' in col.lower() or 'long_name' in col.lower()), None)
    country_col = next((col for col in available_columns if 'country' in col.lower()), None)
    
    return sector_col, market_cap_col, industry_col, name_col, country_col

def analyze_us_vs_rest_of_world():
    """Compare US vs Rest of World in target industries"""
    print("="*80)
    print("US vs REST OF WORLD COMPARISON - TARGET INDUSTRIES")
    print("="*80)
    
    # Load global data
    df_global = load_and_process_data()
    sector_col, market_cap_col, industry_col, name_col, country_col = identify_columns(df_global)
    
    if not all([sector_col, country_col]):
        print("Required columns not found for analysis")
        return None, None
    
    # Clean data
    df_clean = df_global.dropna(subset=[sector_col, country_col])
    
    target_sectors = ['Financials', 'Industrials', 'Materials']
    
    # Filter for target sectors only
    df_target = df_clean[df_clean[sector_col].isin(target_sectors)]
    
    # Create US vs Rest of World classification
    df_target['region'] = df_target[country_col].apply(lambda x: 'United States' if x == 'United States' else 'Rest of World')
    
    print(f"Total companies in target sectors globally: {len(df_target):,}")
    
    # Overall US vs Rest of World comparison
    region_counts = df_target['region'].value_counts()
    region_percentages = (region_counts / len(df_target) * 100).round(2)
    
    print("\nTarget Industries Distribution:")
    print("-" * 50)
    for region, count in region_counts.items():
        percentage = region_percentages[region]
        print(f"{region:<15}: {count:>8,} companies ({percentage:>5.1f}%)")
    
    # Sector-wise US vs Rest of World comparison
    sector_region_analysis = df_target.groupby([sector_col, 'region']).size().unstack(fill_value=0)
    sector_region_percentages = sector_region_analysis.div(sector_region_analysis.sum(axis=1), axis=0) * 100
    
    print("\nSector-wise US vs Rest of World Distribution:")
    print("-" * 70)
    print(f"{'Sector':<15} | {'US Count':<10} | {'US %':<8} | {'RoW Count':<12} | {'RoW %':<8}")
    print("-" * 70)
    
    for sector in target_sectors:
        if sector in sector_region_analysis.index:
            us_count = sector_region_analysis.loc[sector, 'United States'] if 'United States' in sector_region_analysis.columns else 0
            row_count = sector_region_analysis.loc[sector, 'Rest of World'] if 'Rest of World' in sector_region_analysis.columns else 0
            total_sector = us_count + row_count
            us_pct = (us_count / total_sector * 100) if total_sector > 0 else 0
            row_pct = (row_count / total_sector * 100) if total_sector > 0 else 0
            
            print(f"{sector:<15} | {us_count:<10,} | {us_pct:<8.1f} | {row_count:<12,} | {row_pct:<8.1f}")
    
    return df_target, sector_region_analysis

def analyze_market_cap_us_vs_world():
    """Analyze market cap distribution US vs Rest of World"""
    print("\n" + "="*80)
    print("MARKET CAP ANALYSIS - US vs REST OF WORLD")
    print("="*80)
    
    # Load global data
    df_global = load_and_process_data()
    sector_col, market_cap_col, industry_col, name_col, country_col = identify_columns(df_global)
    
    if not all([sector_col, market_cap_col, country_col]):
        print("Required columns not found for market cap analysis")
        return None
    
    # Clean data and filter for target sectors
    target_sectors = ['Financials', 'Industrials', 'Materials']
    df_clean = df_global.dropna(subset=[sector_col, market_cap_col, country_col])
    df_target = df_clean[df_clean[sector_col].isin(target_sectors)]
    
    # Create region classification
    df_target['region'] = df_target[country_col].apply(lambda x: 'United States' if x == 'United States' else 'Rest of World')
    
    print(f"Companies with market cap data in target sectors: {len(df_target):,}")
    
    # Market cap distribution by region
    marketcap_region_analysis = df_target.groupby(['region', market_cap_col]).size().unstack(fill_value=0)
    marketcap_region_percentages = marketcap_region_analysis.div(marketcap_region_analysis.sum(axis=1), axis=0) * 100
    
    print("\nMarket Cap Distribution by Region:")
    print("-" * 60)
    
    for region in ['United States', 'Rest of World']:
        if region in marketcap_region_analysis.index:
            print(f"\n{region}:")
            region_data = marketcap_region_analysis.loc[region]
            total_region = region_data.sum()
            
            for cap_category in market_cap_order:
                if cap_category in region_data.index:
                    count = region_data[cap_category]
                    percentage = (count / total_region * 100) if total_region > 0 else 0
                    print(f"  {cap_category:<13}: {count:>6,} companies ({percentage:>5.1f}%)")
    
    # Sector-wise market cap analysis
    print("\nSector-wise Market Cap Analysis (US vs Rest of World):")
    print("-" * 80)
    
    for sector in target_sectors:
        sector_data = df_target[df_target[sector_col] == sector]
        if len(sector_data) > 0:
            print(f"\n{sector.upper()}:")
            sector_marketcap_region = sector_data.groupby(['region', market_cap_col]).size().unstack(fill_value=0)
            
            for region in ['United States', 'Rest of World']:
                if region in sector_marketcap_region.index:
                    print(f"  {region}:")
                    region_data = sector_marketcap_region.loc[region]
                    total_region = region_data.sum()
                    
                    for cap_category in market_cap_order:
                        if cap_category in region_data.index and region_data[cap_category] > 0:
                            count = region_data[cap_category]
                            percentage = (count / total_region * 100) if total_region > 0 else 0
                            print(f"    {cap_category:<13}: {count:>4,} ({percentage:>5.1f}%)")
    
    return marketcap_region_analysis

def analyze_industry_breakdown_global():
    """Detailed industry breakdown within each sector globally"""
    print("\n" + "="*80)
    print("DETAILED INDUSTRY BREAKDOWN - GLOBAL ANALYSIS")
    print("="*80)
    
    # Load global data
    df_global = load_and_process_data()
    sector_col, market_cap_col, industry_col, name_col, country_col = identify_columns(df_global)
    
    if not all([sector_col, industry_col, country_col]):
        print("Required columns not found for industry breakdown")
        return None
    
    # Clean data
    target_sectors = ['Financials', 'Industrials', 'Materials']
    df_clean = df_global.dropna(subset=[sector_col, industry_col, country_col])
    df_target = df_clean[df_clean[sector_col].isin(target_sectors)]
    
    # Create region classification
    df_target['region'] = df_target[country_col].apply(lambda x: 'United States' if x == 'United States' else 'Rest of World')
    
    industry_analysis = {}
    
    for sector in target_sectors:
        print(f"\n{sector.upper()} SECTOR - Industry Breakdown:")
        print("-" * 60)
        
        sector_data = df_target[df_target[sector_col] == sector]
        
        if len(sector_data) > 0:
            # Overall industry distribution in this sector
            industry_counts = sector_data[industry_col].value_counts().head(10)
            total_sector = len(sector_data)
            
            print(f"Total companies in {sector}: {total_sector:,}")
            print(f"\nTop 10 Industries in {sector}:")
            
            for industry, count in industry_counts.items():
                percentage = (count / total_sector * 100)
                print(f"  {industry:<35}: {count:>6,} ({percentage:>5.1f}%)")
            
            # US vs Rest of World breakdown for top industries
            print(f"\nUS vs Rest of World - Top 5 Industries in {sector}:")
            print(f"{'Industry':<35} | {'US':<8} | {'RoW':<8} | {'US %':<6} | {'RoW %':<6}")
            print("-" * 80)
            
            top_5_industries = industry_counts.head(5).index
            
            for industry in top_5_industries:
                industry_data = sector_data[sector_data[industry_col] == industry]
                region_counts = industry_data['region'].value_counts()
                
                us_count = region_counts.get('United States', 0)
                row_count = region_counts.get('Rest of World', 0)
                total_industry = us_count + row_count
                
                us_pct = (us_count / total_industry * 100) if total_industry > 0 else 0
                row_pct = (row_count / total_industry * 100) if total_industry > 0 else 0
                
                print(f"{industry:<35} | {us_count:<8,} | {row_count:<8,} | {us_pct:<6.1f} | {row_pct:<6.1f}")
            
            industry_analysis[sector] = {
                'total_companies': total_sector,
                'top_industries': industry_counts.head(10).to_dict(),
                'us_vs_row': {}
            }
    
    return industry_analysis

def create_comprehensive_visualizations(df_target, sector_region_analysis, marketcap_region_analysis):
    """Create comprehensive visualizations for US vs Rest of World analysis"""
    print("\n" + "="*80)
    print("CREATING COMPREHENSIVE VISUALIZATIONS")
    print("="*80)
    
    # Create a large figure with multiple subplots
    fig = plt.figure(figsize=(24, 16))
    
    # 1. Overall US vs Rest of World Distribution
    ax1 = plt.subplot(2, 4, 1)
    if df_target is not None:
        region_counts = df_target['region'].value_counts()
        colors = ['#ff7f0e', '#1f77b4']  # Orange for US, Blue for Rest of World
        bars = ax1.bar(region_counts.index, region_counts.values, color=colors, alpha=0.8)
        ax1.set_title('Target Industries: US vs Rest of World', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Number of Companies')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}', ha='center', va='bottom')
    
    # 2. Sector-wise US vs Rest of World (Stacked Bar)
    ax2 = plt.subplot(2, 4, 2)
    if sector_region_analysis is not None:
        sector_region_analysis.plot(kind='bar', stacked=True, ax=ax2, color=['#ff7f0e', '#1f77b4'], alpha=0.8)
        ax2.set_title('Sector Distribution: US vs Rest of World', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Number of Companies')
        ax2.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
    
    # 3. Sector-wise Percentage Distribution
    ax3 = plt.subplot(2, 4, 3)
    if sector_region_analysis is not None:
        sector_percentages = sector_region_analysis.div(sector_region_analysis.sum(axis=1), axis=0) * 100
        sector_percentages.plot(kind='bar', ax=ax3, color=['#ff7f0e', '#1f77b4'], alpha=0.8)
        ax3.set_title('Sector Distribution (%): US vs Rest of World', fontsize=12, fontweight='bold')
        ax3.set_ylabel('Percentage (%)')
        ax3.legend(title='Region', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax3.set_ylim(0, 100)
        plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
    
    # 4. Market Cap Distribution - US
    ax4 = plt.subplot(2, 4, 4)
    if marketcap_region_analysis is not None and 'United States' in marketcap_region_analysis.index:
        us_marketcap = marketcap_region_analysis.loc['United States']
        us_marketcap = us_marketcap[us_marketcap > 0]  # Filter out zero values
        colors = plt.cm.Set3(range(len(us_marketcap)))
        wedges, texts, autotexts = ax4.pie(us_marketcap.values, labels=us_marketcap.index, 
                                          autopct='%1.1f%%', colors=colors, startangle=90)
        ax4.set_title('US Market Cap Distribution', fontsize=12, fontweight='bold')
    
    # 5. Market Cap Distribution - Rest of World
    ax5 = plt.subplot(2, 4, 5)
    if marketcap_region_analysis is not None and 'Rest of World' in marketcap_region_analysis.index:
        row_marketcap = marketcap_region_analysis.loc['Rest of World']
        row_marketcap = row_marketcap[row_marketcap > 0]  # Filter out zero values
        colors = plt.cm.Set3(range(len(row_marketcap)))
        wedges, texts, autotexts = ax5.pie(row_marketcap.values, labels=row_marketcap.index, 
                                          autopct='%1.1f%%', colors=colors, startangle=90)
        ax5.set_title('Rest of World Market Cap Distribution', fontsize=12, fontweight='bold')
    
    # 6. Market Cap Comparison (Side by Side)
    ax6 = plt.subplot(2, 4, 6)
    if marketcap_region_analysis is not None:
        marketcap_region_analysis.plot(kind='bar', ax=ax6, color=['#ff7f0e', '#1f77b4'], alpha=0.8)
        ax6.set_title('Market Cap Distribution Comparison', fontsize=12, fontweight='bold')
        ax6.set_ylabel('Number of Companies')
        ax6.legend(title='Region')
        plt.setp(ax6.get_xticklabels(), rotation=45, ha='right')
    
    # 7. Market Cap Percentage Comparison
    ax7 = plt.subplot(2, 4, 7)
    if marketcap_region_analysis is not None:
        marketcap_percentages = marketcap_region_analysis.div(marketcap_region_analysis.sum(axis=1), axis=0) * 100
        marketcap_percentages.plot(kind='bar', ax=ax7, color=['#ff7f0e', '#1f77b4'], alpha=0.8)
        ax7.set_title('Market Cap Distribution (%) Comparison', fontsize=12, fontweight='bold')
        ax7.set_ylabel('Percentage (%)')
        ax7.legend(title='Region')
        ax7.set_ylim(0, 100)
        plt.setp(ax7.get_xticklabels(), rotation=45, ha='right')
    
    # 8. Regional Dominance by Sector
    ax8 = plt.subplot(2, 4, 8)
    if sector_region_analysis is not None:
        # Calculate which region dominates each sector
        sector_percentages = sector_region_analysis.div(sector_region_analysis.sum(axis=1), axis=0) * 100
        
        # Create a stacked bar showing US percentage (Rest of World is implicit)
        us_percentages = sector_percentages['United States'] if 'United States' in sector_percentages.columns else [0] * len(sector_percentages)
        
        bars = ax8.barh(range(len(sector_percentages)), us_percentages, color='#ff7f0e', alpha=0.8, label='US %')
        ax8.barh(range(len(sector_percentages)), 100 - us_percentages, left=us_percentages, 
                color='#1f77b4', alpha=0.8, label='Rest of World %')
        
        ax8.set_title('Regional Dominance by Sector', fontsize=12, fontweight='bold')
        ax8.set_xlabel('Percentage (%)')
        ax8.set_yticks(range(len(sector_percentages)))
        ax8.set_yticklabels(sector_percentages.index)
        ax8.legend()
        ax8.set_xlim(0, 100)
        
        # Add percentage labels
        for i, (us_pct, total_pct) in enumerate(zip(us_percentages, [100] * len(us_percentages))):
            ax8.text(us_pct/2, i, f'{us_pct:.1f}%', ha='center', va='center', fontweight='bold')
            ax8.text(us_pct + (100-us_pct)/2, i, f'{100-us_pct:.1f}%', ha='center', va='center', fontweight='bold')
    
    plt.tight_layout()
    
    # Save the figure instead of showing it
    plt.savefig('us_vs_row_financial_analysis.png', dpi=300, bbox_inches='tight')
    print("Figure saved as 'us_vs_row_financial_analysis.png'")
    
    plt.show()
    print("Comprehensive visualizations created successfully!")

def main():
    """Main function to run the complete US vs Rest of World analysis"""
    print("US vs REST OF WORLD FINANCIAL ANALYSIS")
    print("="*80)
    
    # 1. US vs Rest of World comparison in target industries
    df_target, sector_region_analysis = analyze_us_vs_rest_of_world()
    
    # 2. Market cap analysis US vs Rest of World
    marketcap_region_analysis = analyze_market_cap_us_vs_world()
    
    # 3. Detailed industry breakdown analysis
    industry_analysis = analyze_industry_breakdown_global()
    
    # 4. Create comprehensive visualizations
    create_comprehensive_visualizations(df_target, sector_region_analysis, marketcap_region_analysis)
    
    print("\n" + "="*80)
    print("US vs REST OF WORLD ANALYSIS COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()