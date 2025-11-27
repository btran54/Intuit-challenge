# I picked this specific dataset from https://www.kaggle.com/datasets/hummaamqaasim/jobs-in-data and decided to use it because I was originally searching 
# for salaries for software engineer roles within the tech industry, but the dataset was too unorganized and the data itself wasn't concrete (salary 
# ranges like "$68K - $94K (Glassdoor est.)" instead of actual values). I figured that a viable alternative to my original dataset was data science, and 
# the specific one I found had better structure and labeling. This dataset contained several different columns including job titles, job categories, 
# salary in USD, experience levels, employment types, work settings, company locations, and company sizes. For this analysis, I focused on the columns 
# most relevant to demonstrating functional programming and stream operations: job_title, job_category, salary_in_usd, experience_level, employment_type, 
# work_setting, company_location, and company_size. I chose to ignore columns like work_year, salary_currency, salary (non-USD), and employee_residence 
# as they were not necessary for the core analysis objectives.#


import pandas as pd
import numpy as np

# Print a formatted section divider with title
def print_section_header(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)

# Create a summary DataFrame with counts and percentages
def create_count_summary(counts, total_rows):
    percentages = (counts / total_rows * 100).round(2)
    return pd.DataFrame({
        'Count': counts,
        'Percentage': percentages
    })

# Print DataFrame with column formatters
def print_formatted_dataframe(df_csv, formatters):
    print(df_csv.to_string(formatters=formatters))

# Calculate group statistics like the total and percentage
def calculate_group_statistics(df_csv, group_column, value_column, total_value):
    group_sum = df_csv.groupby(group_column, sort=False)[value_column].sum()
    percentages = (group_sum / total_value * 100).round(2)
    
    return pd.DataFrame({
        'Total': group_sum,
        'Percentage': percentages
    })

# Perform analysis on the salary data from the CSV file
def analyze_salary_data(file_path='jobs_in_data.csv'):
    
    # Read CSV with explicit datatypes for memory efficiency and type safety
    dtypes = {
        'job_title': 'string',
        'job_category': 'category',
        'salary_in_usd': 'int32',
        'experience_level': 'category',
        'employment_type': 'category',
        'work_setting': 'category',
        'company_location': 'category',
        'company_size': 'category'
    }
    
    use_cols = list(dtypes.keys())
    
    df_csv = pd.read_csv(file_path, dtype=dtypes, usecols=use_cols)
    print(f"Successfully loaded {len(df_csv):,} rows\n")
    
    total_rows = len(df_csv)
    total_salary = df_csv['salary_in_usd'].sum()
    
    # Population count AND total salary by experience level
    print_section_header("Population Count by Experience Level")
    
    exp_stats = df_csv.groupby('experience_level', sort=False, observed=True).agg({
        'job_title': 'size', # Row count
        'salary_in_usd': 'sum' # Total salary
    })
    exp_stats.columns = ['Count', 'Total Salary']
    
    exp_stats['Count %'] = (exp_stats['Count'] / total_rows * 100).round(2)
    exp_stats['Salary %'] = (exp_stats['Total Salary'] / total_salary * 100).round(2)
    
    count_summary = exp_stats[['Count', 'Count %']]
    count_summary.columns = ['Count', 'Percentage']
    
    # Lambda formatters for pretty printing
    print_formatted_dataframe(count_summary, {
        'Count': lambda x: f"{x:,}",
        'Percentage': lambda x: f"{x:.2f}%"
    })
    print(f"\nTotal: {total_rows:,}")
    
    # Display salary summary
    print_section_header("Total Salary by Experience Level")
    
    salary_summary = exp_stats[['Total Salary', 'Salary %']]
    salary_summary.columns = ['Total Salary', 'Percentage']
    
    print_formatted_dataframe(salary_summary, {
        'Total Salary': lambda x: f"${x:,.2f}",
        'Percentage': lambda x: f"{x:.2f}%"
    })
    print(f"\nGrand Total: ${total_salary:,.2f}")
    
    # Find most common employment type using value_counts() for frequency analysis
    print_section_header("Employment Type Usage")
    
    employment_counts = df_csv['employment_type'].value_counts()
    employment_summary = create_count_summary(employment_counts, total_rows)
    
    print_formatted_dataframe(employment_summary, {
        'Count': lambda x: f"{x:,}",
        'Percentage': lambda x: f"{x:.2f}%"
    })
    print(f"\nMost common employment type: {employment_counts.idxmax()} ({employment_counts.max():,} positions)")
    
    # Find job category with most positions using nlargest() for top-N selections
    print_section_header("Top Job Categories")
    
    category_counts = df_csv['job_category'].value_counts()
    top_categories = category_counts.nlargest(7)
    
    print("\nTop 7 job categories by count:")
    for i, (category, count) in enumerate(top_categories.items(), 1):
        print(f"{i:2d}. {category}: {count:,} positions")
    
    top_category = top_categories.idxmax()
    max_count = top_categories.max()
    print(f"\nMost common category: {top_category} ({max_count:,} positions)")

    # Average salary by job category
    print_section_header("Average Salary by Job Category")
    
    category_avg = df_csv.groupby('job_category', observed=True)['salary_in_usd'].mean().sort_values(ascending=False)
    print("\nTop 5 job categories by average salary:")
    for i, (category, avg) in enumerate(category_avg.head(5).items(), 1):
        print(f"{i}. {category}: ${avg:,.2f}")
    
    print_section_header("Additional Statistics")
    
    avg_salary = df_csv['salary_in_usd'].mean()
    median_salary = df_csv['salary_in_usd'].median()
    unique_titles = df_csv['job_title'].nunique()
    unique_locations = df_csv['company_location'].nunique()
    
    print(f"Total positions: {total_rows:,}")
    print(f"Total salary pool: ${total_salary:,.2f}")
    print(f"Average salary: ${avg_salary:,.2f}")
    print(f"Median salary: ${median_salary:,.2f}")
    print(f"Unique job titles: {unique_titles:,}")
    print(f"Unique company locations: {unique_locations:,}")
    
    return df_csv

if __name__ == "__main__":
    df_csv = analyze_salary_data('jobs_in_data.csv')
    
    print("\n" + "=" * 50)