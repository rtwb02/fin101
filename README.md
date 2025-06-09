# Sector Analysis 01
Start to a series of mini projects to learn more about the market through data
# Global Equity Sector Analysis

A comprehensive Python code for analyzing global equity markets, providing insights into sector distributions, country breakdowns, and industry trends across international stock markets.

## 🚀 Features

- **Global Sector Analysis**: Visualize the distribution of companies across different sectors worldwide
- **Country-wise Breakdown**: Analyze which countries dominate specific sectors
- **Industry Deep-dive**: Explore industry distributions within sectors
- **Interactive Visualizations**: Beautiful pie charts and treemaps for data representation
- **Robust Data Handling**: Automatic fallback to sample data if API fails
- **Flexible Column Detection**: Automatically identifies relevant columns regardless of naming conventions

## 📈 Visualizations

The code generates several types of visualizations:

- **Pie Charts**: For sector, country, and industry distributions
- **Treemaps**: For hierarchical sector analysis by country
- **Color-coded Charts**: Using different color schemes for easy differentiation

The script will:
1. Load global equity data from the Finance Database
2. Clean and process the data
3. Generate comprehensive visualizations
4. Provide detailed analysis for the top country

### Outputs

The analysis:

Pie chart plots shows 
- Top 10 global sectors by company count
- Top 10 countries by company count  
- Country distribution for top 3 sectors
- US Companies distribution analysis with treemaps
  
Top 10 countries with most companies:
1. United States (22273 companies)
2. Canada (8434 companies)
3. China (5656 companies)
4. India (5019 companies)
5. Japan (4399 companies)
6. United Kingdom (3174 companies)
7. Australia (3065 companies)
8. Germany (2565 companies)
9. France (1856 companies)
10. Hong Kong (1799 companies)

Majority of the companies recorded are based in the US

The Top 3 Sectors are further broken down into its sectors

--------------------------------------------------------------------------------

Industry breakdown for 'Financials' sector:
1. Diversified Financials: 9313 companies (68.8%)
2. Banks: 3120 companies (23.0%)
3. Insurance: 1102 companies (8.1%)

--------------------------------------------------------------------------------

Industry breakdown for 'Industrials' sector:
1. Capital Goods: 7402 companies (65.9%)
2. Transportation: 2039 companies (18.2%)
3. Commercial & Professional Services: 1785 companies (15.9%)

--------------------------------------------------------------------------------

Industry breakdown for 'Materials' sector:
1. Materials: 10807 companies (100.0%)

--------------------------------------------------------------------------------
    
## 📊 Data Source
I would like to thank Jerbouma for providing me with this database to help kick start my journey.

This project uses the [Finance Database](https://github.com/JerBouma/FinanceDatabase) which provides:
- 300,000+ symbols containing Equities, ETFs, Funds, Indices, Currencies, Cryptocurrencies and Money Markets
- 180+ countries, 100+ sectors, 1000+ industries
- Real-time data access

## 📋 Future Directions

- [ ] Add market capitalization analysis
- [ ] Dive into each sector and see how different industries correlate with each other (Market movements)
- [ ] Evolution throughout the years (Market Trends)

## 🙏 Acknowledgments

- [Finance Database](https://github.com/JerBouma/FinanceDatabase) for providing comprehensive financial data
- [Matplotlib](https://matplotlib.org/) for visualization capabilities
- [Pandas](https://pandas.pydata.org/) for data manipulation
- [Squarify](https://github.com/laserson/squarify) for treemap visualizations

## 📞 Contact

If you have any questions, suggestions, or issues, please contact tanryan.wb@gmail.com.

---
