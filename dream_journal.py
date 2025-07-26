# dream_journal.py - Dream Journal and Analysis

from collections import Counter, defaultdict
from datetime import datetime, timedelta
import re

class DreamJournal:
    def __init__(self):
        pass
    
    def get_dream_statistics(self, sleep_entries):
        """Calculate comprehensive dream statistics"""
        if not sleep_entries:
            return None
        
        dream_entries = [entry for entry in sleep_entries if entry.had_dreams]
        total_entries = len(sleep_entries)
        dream_nights = len(dream_entries)
        
        if dream_nights == 0:
            return {
                'total_nights': total_entries,
                'dream_nights': 0,
                'dream_frequency': 0,
                'average_dream_length_words': 0,
                'avg_sleep_quality_with_dreams': 0,
                'avg_sleep_quality_without_dreams': 0,
                'most_common_emotions': [],
                'total_emotions_recorded': 0,
                'unique_emotions': 0
            }
        
        # Basic statistics
        dream_frequency = (dream_nights / total_entries) * 100
        
        # Dream length analysis
        word_counts = []
        for entry in dream_entries:
            if entry.dream_content:
                word_count = len(entry.dream_content.split())
                word_counts.append(word_count)
        
        avg_dream_length = sum(word_counts) / len(word_counts) if word_counts else 0
        
        # Sleep quality comparison
        dream_sleep_qualities = [entry.sleep_quality for entry in dream_entries]
        no_dream_entries = [entry for entry in sleep_entries if not entry.had_dreams]
        no_dream_sleep_qualities = [entry.sleep_quality for entry in no_dream_entries]
        
        avg_sleep_with_dreams = sum(dream_sleep_qualities) / len(dream_sleep_qualities) if dream_sleep_qualities else 0
        avg_sleep_without_dreams = sum(no_dream_sleep_qualities) / len(no_dream_sleep_qualities) if no_dream_sleep_qualities else 0
        
        # Emotion analysis
        all_emotions = []
        for entry in dream_entries:
            if entry.dream_emotions:
                all_emotions.extend([emotion.lower().strip() for emotion in entry.dream_emotions])
        
        emotion_counter = Counter(all_emotions)
        most_common_emotions = emotion_counter.most_common(5)
        
        return {
            'total_nights': total_entries,
            'dream_nights': dream_nights,
            'dream_frequency': round(dream_frequency, 1),
            'average_dream_length_words': round(avg_dream_length, 1),
            'avg_sleep_quality_with_dreams': round(avg_sleep_with_dreams, 1),
            'avg_sleep_quality_without_dreams': round(avg_sleep_without_dreams, 1),
            'most_common_emotions': most_common_emotions,
            'total_emotions_recorded': len(all_emotions),
            'unique_emotions': len(set(all_emotions))
        }
    
    def search_dreams_by_theme(self, sleep_entries, theme):
        """Search dreams by specific theme"""
        from dream_analyzer import DreamThemeAnalyzer
        analyzer = DreamThemeAnalyzer()
        
        matching_dreams = []
        
        for entry in sleep_entries:
            if entry.had_dreams and entry.dream_content:
                themes = analyzer.analyze_dream_themes(entry.dream_content)
                
                # Check if the specified theme is in the detected themes
                for detected_theme, _ in themes:
                    if detected_theme.lower() == theme.lower():
                        matching_dreams.append({
                            'date': entry.date,
                            'content': entry.dream_content,
                            'emotions': entry.dream_emotions,
                            'sleep_quality': entry.sleep_quality
                        })
                        break
        
        return matching_dreams
    
    def generate_dream_insights(self, sleep_entries):
        """Generate comprehensive dream insights"""
        dream_entries = [entry for entry in sleep_entries if entry.had_dreams]
        
        if not dream_entries:
            return "No dream data available for analysis."
        
        insights = []
        insights.append("🌙 DREAM INSIGHTS REPORT")
        insights.append("=" * 50)
        
        # Recent dream activity
        recent_dreams = [entry for entry in sleep_entries[-30:] if entry.had_dreams]
        insights.append(f"\n📊 RECENT ACTIVITY (Last 30 days):")
        insights.append(f"Dreams recorded: {len(recent_dreams)}")
        
        if recent_dreams:
            avg_recent_quality = sum(entry.sleep_quality for entry in recent_dreams) / len(recent_dreams)
            insights.append(f"Average sleep quality with dreams: {avg_recent_quality:.1f}/10")
        
        # Dream frequency patterns
        dream_by_weekday = defaultdict(int)
        for entry in dream_entries:
            try:
                date_obj = datetime.strptime(entry.date, "%Y-%m-%d")
                weekday = date_obj.strftime("%A")
                dream_by_weekday[weekday] += 1
            except:
                continue
        
        if dream_by_weekday:
            most_common_day = max(dream_by_weekday, key=dream_by_weekday.get)
            insights.append(f"\n📅 DREAM PATTERNS:")
            insights.append(f"Most dreams occur on: {most_common_day}")
        
        # Emotional patterns
        all_emotions = []
        for entry in dream_entries:
            if entry.dream_emotions:
                all_emotions.extend([emotion.lower().strip() for emotion in entry.dream_emotions])
        
        if all_emotions:
            emotion_counter = Counter(all_emotions)
            top_emotion = emotion_counter.most_common(1)[0]
            insights.append(f"\n😊 EMOTIONAL PATTERNS:")
            insights.append(f"Most frequent dream emotion: {top_emotion[0].title()} ({top_emotion[1]} times)")
        
        # Sleep quality correlation
        if len(dream_entries) >= 5:
            high_quality_dreams = [entry for entry in dream_entries if entry.sleep_quality >= 8]
            low_quality_dreams = [entry for entry in dream_entries if entry.sleep_quality <= 5]
            
            insights.append(f"\n💤 SLEEP QUALITY INSIGHTS:")
            insights.append(f"Dreams with high sleep quality (8+): {len(high_quality_dreams)}")
            insights.append(f"Dreams with low sleep quality (≤5): {len(low_quality_dreams)}")
        
        # Content analysis
        total_words = sum(len(entry.dream_content.split()) for entry in dream_entries if entry.dream_content)
        avg_length = total_words / len(dream_entries) if dream_entries else 0
        
        insights.append(f"\n📝 CONTENT ANALYSIS:")
        insights.append(f"Average dream description length: {avg_length:.1f} words")
        insights.append(f"Total dream content recorded: {total_words} words")
        
        # Recommendations
        insights.append(f"\n💡 PERSONALIZED RECOMMENDATIONS:")
        
        if recent_dreams:
            recent_avg = sum(entry.sleep_quality for entry in recent_dreams) / len(recent_dreams)
            if recent_avg < 6:
                insights.append("• Consider improving sleep hygiene for better dream recall")
            elif recent_avg > 8:
                insights.append("• Great sleep quality! Your dreams are well-remembered")
        
        if len(set(all_emotions)) > 5:
            insights.append("• You experience diverse emotions in dreams - sign of active subconscious processing")
        
        if avg_length > 50:
            insights.append("• You provide detailed dream descriptions - excellent for pattern analysis!")
        
        return "\n".join(insights)
    
    def get_dream_trends(self, sleep_entries, days=30):
        """Analyze dream trends over specified period"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        recent_entries = []
        for entry in sleep_entries:
            try:
                entry_date = datetime.strptime(entry.date, "%Y-%m-%d")
                if entry_date >= cutoff_date and entry.had_dreams:
                    recent_entries.append(entry)
            except:
                continue
        
        if not recent_entries:
            return None
        
        # Calculate trends
        weekly_dreams = defaultdict(int)
        for entry in recent_entries:
            entry_date = datetime.strptime(entry.date, "%Y-%m-%d")
            week = entry_date.strftime("%Y-W%U")
            weekly_dreams[week] += 1
        
        # Emotion trends
        recent_emotions = []
        for entry in recent_entries:
            if entry.dream_emotions:
                recent_emotions.extend([emotion.lower().strip() for emotion in entry.dream_emotions])
        
        emotion_trends = Counter(recent_emotions).most_common(3)
        
        return {
            'period_days': days,
            'total_dreams': len(recent_entries),
            'weekly_average': sum(weekly_dreams.values()) / len(weekly_dreams) if weekly_dreams else 0,
            'top_emotions': emotion_trends,
            'avg_sleep_quality': sum(entry.sleep_quality for entry in recent_entries) / len(recent_entries)
        }