import pandas as pd
import emoji
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from datetime import datetime
import re
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class EmojiAnalyzer:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
        self.emoji_data = None
        self.date_column = 'Message Date'
        self.text_column = 'Text'

    def load_data(self):
        """Load and prepare the CSV data"""
        try:
            # First, peek at the CSV headers
            header_df = pd.read_csv(self.csv_path, nrows=0)
            columns = header_df.columns

            # Verify required columns exist
            if self.date_column not in columns:
                print("Available columns:", list(columns))
                raise ValueError(f"Could not find '{self.date_column}' column.")

            if self.text_column not in columns:
                print("Available columns:", list(columns))
                raise ValueError(f"Could not find '{self.text_column}' column.")

            # Read the full CSV
            print(f"Reading CSV file...")
            self.df = pd.read_csv(self.csv_path, parse_dates=[self.date_column], low_memory=False)

            # Filter for 2024 messages and outgoing messages
            self.df = self.df[
                (self.df[self.date_column].dt.year == 2024) &
                (self.df['Type'] == 'Outgoing')
            ]

            print(f"Found {len(self.df):,} outgoing messages from 2024")

        except Exception as e:
            print(f"Error loading CSV file: {str(e)}")
            raise

    def extract_emojis(self, text):
        """Extract emojis from text"""
        if not isinstance(text, str):
            return []
        return [c for c in text if c in emoji.EMOJI_DATA]

    def process_emoji_data(self):
        """Process the data to extract emoji information"""
        print("Extracting emojis from messages...")
        # Extract emojis from each message
        self.df['emojis'] = self.df[self.text_column].apply(self.extract_emojis)
        self.df['emoji_count'] = self.df['emojis'].apply(len)

        # Create a DataFrame with one row per emoji
        print("Processing emoji data...")
        emoji_data = []
        for idx, row in self.df.iterrows():
            for emoji_char in row['emojis']:
                emoji_data.append({
                    'message_date': row[self.date_column],  # Use original column name
                    'emoji': emoji_char,
                    'hour': row[self.date_column].hour,
                    'day_of_week': row[self.date_column].day_name(),
                    'month': row[self.date_column].month_name()
                })
        self.emoji_data = pd.DataFrame(emoji_data)
        print(f"Found {len(emoji_data):,} emoji uses")

    def basic_stats(self):
        """Calculate basic emoji usage statistics"""
        total_emojis = self.df['emoji_count'].sum()
        unique_emojis = len(set([e for emojis in self.df['emojis'] for e in emojis]))
        messages_with_emojis = len(self.df[self.df['emoji_count'] > 0])

        print("\n=== Emoji Usage Statistics ===")
        print(f"Total emojis used: {total_emojis:,}")
        print(f"Unique emojis used: {unique_emojis:,}")
        print(f"Messages containing emojis: {messages_with_emojis:,}")
        print(f"Percentage of messages with emojis: {(messages_with_emojis/len(self.df)*100):.1f}%")

    def top_emojis(self, n=25):
        """Get the top n most frequently used emojis"""
        all_emojis = [e for emojis in self.df['emojis'] for e in emojis]
        return Counter(all_emojis).most_common(n)

    def plot_top_emojis(self, n=25):
        """Create an interactive bar chart of top emojis"""
        print(f"\nGenerating top {n} emojis visualization...")
        top_n = self.top_emojis(n)
        fig = px.bar(
            x=[e[0] for e in top_n],
            y=[e[1] for e in top_n],
            title=f"Top {n} Most Used Emojis",
            labels={'x': 'Emoji', 'y': 'Frequency'}
        )
        fig.show()

    def plot_time_patterns(self):
        """Create interactive plots for time-based patterns"""
        print("\nGenerating time pattern visualizations...")
        # Create subplots
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Hourly Usage', 'Daily Usage', 'Monthly Usage'),
            vertical_spacing=0.1
        )

        # Hourly patterns
        hourly = self.emoji_data.groupby('hour').size()
        fig.add_trace(
            go.Scatter(x=hourly.index, y=hourly.values, mode='lines+markers',
                      name='Hourly Usage'),
            row=1, col=1
        )

        # Daily patterns
        daily = self.emoji_data.groupby('day_of_week').size()
        # Reorder days to start with Monday
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                     'Friday', 'Saturday', 'Sunday']
        daily = daily.reindex(days_order)
        fig.add_trace(
            go.Bar(x=daily.index, y=daily.values, name='Daily Usage'),
            row=2, col=1
        )

        # Monthly patterns
        monthly = self.emoji_data.groupby('month').size()
        # Reorder months chronologically
        months_order = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        monthly = monthly.reindex(months_order)
        fig.add_trace(
            go.Bar(x=monthly.index, y=monthly.values, name='Monthly Usage'),
            row=3, col=1
        )

        fig.update_layout(height=900, showlegend=False,
                         title_text="Emoji Usage Patterns")
        fig.show()

    def plot_usage_over_time(self):
        """Create a line graph showing emoji usage over time"""
        print("\nGenerating usage over time visualization...")
        daily_counts = self.emoji_data.groupby('message_date').size().reset_index()
        fig = px.line(
            daily_counts,
            x='message_date',
            y=0,
            title='Emoji Usage Over Time',
            labels={'message_date': 'Date', '0': 'Number of Emojis'}
        )
        fig.show()

    def analyze_categories(self):
        """Analyze distribution of emoji categories"""
        print("\nAnalyzing emoji categories...")
        def get_emoji_category(emoji_char):
            return emoji.EMOJI_DATA[emoji_char].get('category', 'Unknown')

        self.emoji_data['category'] = self.emoji_data['emoji'].apply(get_emoji_category)
        category_counts = self.emoji_data['category'].value_counts()

        fig = px.pie(
            values=category_counts.values,
            names=category_counts.index,
            title='Distribution of Emoji Categories'
        )
        fig.show()

def main():
    # Update this path to point to your combined messages CSV file
    file_path = './messages/combined_messages.csv'

    # Create analyzer instance
    analyzer = EmojiAnalyzer(file_path)

    try:
        # Load and process data
        print("\nStarting emoji analysis...")
        analyzer.load_data()
        analyzer.process_emoji_data()

        # Generate analyses
        analyzer.basic_stats()
        analyzer.plot_top_emojis()
        analyzer.plot_time_patterns()
        analyzer.plot_usage_over_time()
        analyzer.analyze_categories()

        print("\nAnalysis complete! All visualizations should have opened in your browser.")

    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        print("Please check the error message above and ensure the CSV file is in the correct format.")
        raise

if __name__ == "__main__":
    main()
