Here's a description for your GitHub repository in markdown format:

---

# Web Scraping and Data Analysis of Largest US Companies by Revenue

This project demonstrates how to scrape data from a Wikipedia page listing the largest companies in the United States by revenue and perform data analysis using Python libraries such as `requests`, `BeautifulSoup`, and `pandas`.

## Description

The project is designed to:
1. **Fetch and Parse HTML**: Retrieve data from a Wikipedia page containing tables with company details such as revenue, profits, and industries.
2. **Extract Tables**: Identify and extract tables with the class `wikitable` from the parsed HTML content.
3. **Process and Clean Data**: Clean the extracted data, removing unnecessary characters like commas and dollar signs, and convert columns to appropriate numerical values.
4. **Save Data to CSV**: Convert the processed data into a structured format and save it as CSV files.
5. **Data Analysis**: 
   - Calculate the total revenue and profits for the companies.
   - Extract unique industries across multiple tables.
   - Rank companies by their revenue and display the top 5 companies based on their revenue.

## Files

1. **scraping_and_analysis.py**: Main script that contains functions for scraping data, cleaning, and performing calculations.
2. **tables CSVs**: The CSV files generated from the web scraping, representing the data from different tables on the Wikipedia page.

## Steps in the Project

### 1. Fetching HTML Content
A `GET` request is sent to the Wikipedia page to retrieve its HTML content. This content is then parsed using BeautifulSoup.

```python
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
```

### 2. Extracting Data
The script finds all tables with the class `wikitable` and processes each table by extracting relevant data (e.g., company name, revenue, industry).

```python
tables = soup.find_all("table", class_="wikitable")
```

### 3. Data Cleaning
The data is cleaned by removing commas, dollar signs, and converting strings to numeric values to make the data ready for analysis.

```python
df[column_name] = df[column_name].str.replace(",", "", regex=True).str.replace("$", "", regex=True)
df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
```

### 4. Calculating Totals
For each DataFrame (corresponding to different CSVs), the script calculates the total revenue and profit for the companies listed.

```python
total_revenue = df[column_name].sum() * conversion_factor
```

### 5. Ranking Companies
A rank column is added to each DataFrame based on revenue, allowing easy identification of top-performing companies.

```python
df['rank'] = df[rank_column].rank(ascending=True)
```

### 6. Extracting Unique Industries
The script extracts the unique industries across the three DataFrames and displays the number of unique industries.

```python
unique_industries = pd.concat([df[industry_column] for df in dfs.values()], ignore_index=True).dropna().unique()
```

### 7. Output
The results include:
- **CSV files** for each table.
- A printout of total revenue, top 5 companies, unique industries, and ranks.

## Requirements

To run this project, install the required libraries by using the following pip command:

```bash
pip install requests beautifulsoup4 pandas
```

## How to Run the Script

1. Clone this repository.
2. Run the `scraping_and_analysis.py` script:
   ```bash
   python scraping_and_analysis.py
   ```
3. The script will fetch data from the Wikipedia page, process it, and generate the results in CSV format.
