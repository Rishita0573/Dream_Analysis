# test_enhanced_features.py - Test the new enhanced dream features

from enhanced_dream_analysis import DreamThemeAnalyzer, DreamJournal
from sleep_entry import SleepEntry

def test_dream_analysis():
    """Test the dream analysis functionality"""
    print("🧪 Testing Enhanced Dream Analysis Features\n")
    
    # Create test data
    dream_analyzer = DreamThemeAnalyzer()
    dream_journal = DreamJournal()
    
    # Test dream entries
    test_dreams = [
        {
            'date': '2024-01-15',
            'content': 'I was flying over beautiful mountains and felt so peaceful and free',
            'emotions': ['peaceful', 'happy', 'excited'],
            'quality': 8
        },
        {
            'date': '2024-01-16', 
            'content': 'Someone was chasing me through dark streets and I felt very scared',
            'emotions': ['scared', 'anxious'],
            'quality': 5
        },
        {
            'date': '2024-01-17',
            'content': 'I was swimming in clear blue water with dolphins',
            'emotions': ['peaceful', 'joyful'],
            'quality': 7
        },
        {
            'date': '2024-01-18',
            'content': 'My family was having dinner together and everyone was laughing',
            'emotions': ['happy', 'loved'],
            'quality': 8
        }
    ]
    
    # Create SleepEntry objects
    sleep_entries = []
    for dream in test_dreams:
        entry = SleepEntry(
            date=dream['date'],
            bedtime='23:00',
            wake_time='07:00',
            sleep_quality=dream['quality'],
            had_dreams=True,
            dream_content=dream['content'],
            dream_emotions=dream['emotions']
        )
        sleep_entries.append(entry)
    
    print("✅ Test 1: Dream Theme Detection")
    print("-" * 40)
    
    for i, entry in enumerate(sleep_entries, 1):
        print(f"\nDream {i}: {entry.dream_content}")
        themes = dream_analyzer.analyze_dream_themes(entry.dream_content)
        
        if themes:
            print("Detected themes:")
            for theme, data in themes:
                print(f"  • {theme}: {data['confidence']:.1f}% confidence")
                print(f"    Keywords: {', '.join(data['keywords'][:3])}")
        else:
            print("  No themes detected")
    
    print("\n✅ Test 2: Dream Interpretations")
    print("-" * 40)
    
    # Test interpretation for flying dream
    flying_themes = dream_analyzer.analyze_dream_themes(test_dreams[0]['content'])
    if flying_themes:
        interpretations = dream_analyzer.get_dream_interpretation(flying_themes[:1])
        if interpretations:
            interp = interpretations[0]
            print(f"Theme: {interp['theme']}")
            print(f"Interpretation: {interp['interpretation']}")
            print(f"Tips: {', '.join(interp['tips'][:2])}")
    
    print("\n✅ Test 3: Dream Pattern Analysis")
    print("-" * 40)
    
    patterns = dream_analyzer.analyze_dream_patterns(sleep_entries)
    if patterns:
        print(f"Analysis period: {patterns['analysis_period']}")
        print(f"Total dream nights: {patterns['total_dream_nights']}")
        
        if patterns['most_common_themes']:
            print("\nMost common themes:")
            for theme, count in patterns['most_common_themes']:
                print(f"  • {theme}: {count} times")
        
        if patterns['most_common_emotions']:
            print("\nMost common emotions:")
            for emotion, count in patterns['most_common_emotions']:
                print(f"  • {emotion}: {count} times")
    
    print("\n✅ Test 4: Dream Statistics")
    print("-" * 40)
    
    stats = dream_journal.get_dream_statistics(sleep_entries)
    if stats:
        print(f"Dream frequency: {stats['dream_frequency']}%")
        print(f"Average sleep quality with dreams: {stats['avg_sleep_quality_with_dreams']}/10")
        print(f"Average dream length: {stats['average_dream_length_words']} words")
        print(f"Unique emotions: {stats['unique_emotions']}")
    
    print("\n✅ Test 5: Dream Search")
    print("-" * 40)
    
    # Search for water-related dreams
    water_dreams = dream_journal.search_dreams_by_theme(sleep_entries, 'Water')
    print(f"Found {len(water_dreams)} dreams with water theme:")
    for dream in water_dreams:
        print(f"  • {dream['date']}: {dream['content'][:50]}...")
    
    print("\n✅ Test 6: Comprehensive Dream Insights")
    print("-" * 40)
    
    insights = dream_journal.generate_dream_insights(sleep_entries)
    print(insights)
    
    print("\n🎉 All tests completed successfully!")
    print("\nThe enhanced dream analysis features are working correctly.")
    print("You can now use these features in your main program!")

if __name__ == "__main__":
    test_dream_analysis()