
#Part 1
    # 1. Download and Load the Data
# Import the necessary libraries

import pandas as pd
import numpy as np  # Useful for numerical operations
'''
# Load the metadata.csv file into a pandas DataFrame
# We'll call our DataFrame 'df' for simplicity
df = pd.read_csv('metadata.csv')

# Confirm the load was successful by checking the type of 'df'
print("Data loaded successfully. Type of variable 'df':", type(df))


# Examine the first 5 rows
print("\n--- First 5 Rows of the Dataset ---")
print(df.head())

# Examine the last 5 rows to see if the data is consistent
print("\n--- Last 5 Rows of the Dataset ---")
print(df.tail())

# Get a comprehensive overview of the DataFrame's structure
print("\n--- Detailed Information about the DataFrame (Structure) ---")
print(df.info())

    #Basic Data Exploration
# Check the dimensions (number of rows, number of columns)
print("\n--- DataFrame Dimensions ---")
print(f"The dataset has {df.shape[0]:,} rows and {df.shape[1]} columns.")
# The :, in the f-string formats the number with commas for thousands, making it easier to read.
'''

'''
# Check for missing values in ALL columns, sorted by the number of missing values (descending)
print("\n--- Missing Values in All Columns (Sorted) ---")
missing_data = df.isnull().sum().sort_values(ascending=False)
print(missing_data)

# Now, let's focus on key columns for our analysis
key_columns = ['publish_time', 'authors', 'journal', 'title', 'abstract']
print("\n--- Missing Values in Key Columns ---")
for column in key_columns:
    if column in df.columns:  # Check if the column exists in the DataFrame
        missing_count = df[column].isnull().sum()
        missing_percent = (missing_count / df.shape[0]) * 100
        print(f"'{column}': {missing_count:,} missing values ({missing_percent:.2f}%)")
    else:
        print(f"Warning: Column '{column}' not found in the dataset.")


 # Get descriptive statistics for numerical columns
 #numerical columns have int, float and dtypes. These can be filtered by the command describe(). 
print("\n--- Basic Statistics for Numerical Columns ---")
print(df.describe())


#Part 2: Data Cleaning and Preparation
    # 3. Handle Missing Data
# First, I'll recall the missing values situation for key columns
print("=== MISSING VALUES ANALYSIS ===")
key_columns = ['publish_time', 'authors', 'journal', 'title', 'abstract']
for column in key_columns:
    if column in df.columns:
        missing_count = df[column].isnull().sum()
        missing_percent = (missing_count / len(df)) * 100
        print(f"{column}: {missing_count:,} missing ({missing_percent:.2f}%)")

# For publish_time: CRITICAL - we cannot analyze timing without this
# Since we can't fill missing dates reasonably, we'll drop rows where publish_time is missing
print(f"\nOriginal dataset shape: {df.shape}")
df_clean = df.dropna(subset=['publish_time']).copy()  # Using .copy() to avoid SettingWithCopyWarning
print(f"After dropping rows with missing publish_time: {df_clean.shape}")
print(f"Rows removed: {df.shape[0] - df_clean.shape[0]}")

# For journal: We might want to keep papers even if journal is missing
# Let's fill missing journal values with 'Unknown'
df_clean['journal'] = df_clean['journal'].fillna('Unknown')

# For abstract: Since text analysis might be future work, let's keep but note the missingness
df_clean['abstract'] = df_clean['abstract'].fillna('Abstract not available')

print("\n--- Missing Values After Cleaning ---")
for column in key_columns:
    if column in df_clean.columns:
        missing_count = df_clean[column].isnull().sum()
        print(f"{column}: {missing_count} missing")

    #4. Prepare Data for Analysis
# First, let's see what the publish_time data looks like
print("=== DATE CONVERSION ===")
print("Sample of publish_time values before conversion:")
print(df_clean['publish_time'].head(10))

# Convert to datetime - pandas is smart about parsing various formats
# errors='coerce' will convert unparsable dates to NaT (Not a Time)
df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')

# Check if any dates failed to parse
failed_dates = df_clean['publish_time'].isnull().sum()
print(f"\nDates that failed to parse: {failed_dates}")

# If there are failed parses, we might need to drop them
if failed_dates > 0:
    print(f"Shape before dropping failed dates: {df_clean.shape}")
    df_clean = df_clean.dropna(subset=['publish_time'])
    print(f"Shape after dropping failed dates: {df_clean.shape}")

# Extract year and month for easier grouping and analysis
df_clean['publication_year'] = df_clean['publish_time'].dt.year
df_clean['publication_month'] = df_clean['publish_time'].dt.month
df_clean['publication_year_month'] = df_clean['publish_time'].dt.to_period('M')

print("\n--- Date Extraction Sample ---")
print(df_clean[['publish_time', 'publication_year', 'publication_month', 'publication_year_month']].head())

# Create abstract word count - useful for understanding paper length distribution
df_clean['abstract_word_count'] = df_clean['abstract'].apply(
    lambda x: len(str(x).split()) if pd.notnull(x) and x != 'Abstract not available' else 0
)

# Create title word count
df_clean['title_word_count'] = df_clean['title'].apply(
    lambda x: len(str(x).split()) if pd.notnull(x) else 0
)

# Extract number of authors (approximate)
df_clean['author_count'] = df_clean['authors'].apply(
    lambda x: len(str(x).split(';')) if pd.notnull(x) else 0
)

print("\n--- New Columns Sample ---")
print(df_clean[['title_word_count', 'abstract_word_count', 'author_count']].head())

print("=== FINAL CLEANED DATASET SUMMARY ===")
print(f"Final dataset shape: {df_clean.shape}")
print(f"Date range: {df_clean['publish_time'].min()} to {df_clean['publish_time'].max()}")

print("\n--- Data Types After Cleaning ---")
print(df_clean[['publish_time', 'publication_year', 'publication_month', 
                'title_word_count', 'abstract_word_count', 'author_count']].dtypes)

print("\n--- Basic Stats for New Numerical Columns ---")
print(df_clean[['title_word_count', 'abstract_word_count', 'author_count']].describe())

# Save the cleaned dataset for future use
df_clean.to_csv('cord19_metadata_cleaned.csv', index=False)
print("Cleaned dataset saved to 'cord19_metadata_cleaned.csv'")
'''

#Part 3: Data Analysis and Visualization
    # 5. Perform Basic Analysis
# Analysis 1: Papers by publication year
df_clean = pd.read_csv('cord19_metadata_cleaned.csv')
papers_by_year = df_clean['publication_year'].value_counts().sort_index()
print("=== PAPERS BY PUBLICATION YEAR ===")
print(papers_by_year)

# Additional insight: Year-over-year growth
if len(papers_by_year) > 1:
    growth_rate = (papers_by_year.iloc[-1] - papers_by_year.iloc[0]) / papers_by_year.iloc[0] * 100
    print(f"\nGrowth from {papers_by_year.index[0]} to {papers_by_year.index[-1]}: {growth_rate:.1f}%")

# Analysis 2: Top journals (excluding 'Unknown')
top_journals = df_clean[df_clean['journal'] != 'Unknown']['journal'].value_counts().head(15)
print("\n=== TOP 15 JOURNALS BY PUBLICATION COUNT ===")
print(top_journals)

# Calculate market share of top journals
total_papers_with_journal = len(df_clean[df_clean['journal'] != 'Unknown'])
top_journals_share = (top_journals.head(10).sum() / total_papers_with_journal) * 100
print(f"\nTop 10 journals represent {top_journals_share:.1f}% of all papers with journal information")

# Analysis 3: Most frequent words in titles
import re
from collections import Counter

# Combine all titles and clean the text
all_titles = ' '.join(df_clean['title'].dropna().astype(str))
# Convert to lowercase and remove punctuation
words = re.findall(r'\b[a-zA-Z]{3,}\b', all_titles.lower())  # Words with 3+ letters

# Remove common stop words
stop_words = {'the', 'and', 'for', 'with', 'using', 'based', 'from', 'this', 'that', 
              'their', 'were', 'have', 'has', 'been', 'which', 'during', 'among',
              'study', 'analysis', 'review', 'effect', 'effects', 'impact',
              'covid', 'sars', 'cov', 'coronavirus', 'pandemic'}  # Add domain-specific words

filtered_words = [word for word in words if word not in stop_words]
word_freq = Counter(filtered_words).most_common(20)

print("\n=== TOP 20 MOST FREQUENT WORDS IN TITLES ===")
for word, count in word_freq:
    print(f"{word}: {count}")

    # 6. Visualizations
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

print("\n=== GENERATING VISUALIZATIONS ===")

# Visualization 1: Publications over time (by month)
publications_by_month = df_clean.groupby('publication_year_month').size()

plt.figure(figsize=(14, 6))
publications_by_month.plot(kind='line', color='#2E86AB', linewidth=2.5)
plt.title('COVID-19 Research Publications Over Time', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Publication Date', fontsize=12)
plt.ylabel('Number of Publications', fontsize=12)
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('publications_over_time.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"Peak publication month: {publications_by_month.idxmax()} with {publications_by_month.max()} papers")

# Visualization 2: Top journals bar chart
top_10_journals = top_journals.head(10)

plt.figure(figsize=(12, 8))
bars = plt.barh(range(len(top_10_journals)), top_10_journals.values, color='#A23B72')
plt.yticks(range(len(top_10_journals)), top_10_journals.index)
plt.title('Top 10 Journals Publishing COVID-19 Research', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Number of Publications', fontsize=12)
plt.gca().invert_yaxis()  # Highest value at the top

# Add value labels on bars
for i, bar in enumerate(bars):
    plt.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2, 
             f'{int(bar.get_width())}', ha='left', va='center')

plt.tight_layout()
plt.savefig('top_journals.png', dpi=300, bbox_inches='tight')
plt.show()

# Visualization 3: Word cloud
try:
    from wordcloud import WordCloud
    
    # Create word cloud
    wordcloud = WordCloud(width=1200, height=600, 
                         background_color='white',
                         colormap='viridis',
                         stopwords=stop_words).generate(all_titles)
    
    plt.figure(figsize=(14, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Most Frequent Words in COVID-19 Paper Titles', 
              fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('title_wordcloud.png', dpi=300, bbox_inches='tight')
    plt.show()
    
except ImportError:
    print("WordCloud library not installed. Install it with: pip install wordcloud")
    # Alternative: Show the top words as a bar chart
    words, counts = zip(*word_freq)
    plt.figure(figsize=(12, 8))
    plt.barh(range(len(words)), counts, color='#F18F01')
    plt.yticks(range(len(words)), words)
    plt.gca().invert_yaxis()
    plt.title('Top 20 Words in COVID-19 Paper Titles', fontsize=16, fontweight='bold')
    plt.xlabel('Frequency')
    plt.tight_layout()
    plt.savefig('top_words.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Visualization 4: Distribution of publications by source (journal)
# Show the long tail distribution
journal_counts = df_clean[df_clean['journal'] != 'Unknown']['journal'].value_counts()

plt.figure(figsize=(12, 6))
plt.hist(journal_counts.values, bins=50, color='#C73E1D', alpha=0.7, edgecolor='black')
plt.title('Distribution of Publications per Journal', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Number of Publications per Journal', fontsize=12)
plt.ylabel('Number of Journals', fontsize=12)
plt.yscale('log')  # Log scale to better see the distribution
plt.grid(True, alpha=0.3)

# Add some statistics to the plot
mean_pubs = journal_counts.mean()
median_pubs = journal_counts.median()
plt.axvline(mean_pubs, color='red', linestyle='--', label=f'Mean: {mean_pubs:.1f}')
plt.axvline(median_pubs, color='blue', linestyle='--', label=f'Median: {median_pubs:.1f}')
plt.legend()

plt.tight_layout()
plt.savefig('journal_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"\nJournal statistics: Mean={mean_pubs:.1f}, Median={median_pubs:.1f}")
print(f"Total unique journals: {len(journal_counts)}")

