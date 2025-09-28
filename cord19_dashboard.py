import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
from datetime import datetime
import numpy as np

#Read cleaned data
df_clean = pd.read_csv('cord19_metadata_cleaned.csv')
# Page configuration - must be first Streamlit command
st.set_page_config(
    page_title="CORD-19 Research Dashboard",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .section-header {
        color: #1f77b4;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the cleaned dataset"""
    try:
        df_clean = pd.read_csv('cord19_metadata_cleaned.csv')
        df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'])
        return df_clean
    except FileNotFoundError:
        st.error("❌ Cleaned dataset not found. Please run the data cleaning script first.")
        return None

def main():
    # Header with creative title
    st.markdown('<h1 class="main-header">🔬 CORD-19 Research Explorer</h1>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    Welcome to the interactive dashboard for exploring COVID-19 research trends from the CORD-19 dataset. 
    This tool allows you to analyze publication patterns, journal distributions, and research focus areas.
    """)
    
    # Load data with progress indicator
    with st.spinner('Loading research data...'):
        df_clean = load_data()
    
    if df_clean is None:
        return
    
    # Sidebar for filters and controls
    st.sidebar.title("🔍 Filter Controls")
    st.sidebar.markdown("Customize the data view using the filters below:")
    
    # Year range slider
    years = sorted(df_clean['publication_year'].unique())
    year_range = st.sidebar.slider(
        "Select Publication Year Range",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=(int(min(years)), int(max(years)))
    )
    
    # Journal selection
    journals = ['All'] + sorted(df_clean[df_clean['journal'] != 'Unknown']['journal'].unique().tolist())
    selected_journal = st.sidebar.selectbox("Filter by Journal", journals)
    
    # Minimum word count filter
    min_words = st.sidebar.slider("Minimum Abstract Word Count", 0, 500, 50)
    
    # Apply filters
    filtered_df_clean = df_clean[
        (df_clean['publication_year'] >= year_range[0]) & 
        (df_clean['publication_year'] <= year_range[1]) &
        (df_clean['abstract_word_count'] >= min_words)
    ]
    
    if selected_journal != 'All':
        filtered_df_clean = filtered_df_clean[filtered_df_clean['journal'] == selected_journal]
    
    # Key metrics cards
    st.markdown("### 📊 Overview Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Papers", f"{len(filtered_df_clean):,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Unique Journals", f"{filtered_df_clean['journal'].nunique():,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avg_authors = filtered_df_clean['author_count'].mean()
        st.metric("Avg Authors/Paper", f"{avg_authors:.1f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avg_words = filtered_df_clean['abstract_word_count'].mean()
        st.metric("Avg Abstract Length", f"{avg_words:.0f} words")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🏢 Journals", "📝 Content Analysis", "🔍 Data Explorer"])
    
    with tab1:
        st.markdown('<h3 class="section-header">Publication Trends Over Time</h3>', unsafe_allow_html=True)
        
        # Time series analysis
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Monthly publications chart
            monthly_data = filtered_df_clean.groupby(pd.Grouper(key='publish_time', freq='M')).size()
            
            fig, ax = plt.subplots(figsize=(10, 4))
            monthly_data.plot(kind='line', ax=ax, color='#1f77b4', linewidth=2)
            ax.set_title('Monthly Publications Trend', fontweight='bold')
            ax.set_xlabel('Date')
            ax.set_ylabel('Number of Publications')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            st.pyplot(fig)
        
        with col2:
            # Yearly breakdown
            yearly_data = filtered_df_clean['publication_year'].value_counts().sort_index()
            st.write("**Yearly Breakdown:**")
            for year, count in yearly_data.items():
                st.write(f"{year}: {count:,} papers")
            
            if len(yearly_data) > 1:
                growth = ((yearly_data.iloc[-1] - yearly_data.iloc[0]) / yearly_data.iloc[0]) * 100
                st.metric("Growth Rate", f"{growth:+.1f}%")
    
    with tab2:
        st.markdown('<h3 class="section-header">Journal Analysis</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Top journals chart
            top_journals = filtered_df_clean[filtered_df_clean['journal'] != 'Unknown']['journal'].value_counts().head(10)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            top_journals.plot(kind='barh', ax=ax, color='#2ca02c')
            ax.set_title('Top 10 Journals by Publication Count', fontweight='bold')
            ax.set_xlabel('Number of Publications')
            plt.gca().invert_yaxis()
            st.pyplot(fig)
        
        with col2:
            # Journal statistics
            journal_stats = filtered_df_clean[filtered_df_clean['journal'] != 'Unknown']['journal'].value_counts()
            st.write("**Journal Statistics:**")
            st.write(f"Total journals: {len(journal_stats):,}")
            st.write(f"Top journal: **{journal_stats.index[0]}** ({journal_stats.iloc[0]:,} papers)")
            st.write(f"Median papers per journal: {journal_stats.median():.1f}")
            
            # Journal concentration
            top_10_share = (journal_stats.head(10).sum() / journal_stats.sum()) * 100
            st.write(f"Top 10 journals account for: **{top_10_share:.1f}%** of publications")
    
    with tab3:
        st.markdown('<h3 class="section-header">Research Content Analysis</h3>', unsafe_allow_html=True)
        
        # Word frequency analysis
        if not filtered_df_clean.empty:
            all_titles = ' '.join(filtered_df_clean['title'].dropna().astype(str))
            words = re.findall(r'\b[a-zA-Z]{4,}\b', all_titles.lower())
            
            stop_words = {'this', 'that', 'with', 'from', 'have', 'has', 'been', 'during', 
                         'study', 'analysis', 'research', 'using', 'based', 'among', 'covid'}
            filtered_words = [word for word in words if word not in stop_words]
            word_freq = Counter(filtered_words).most_common(15)
            
            # Create word frequency chart
            words, counts = zip(*word_freq)
            
            fig, ax = plt.subplots(figsize=(10, 6))
            y_pos = np.arange(len(words))
            ax.barh(y_pos, counts, color='#ff7f0e')
            ax.set_yticks(y_pos)
            ax.set_yticklabels(words)
            ax.invert_yaxis()
            ax.set_title('Top 15 Words in Paper Titles', fontweight='bold')
            ax.set_xlabel('Frequency')
            st.pyplot(fig)
            
            st.write("**Most Common Research Themes:**")
            for i, (word, count) in enumerate(word_freq[:5], 1):
                st.write(f"{i}. **{word}** (appears {count} times)")
    
    with tab4:
        st.markdown('<h3 class="section-header">Data Explorer</h3>', unsafe_allow_html=True)
        
        # Data sample with search
        st.write(f"Showing {len(filtered_df_clean):,} papers matching your filters")
        
        # Search functionality
        search_term = st.text_input("🔍 Search in titles and abstracts:")
        if search_term:
            search_df_clean = filtered_df_clean[
                filtered_df_clean['title'].str.contains(search_term, case=False, na=False) |
                filtered_df_clean['abstract'].str.contains(search_term, case=False, na=False)
            ]
        else:
            search_df_clean = filtered_df_clean
        
        # Display sample data
        sample_size = st.slider("Sample size to display", 5, 100, 10)
        st.dataframe(
            search_df_clean[['title', 'journal', 'publish_time', 'authors']].head(sample_size),
            use_container_width=True
        )
        
        # Data download option
        csv = search_df_clean.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f"cord19_filtered_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown(
        "**Data Source**: CORvidD-19 Dataset | "
        "**Last Updated**: " + datetime.now().strftime("%Y-%m-%d") + " | "
        "Built by Abihud using Streamlit"
    )

if __name__ == "__main__":
    main()