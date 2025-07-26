# Dream_Journel
Advanced Sleep Analytics Platform with Dream Analysis

A Python-based sleep tracking application that helps analyze sleep patterns and dream content.

## What it does

This app lets you track your sleep data, record dreams, and see patterns over time. I built it to understand my own sleep better and experiment with text analysis for dream themes.

## Features

- Track sleep quality, bedtime, wake time
- Record and analyze dreams with automatic theme detection
- Performance metrics (mood, energy, productivity)
- Search through your dream entries by keywords, emotions, dates
- Generate comprehensive reports showing correlations between sleep and performance
- Dream statistics and trend analysis
- Automatic backup of your data

## Dream Analysis

The app can detect common dream themes like:
- Flying, falling, being chased
- Water, animals, houses
- School/exam scenarios
- Vehicles, money, food
- Pregnancy/birth, nakedness, fire
- And several others

It uses keyword matching to identify themes and provides psychological interpretations with personalized tips.

## Advanced Features

- **Multi-criteria search**: Find dreams by theme, emotion, sleep quality, or date range
- **Statistical analysis**: Dream frequency patterns, emotion correlation, sleep quality trends
- **Theme explorer**: Browse dreams by specific psychological themes
- **Comprehensive statistics**: Detailed analytics on your sleep and dream patterns
- **Performance correlation**: See how sleep affects your daily productivity and mood
- **Dream insights**: Automatic generation of personalized recommendations

## How to use

1. Download all the files
2. Run `python main.py`
3. Start with option 1 to record sleep data
4. Use the menu to explore different features:
   - Options 1-6: Basic sleep and performance tracking
   - Options 7-10: Advanced dream analysis features
   - Option 11: Backup your data

The app creates a `data/` folder to store your information locally.

## File Structure

```
sleep-analytics-platform/
├── main.py              # Main application with menu system
├── sleep_entry.py       # Data models for sleep and performance entries
├── dream_journal.py     # Dream statistics and insights generation
├── dream_analyzer.py    # Theme detection and pattern analysis
├── file_handler.py      # Data persistence and backup system
├── reports.py           # Comprehensive report generation
├── utils.py             # Helper functions and input validation
└── data/               # Created automatically
    ├── sleep_data.json
    ├── performance_data.json
    └── reports/
```

## Sample Output

When you record a dream, the app immediately analyzes it:

```
🌙 Analyzing your dream...

🎭 Detected Dream Themes:
   • Flying (Confidence: 85.2%)
   • Freedom (Confidence: 72.1%)

💡 Theme Insight: Flying dreams often represent freedom, ambition, and desire to rise above limitations.
💭 Suggestion: Consider what areas of your life you want more freedom in
```

## Menu Options

The application offers 12 different features:
1. Record Sleep Data (with dream analysis)
2. Record Performance Data  
3. View Sleep History
4. View Performance History
5. Generate Analysis Report
6. View Correlations
7. 🌙 Advanced Dream Analysis
8. 🎭 Dream Theme Explorer  
9. 🔍 Search Dreams
10. 📊 Dream Statistics
11. Backup Data
12. Exit

## Requirements

Just Python 3.x - no external libraries needed.

## Data Privacy

All data stays on your computer - nothing gets sent anywhere. The app works completely offline and includes automatic backup functionality.

## Notes

This was a personal project to learn more about data analysis and improve my Python skills. The dream analysis turned out to be pretty interesting - it can actually spot meaningful patterns in your sleep data over time.
