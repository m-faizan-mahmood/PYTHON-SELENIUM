import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to send GET request and retrieve HTML content from the URL
def fetch_html(url):
    """Fetch the HTML content from the given URL."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

# Function to extract tables from the parsed HTML
def extract_tables(soup):
    """Extract all tables with class 'wikitable' from the parsed HTML."""
    tables = soup.find_all("table", class_="wikitable")
    return tables

# Function to process and extract data from a single table
def process_table(table):
    """Extract and clean data from a single table."""
    data = []
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all(["th", "td"])
        cols = [ele.text.strip() for ele in cols]
        data.append(cols)
    return data

# Function to convert data to a DataFrame and save as CSV
def save_table_to_csv(data, table_number):
    """Convert the extracted data to a DataFrame and save it as a CSV file."""
    df = pd.DataFrame(data)
    df.columns = df.iloc[0]  # Set the first row as header
    df = df[:]  # Remove the first row from the DataFrame
    filename = f"table411_{table_number}.csv"
    df.to_csv(filename, index=False)
    print(f"Table {table_number} saved to {filename}")

# Function to load CSV files into a dictionary of DataFrames
def load_csvs(file_paths):
    """Load CSV files into a dictionary of DataFrames."""
    dfs = {}
    for i, file_path in enumerate(file_paths):
        df_name = f"df{i+1}"
        dfs[df_name] = pd.read_csv(file_path)
    return dfs

# Function to clean and convert columns (handles both numeric conversion and string cleaning)
def clean_column(df, column_name):
    """Cleans the column by removing commas, dollar signs, and converting to float."""
    if df[column_name].dtype == 'object':
        df[column_name] = df[column_name].str.replace(",", "", regex=True).str.replace("$", "", regex=True)
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
    return df

# Function to calculate total revenue or profit
def calculate_total(df, column_name, conversion_factor=1):
    """Calculate the total of a column, optionally applying a conversion factor."""
    total = df[column_name].sum() * conversion_factor
    return total

# Function to add rank column based on a specific column
def add_rank_column(dfs, rank_column):
    """Add a rank column based on the 'rank_column'."""
    for df_name, df in dfs.items():
        if rank_column in df.columns:
            df['rank'] = df[rank_column].rank(ascending=True)
            print(f"Updated {df_name}:")
            print(df.head())  # Display the first few rows for verification
    return dfs

# Function to get unique industries and top 5 companies by revenue
def get_unique_industries_and_top_companies(dfs):
    """Get the unique industries and top 5 companies by revenue."""
    
    # Assuming the industry column is in the first DataFrame, adjust based on actual column name
    # If there's a column that represents the industry, you can extract unique industries like this
    industry_column = "Industry"  # Change this if the industry column has a different name
    
    # Get unique industries
    unique_industries = pd.concat([df[industry_column] for df in dfs.values()], ignore_index=True).dropna().unique()
    print(f"Number of unique industries: {len(unique_industries)}")
    
    # Assuming revenue is in "Revenue (USD millions)" column for df1
    # Sort by revenue and get the top 5 companies by revenue
    top_companies_df1 = dfs["df1"].sort_values(by="Revenue (USD millions)", ascending=False).head(5)
    top_companies_df1 = top_companies_df1[["Name", "Revenue (USD millions)"]]  # Adjust columns if necessary
    print("Top 5 companies by revenue:")
    print(top_companies_df1)

# Add this function call to the main function to see the results
def main():
    """Main function to orchestrate the scraping, cleaning, and calculations."""
    # Define the URL of the Wikipedia page
    url = "https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue"

    # Fetch HTML content
    soup = fetch_html(url)

    # Extract tables from the page
    tables = extract_tables(soup)

    # Process each table and save to CSV
    for i, table in enumerate(tables):
        data = process_table(table)
        save_table_to_csv(data, i + 1)

    # Define file paths
    file_paths = ["/content/table411_1.csv", "/content/table411_2.csv", "/content/table411_3.csv"]

    # Load the CSVs
    dfs = load_csvs(file_paths)

    # Clean specific columns in each DataFrame
    dfs["df1"] = clean_column(dfs["df1"], "Revenue (USD millions)")
    dfs["df2"] = clean_column(dfs["df2"], "Revenue (USD billions)")
    dfs["df3"] = clean_column(dfs["df3"], "Profits(USD millions)")

    # Calculate total revenue or profit for each DataFrame
    total_revenue_df1 = calculate_total(dfs["df1"], "Revenue (USD millions)")
    total_revenue_df2 = calculate_total(dfs["df2"], "Revenue (USD billions)", conversion_factor=1000)  # Convert billions to millions
    total_revenue_df3 = calculate_total(dfs["df3"], "Profits(USD millions)")

    # Print totals
    print(f"Total revenue for df1: {total_revenue_df1}")
    print(f"Total revenue for df2: {total_revenue_df2}")
    print(f"Total revenue for df3: {total_revenue_df3}")

    # Add rank column based on `revenue_percentage`
    dfs = add_rank_column(dfs, "revenue_percentage")
    
    # Get unique industries and top 5 companies
    get_unique_industries_and_top_companies(dfs)

# Run the main function
if __name__ == "__main__":
    main()
