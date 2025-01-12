# Emoji Wrapped 🎧

A Python tool to analyze and visualize your emoji usage patterns from iMessage conversations.

## Overview

This tool helps you analyze your emoji usage patterns from iMessage conversations by processing exported message data. It provides insights and visualizations for:
- Most frequently used emojis
- Time-based usage patterns (hourly, daily, monthly)
- Emoji category distribution
- Usage trends over time

## Prerequisites

1. Export your iMessage data using [iMazing](https://imazing.com/)
2. Python 3.x
3. Required Python packages:
```bash
pip install pandas emoji matplotlib seaborn plotly
```

## Setup

1. Export your iMessage data using iMazing
2. Combine the exported CSV files into a single file
3. Clone this repository:
```bash
git clone https://github.com/abelinkinbio/emoji-wrapped
cd emoji-wrapped
```

4. Update the file path in `emoji_wrapped.py` to point to your combined CSV file

## Usage

Run the analysis:
```bash
python emoji_wrapped.py
```

The script will generate interactive visualizations in your default web browser and print basic statistics to the console.

## Features

- 📊 Interactive visualizations using Plotly
- 🕒 Temporal analysis of emoji usage
- 📈 Usage trends and patterns
- 🔍 Category-based analysis

## CSV Format

The script expects a CSV file with the following columns:
- Message Date (to filter by year)
- Text (to view texts with emoji usage)
- Type (to identify outgoing messages)

## Contributing

Contributions welcome! Feel free to submit issues or pull requests.

Some ideas for improvements:
- Add more visualization types
- Include sentiment analysis w/ Workers AI
- Add support for different export formats
- Add conversation-specific analysis
- Include reply/reaction analysis

## License

MIT License - feel free to use and modify as needed.
