# enhanced_dream_analysis.py - Advanced Dream Analysis Features

import re
from collections import Counter
from datetime import datetime, timedelta
from utils import timing_decorator, create_simple_chart

class DreamThemeAnalyzer:
    """Advanced dream theme detection and analysis"""
    
    def __init__(self):
        # Predefined dream themes with keywords
        self.dream_themes = {
            'Flying': ['fly', 'flying', 'soar', 'floating', 'levitate', 'wings', 'air', 'sky', 'clouds'],
            'Falling': ['fall', 'falling', 'drop', 'dropped', 'cliff', 'height', 'tumble', 'plunge'],
            'Chase': ['chase', 'chased', 'running', 'pursue', 'escape', 'flee', 'hunt', 'follow'],
            'Water': ['water', 'ocean', 'sea', 'river', 'lake', 'pool', 'swimming', 'drowning', 'waves'],
            'Animals': ['dog', 'cat', 'snake', 'bird', 'lion', 'tiger', 'elephant', 'horse', 'animal'],
            'Family': ['mother', 'father', 'mom', 'dad', 'sister', 'brother', 'family', 'relative'],
            'School/Work': ['school', 'teacher', 'exam', 'test', 'office', 'work', 'boss', 'meeting'],
            'Death': ['death', 'die', 'dead', 'funeral', 'grave', 'ghost', 'spirit', 'cemetery'],
            'Love/Romance': ['love', 'kiss', 'romance', 'boyfriend', 'girlfriend', 'wedding', 'date'],
            'Travel': ['travel', 'journey', 'trip', 'vacation', 'foreign', 'country', 'airport', 'train'],
            'House/Home': ['house', 'home', 'room', 'kitchen', 'bedroom', 'bathroom', 'stairs', 'door'],
            'Money': ['money', 'rich', 'poor', 'lottery', 'gold', 'treasure', 'bank', 'pay', 'buy'],
            'Food': ['food', 'eat', 'eating', 'hungry', 'restaurant', 'cooking', 'meal', 'dinner'],
            'Vehicle': ['car', 'bus', 'train', 'plane', 'bike', 'motorcycle', 'driving', 'crash'],
            'Nature': ['forest', 'mountain', 'tree', 'flower', 'garden', 'field', 'valley', 'desert'],
            'Technology': ['phone', 'computer', 'internet', 'robot', 'machine', 'gadget', 'screen'],
            'Violence': ['fight', 'fighting', 'war', 'weapon', 'gun', 'knife', 'blood', 'attack'],
            'Supernatural': ['magic', 'wizard', 'witch', 'demon', 'angel', 'ghost', 'spirit', 'power']
        }
        
        # Dream interpretations based on psychology
        self.theme_interpretations = {
            'Flying': "Often represents freedom, ambition, or desire to rise above current circumstances. May indicate confidence and control over life situations.",
            'Falling': "Usually reflects feelings of anxiety, loss of control, or fear of failure. May indicate stress about a situation in waking life.",
            'Chase': "Often represents avoidance of something in waking life. May indicate running from responsibilities, fears, or unresolved issues.",
            'Water': "Symbolizes emotions, subconscious mind, and purification. Clear water suggests peace, while turbulent water may indicate emotional turmoil.",
            'Animals': "Represents instincts, desires, and untamed aspects of personality. Different animals have specific symbolic meanings.",
            'Family': "Reflects relationships, family dynamics, and unresolved family issues. May indicate need for connection or healing.",
            'School/Work': "Often represents feelings of being tested or judged in waking life. May indicate anxiety about performance or competence.",
            'Death': "Rarely literal; usually represents transformation, end of a life phase, or fear of change. Often indicates personal growth.",
            'Love/Romance': "Reflects desires for intimacy, connection, or relationship concerns. May indicate longing or relationship satisfaction.",
            'Travel': "Represents life journey, personal growth, or desire for change. May indicate seeking new experiences or escape.",
            'House/Home': "Symbolizes the self, psyche, and different aspects of personality. Different rooms represent different aspects of life.",
            'Money': "Often represents self-worth, power, or security concerns. May indicate financial stress or desire for abundance.",
            'Food': "Represents nourishment, both physical and emotional. May indicate hunger for love, knowledge, or spiritual fulfillment.",
            'Vehicle': "Represents direction in life and level of control. The condition and control of the vehicle reflects life management.",
            'Nature': "Connects to natural instincts, growth, and harmony. Often indicates need for grounding or connection with natural self.",
            'Technology': "Reflects relationship with modern world, communication issues, or feeling overwhelmed by rapid changes.",
            'Violence': "May represent internal conflict, suppressed anger, or external pressures. Often indicates need to address aggressive feelings.",
            'Supernatural': "Represents hidden abilities, spiritual growth, or connection to unconscious mind. May indicate psychic awareness."
        }
        
        # Tips based on dream patterns
        self.theme_tips = {
            'Flying': ["Practice meditation to enhance sense of control", "Set ambitious but realistic goals", "Embrace your leadership abilities"],
            'Falling': ["Practice stress reduction techniques", "Address anxiety-causing situations", "Build confidence through small achievements"],
            'Chase': ["Identify what you're avoiding in waking life", "Face challenges directly", "Practice courage-building exercises"],
            'Water': ["Pay attention to your emotional health", "Practice emotional regulation techniques", "Consider journaling feelings"],
            'Animals': ["Connect with your instinctual nature", "Explore creative outlets", "Consider what the specific animal represents"],
            'Family': ["Strengthen family relationships", "Address unresolved family issues", "Practice forgiveness and understanding"],
            'School/Work': ["Prepare thoroughly for upcoming challenges", "Build confidence in your abilities", "Reduce performance anxiety"],
            'Death': ["Embrace change and transformation", "Let go of old patterns", "Focus on personal growth"],
            'Love/Romance': ["Nurture existing relationships", "Be open to new connections", "Practice self-love"],
            'Travel': ["Plan a real trip or adventure", "Explore new interests", "Embrace change and growth"],
            'House/Home': ["Focus on self-improvement", "Create a peaceful living space", "Explore different aspects of personality"],
            'Money': ["Address financial concerns", "Focus on building self-worth", "Practice gratitude for what you have"],
            'Food': ["Nourish yourself physically and emotionally", "Explore what you're 'hungry' for in life", "Practice mindful eating"],
            'Vehicle': ["Take control of your life direction", "Make important decisions", "Focus on goal achievement"],
            'Nature': ["Spend more time outdoors", "Connect with natural rhythms", "Practice grounding exercises"],
            'Technology': ["Balance screen time with real-world activities", "Improve communication skills", "Embrace helpful technology"],
            'Violence': ["Address anger or frustration constructively", "Practice conflict resolution", "Consider counseling if needed"],
            'Supernatural': ["Explore spiritual practices", "Trust your intuition", "Develop psychic or creative abilities"]
        }
    
    @timing_decorator
    def analyze_dream_themes(self, dream_content):
        """Analyze dream content and identify themes"""
        if not dream_content:
            return []
        
        dream_text = dream_content.lower()
        detected_themes = []
        theme_scores = {}
        
        # Count keyword matches for each theme
        for theme, keywords in self.dream_themes.items():
            score = 0
            matched_keywords = []
            
            for keyword in keywords:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = len(re.findall(pattern, dream_text))
                if matches > 0:
                    score += matches
                    matched_keywords.extend([keyword] * matches)
            
            if score > 0:
                theme_scores[theme] = {
                    'score': score,
                    'keywords': matched_keywords,
                    'confidence': min(score * 20, 100)  # Convert to percentage
                }
        
        # Sort themes by score (most relevant first)
        sorted_themes = sorted(theme_scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        return sorted_themes
    
    def get_dream_interpretation(self, themes):
        """Get interpretations for detected themes"""
        interpretations = []
        
        for theme, data in themes:
            interpretation = {
                'theme': theme,
                'confidence': data['confidence'],
                'keywords_found': data['keywords'],
                'interpretation': self.theme_interpretations.get(theme, "No interpretation available"),
                'tips': self.theme_tips.get(theme, ["Continue exploring this theme"])
            }
            interpretations.append(interpretation)
        
        return interpretations
    
    def analyze_dream_patterns(self, dream_entries, days_back=30):
        """Analyze dream patterns over time"""
        if not dream_entries:
            return {}
        
        # Filter recent dreams
        cutoff_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        recent_dreams = [entry for entry in dream_entries 
                        if entry.had_dreams and entry.date >= cutoff_date]
        
        if not recent_dreams:
            return {}
        
        # Analyze all dreams for patterns
        all_themes = []
        theme_by_date = {}
        emotion_patterns = Counter()
        
        for entry in recent_dreams:
            themes = self.analyze_dream_themes(entry.dream_content)
            
            # Track themes over time
            theme_by_date[entry.date] = [theme for theme, _ in themes]
            all_themes.extend([theme for theme, _ in themes])
            
            # Track emotions
            if entry.dream_emotions:
                emotion_patterns.update(entry.dream_emotions)
        
        # Find recurring themes
        theme_frequency = Counter(all_themes)
        
        # Calculate patterns
        patterns = {
            'total_dream_nights': len(recent_dreams),
            'most_common_themes': theme_frequency.most_common(5),
            'most_common_emotions': emotion_patterns.most_common(5),
            'theme_frequency': dict(theme_frequency),
            'dreams_by_date': theme_by_date,
            'analysis_period': f"Last {days_back} days"
        }
        
        return patterns

class DreamJournal:
    """Enhanced dream journal with advanced features"""
    
    def __init__(self):
        self.theme_analyzer = DreamThemeAnalyzer()
        self.dream_logs = []
    
    def create_detailed_dream_log(self, sleep_entry):
        """Create detailed dream log with analysis"""
        if not sleep_entry.had_dreams:
            return None
        
        # Analyze themes
        themes = self.theme_analyzer.analyze_dream_themes(sleep_entry.dream_content)
        interpretations = self.theme_analyzer.get_dream_interpretation(themes)
        
        dream_log = {
            'date': sleep_entry.date,
            'dream_content': sleep_entry.dream_content,
            'emotions': sleep_entry.dream_emotions,
            'sleep_quality': sleep_entry.sleep_quality,
            'detected_themes': themes,
            'interpretations': interpretations,
            'analysis_timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return dream_log
    
    def generate_dream_insights(self, dream_entries):
        """Generate comprehensive dream insights"""
        if not any(entry.had_dreams for entry in dream_entries):
            return "No dreams recorded for analysis."
        
        patterns = self.theme_analyzer.analyze_dream_patterns(dream_entries)
        
        if not patterns:
            return "Insufficient dream data for pattern analysis."
        
        insights = []
        
        # Theme analysis
        if patterns['most_common_themes']:
            insights.append("🎭 RECURRING DREAM THEMES:")
            for theme, count in patterns['most_common_themes']:
                percentage = (count / patterns['total_dream_nights']) * 100
                insights.append(f"   • {theme}: {count} times ({percentage:.1f}% of dreams)")
        
        # Emotion analysis  
        if patterns['most_common_emotions']:
            insights.append("\n😊 COMMON DREAM EMOTIONS:")
            for emotion, count in patterns['most_common_emotions']:
                insights.append(f"   • {emotion.title()}: {count} occurrences")
        
        # Recommendations based on patterns
        insights.append("\n💡 PERSONALIZED DREAM RECOMMENDATIONS:")
        
        dominant_themes = [theme for theme, _ in patterns['most_common_themes'][:3]]
        recommendations = set()
        
        for theme in dominant_themes:
            theme_tips = self.theme_analyzer.theme_tips.get(theme, [])
            recommendations.update(theme_tips[:2])  # Add top 2 tips per theme
        
        for i, rec in enumerate(list(recommendations)[:5], 1):
            insights.append(f"   {i}. {rec}")
        
        return "\n".join(insights)
    
    def search_dreams_by_theme(self, dream_entries, target_theme):
        """Search dreams by specific theme"""
        matching_dreams = []
        
        for entry in dream_entries:
            if entry.had_dreams:
                themes = self.theme_analyzer.analyze_dream_themes(entry.dream_content)
                theme_names = [theme for theme, _ in themes]
                
                if target_theme in theme_names:
                    matching_dreams.append({
                        'date': entry.date,
                        'content': entry.dream_content,
                        'emotions': entry.dream_emotions,
                        'sleep_quality': entry.sleep_quality
                    })
        
        return matching_dreams
    
    def get_dream_statistics(self, dream_entries):
        """Get comprehensive dream statistics"""
        if not dream_entries:
            return {}
        
        total_nights = len(dream_entries)
        dream_nights = sum(1 for entry in dream_entries if entry.had_dreams)
        
        if dream_nights == 0:
            return {'total_nights': total_nights, 'dream_nights': 0, 'dream_frequency': 0}
        
        # Calculate statistics
        dream_frequency = (dream_nights / total_nights) * 100
        
        # Average sleep quality on dream vs non-dream nights
        dream_sleep_quality = [entry.sleep_quality for entry in dream_entries if entry.had_dreams]
        no_dream_sleep_quality = [entry.sleep_quality for entry in dream_entries if not entry.had_dreams]
        
        avg_dream_quality = sum(dream_sleep_quality) / len(dream_sleep_quality) if dream_sleep_quality else 0
        avg_no_dream_quality = sum(no_dream_sleep_quality) / len(no_dream_sleep_quality) if no_dream_sleep_quality else 0
        
        # Emotion analysis
        all_emotions = []
        for entry in dream_entries:
            if entry.had_dreams and entry.dream_emotions:
                all_emotions.extend(entry.dream_emotions)
        
        emotion_stats = Counter(all_emotions)
        
        # Dream length analysis
        dream_lengths = [len(entry.dream_content.split()) for entry in dream_entries 
                        if entry.had_dreams and entry.dream_content]
        avg_dream_length = sum(dream_lengths) / len(dream_lengths) if dream_lengths else 0
        
        return {
            'total_nights': total_nights,
            'dream_nights': dream_nights,
            'dream_frequency': round(dream_frequency, 1),
            'avg_sleep_quality_with_dreams': round(avg_dream_quality, 1),
            'avg_sleep_quality_without_dreams': round(avg_no_dream_quality, 1),
            'most_common_emotions': emotion_stats.most_common(5),
            'average_dream_length_words': round(avg_dream_length, 1),
            'total_emotions_recorded': len(all_emotions),
            'unique_emotions': len(set(all_emotions))
        }

# Generator for dream-specific data processing
def dream_entries_by_theme(dream_entries, theme_analyzer, target_theme):
    """Generator that yields dreams matching a specific theme"""
    for entry in dream_entries:
        if entry.had_dreams:
            themes = theme_analyzer.analyze_dream_themes(entry.dream_content)
            theme_names = [theme for theme, _ in themes]
            
            if target_theme in theme_names:
                yield entry

def dreams_by_emotion(dream_entries, target_emotion):
    """Generator that yields dreams with specific emotion"""
    target_emotion = target_emotion.lower()
    for entry in dream_entries:
        if entry.had_dreams and entry.dream_emotions:
            emotions = [emotion.lower() for emotion in entry.dream_emotions]
            if target_emotion in emotions:
                yield entry

# Iterator for processing dream patterns
class DreamPatternIterator:
    """Iterator for analyzing dream patterns over time"""
    
    def __init__(self, dream_entries, window_size=7):
        self.dream_entries = [entry for entry in dream_entries if entry.had_dreams]
        self.window_size = window_size
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index + self.window_size > len(self.dream_entries):
            raise StopIteration
        
        window = self.dream_entries[self.index:self.index + self.window_size]
        self.index += 1
        return window

# Decorator for dream analysis functions
def dream_analysis_logger(func):
    """Decorator to log dream analysis activities"""
    def wrapper(*args, **kwargs):
        print(f"🌙 Analyzing dreams with {func.__name__}...")
        start_time = datetime.now()
        
        result = func(*args, **kwargs)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        print(f"✨ Dream analysis completed in {duration:.2f} seconds")
        
        return result
    return wrapper

# Closure for creating dream filters
def create_dream_filter(criteria):
    """Create a dream filter based on criteria"""
    def filter_dreams(dream_entries):
        filtered = []
        for entry in dream_entries:
            if not entry.had_dreams:
                continue
                
            match = True
            
            if 'min_quality' in criteria:
                if entry.sleep_quality < criteria['min_quality']:
                    match = False
            
            if 'emotions' in criteria:
                if not any(emotion.lower() in [e.lower() for e in entry.dream_emotions] 
                          for emotion in criteria['emotions']):
                    match = False
            
            if 'keywords' in criteria:
                content_lower = entry.dream_content.lower()
                if not any(keyword.lower() in content_lower for keyword in criteria['keywords']):
                    match = False
            
            if match:
                filtered.append(entry)
        
        return filtered
    
    return filter_dreams