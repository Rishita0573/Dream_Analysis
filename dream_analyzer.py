# dream_analyzer.py - Dream Theme Analysis and Interpretation

import re
from collections import Counter, defaultdict
from datetime import datetime

class DreamThemeAnalyzer:
    def __init__(self):
        # Define dream themes with their associated keywords
        self.dream_themes = {
            "Flying": {
                "keywords": ["fly", "flying", "soar", "wings", "air", "floating", "levitate", "hover"],
                "interpretation": "Flying dreams often represent freedom, ambition, and desire to rise above limitations.",
                "tips": [
                    "Consider what areas of your life you want more freedom in",
                    "Flying dreams may indicate you're ready to overcome obstacles",
                    "Notice if you're in control while flying - this reflects confidence levels"
                ]
            },
            "Falling": {
                "keywords": ["fall", "falling", "drop", "tumble", "plunge", "crash", "cliff"],
                "interpretation": "Falling dreams typically symbolize feelings of losing control or anxiety about failure.",
                "tips": [
                    "Examine areas where you feel out of control in waking life",
                    "Practice stress-reduction techniques before bed",
                    "Consider what fears you might need to address"
                ]
            },
            "Chase": {
                "keywords": ["chase", "chasing", "pursue", "run", "running", "escape", "hunt", "follow"],
                "interpretation": "Being chased often represents avoiding something in your waking life.",
                "tips": [
                    "Think about what you might be avoiding or running from",
                    "Consider facing challenges directly rather than avoiding them",
                    "Identify the source of stress or anxiety in your life"
                ]
            },
            "Water": {
                "keywords": ["water", "ocean", "sea", "river", "lake", "swimming", "drowning", "waves", "flood"],
                "interpretation": "Water dreams relate to emotions, subconscious thoughts, and life transitions.",
                "tips": [
                    "Pay attention to the water's condition - calm or turbulent",
                    "Consider your current emotional state and relationships",
                    "Water dreams may signal need for emotional cleansing"
                ]
            },
            "Animals": {
                "keywords": ["dog", "cat", "horse", "bird", "snake", "lion", "tiger", "bear", "wolf", "animal"],
                "interpretation": "Animals in dreams often represent instincts, desires, or aspects of personality.",
                "tips": [
                    "Consider what the specific animal represents to you",
                    "Think about your relationship with your instincts",
                    "Animals may represent people or traits in your life"
                ]
            },
            "Death": {
                "keywords": ["death", "dying", "dead", "funeral", "grave", "cemetery", "corpse"],
                "interpretation": "Death dreams usually symbolize endings, transformations, or new beginnings.",
                "tips": [
                    "Consider what in your life is ending or changing",
                    "Death dreams often represent personal growth",
                    "Think about what new phase you're entering"
                ]
            },
            "School/Exam": {
                "keywords": ["school", "exam", "test", "classroom", "teacher", "student", "homework", "study"],
                "interpretation": "School dreams often reflect feelings of being judged or tested in life.",
                "tips": [
                    "Consider areas where you feel evaluated or judged",
                    "Think about skills or knowledge you want to develop",
                    "May indicate imposter syndrome or performance anxiety"
                ]
            },
            "House/Home": {
                "keywords": ["house", "home", "room", "door", "window", "stairs", "basement", "attic"],
                "interpretation": "Houses represent the self, with different rooms symbolizing different aspects of personality.",
                "tips": [
                    "Pay attention to which rooms appear in your dreams",
                    "Consider the condition of the house - reflects self-perception",
                    "Unknown rooms may represent undiscovered aspects of yourself"
                ]
            },
            "Vehicles": {
                "keywords": ["car", "train", "plane", "bus", "driving", "crash", "accident", "travel"],
                "interpretation": "Vehicles represent your journey through life and sense of control over your direction.",
                "tips": [
                    "Notice if you're driving or a passenger - reflects control in life",
                    "Consider where you're going in the dream",
                    "Vehicle problems may indicate obstacles in your path"
                ]
            },
            "Money": {
                "keywords": ["money", "cash", "rich", "poor", "wealthy", "coins", "bills", "treasure"],
                "interpretation": "Money dreams relate to self-worth, values, and material concerns.",
                "tips": [
                    "Consider your relationship with material security",
                    "Think about what you truly value in life",
                    "Money dreams may reflect confidence or insecurity"
                ]
            },
            "Pregnancy/Birth": {
                "keywords": ["pregnant", "pregnancy", "baby", "birth", "newborn", "labor"],
                "interpretation": "Pregnancy dreams often symbolize new projects, ideas, or phases of life being born.",
                "tips": [
                    "Consider what new project or idea you're developing",
                    "Think about creative potential waiting to be expressed",
                    "May indicate readiness for new responsibilities"
                ]
            },
            "Nakedness": {
                "keywords": ["naked", "nude", "undressed", "clothes", "embarrassed", "exposed"],
                "interpretation": "Nakedness dreams often reflect vulnerability or fear of being exposed.",
                "tips": [
                    "Consider areas where you feel vulnerable or exposed",
                    "Think about authenticity and being true to yourself",
                    "May indicate fear of judgment from others"
                ]
            },
            "Food": {
                "keywords": ["food", "eating", "hungry", "feast", "cooking", "restaurant", "meal"],
                "interpretation": "Food dreams relate to nourishment, satisfaction, and fulfillment in life.",
                "tips": [
                    "Consider what kind of fulfillment you're seeking",
                    "Think about emotional or spiritual nourishment needs",
                    "Pay attention to whether you're satisfied or still hungry"
                ]
            },
            "Lost": {
                "keywords": ["lost", "missing", "can't find", "searching", "maze", "confused", "direction"],
                "interpretation": "Being lost represents uncertainty about life direction or feeling confused about choices.",
                "tips": [
                    "Consider areas of life where you feel uncertain",
                    "Think about what guidance or clarity you need",
                    "May indicate need to reconnect with your goals"
                ]
            },
            "Fire": {
                "keywords": ["fire", "flames", "burn", "burning", "smoke", "heat", "explosion"],
                "interpretation": "Fire represents passion, transformation, destruction, or purification.",
                "tips": [
                    "Consider what needs to be transformed in your life",
                    "Think about your passionate feelings or anger",
                    "Fire may indicate need for purification or fresh start"
                ]
            }
        }
    
    def analyze_dream_themes(self, dream_content):
        """Analyze dream content and identify themes with confidence scores"""
        if not dream_content:
            return []
        
        dream_lower = dream_content.lower()
        theme_scores = {}
        
        for theme, data in self.dream_themes.items():
            score = 0
            matched_keywords = []
            
            for keyword in data["keywords"]:
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = len(re.findall(pattern, dream_lower))
                if matches > 0:
                    score += matches
                    matched_keywords.extend([keyword] * matches)
            
            if score > 0:
                # Calculate confidence based on keyword matches and dream length
                dream_length = len(dream_content.split())
                confidence = min((score / max(dream_length * 0.1, 1)) * 100, 100)
                
                theme_scores[theme] = {
                    'confidence': confidence,
                    'keywords': matched_keywords,
                    'score': score
                }
        
        # Sort by confidence score
        sorted_themes = sorted(theme_scores.items(), key=lambda x: x[1]['confidence'], reverse=True)
        
        return sorted_themes
    
    def get_dream_interpretation(self, themes):
        """Get interpretation and tips for detected themes"""
        interpretations = []
        
        for theme, data in themes:
            if theme in self.dream_themes:
                theme_info = self.dream_themes[theme]
                interpretations.append({
                    'theme': theme,
                    'confidence': data.get('confidence', 0),
                    'interpretation': theme_info['interpretation'],
                    'tips': theme_info['tips'],
                    'keywords_found': data.get('keywords', [])
                })
        
        return interpretations
    
    def analyze_dream_patterns(self, sleep_entries):
        """Analyze patterns across multiple dreams"""
        dream_entries = [entry for entry in sleep_entries if entry.had_dreams and entry.dream_content]
        
        if not dream_entries:
            return None
        
        # Analyze themes across all dreams
        all_themes = []
        dreams_by_date = {}
        
        for entry in dream_entries:
            themes = self.analyze_dream_themes(entry.dream_content)
            entry_themes = [theme for theme, _ in themes]
            all_themes.extend(entry_themes)
            dreams_by_date[entry.date] = entry_themes
        
        # Count theme frequency
        theme_counter = Counter(all_themes)
        most_common_themes = theme_counter.most_common(5)
        
        # Calculate recurring themes (appear in >20% of dreams)
        total_dreams = len(dream_entries)
        recurring_themes = []
        for theme, count in theme_counter.items():
            if count / total_dreams >= 0.2:  # 20% threshold
                recurring_themes.append((theme, count, (count/total_dreams)*100))
        
        # Analyze emotional themes correlation
        emotional_themes = []
        for entry in dream_entries:
            if entry.dream_emotions:
                themes = self.analyze_dream_themes(entry.dream_content)
                if themes:
                    emotional_themes.append({
                        'emotions': entry.dream_emotions,
                        'themes': [theme for theme, _ in themes[:2]],  # Top 2 themes
                        'sleep_quality': entry.sleep_quality
                    })
        
        return {
            'total_dream_nights': total_dreams,
            'most_common_themes': most_common_themes,
            'recurring_themes': recurring_themes,
            'dreams_by_date': dreams_by_date,
            'emotional_theme_correlation': emotional_themes,
            'analysis_period': f"{dream_entries[0].date} to {dream_entries[-1].date}"
        }
    
    def get_theme_recommendations(self, patterns):
        """Generate personalized recommendations based on dream patterns"""
        if not patterns or not patterns.get('most_common_themes'):
            return []
        
        recommendations = []
        
        for theme, frequency in patterns['most_common_themes'][:3]:
            if theme in self.dream_themes:
                theme_data = self.dream_themes[theme]
                recommendations.append({
                    'theme': theme,
                    'frequency': frequency,
                    'recommendation': f"Since '{theme}' appears frequently in your dreams, {theme_data['tips'][0].lower()}",
                    'insight': theme_data['interpretation']
                })
        
        return recommendations
    
    def analyze_emotional_dream_correlation(self, sleep_entries):
        """Analyze correlation between dream emotions and themes"""
        correlations = defaultdict(list)
        
        for entry in sleep_entries:
            if entry.had_dreams and entry.dream_content and entry.dream_emotions:
                themes = self.analyze_dream_themes(entry.dream_content)
                
                for emotion in entry.dream_emotions:
                    emotion_clean = emotion.lower().strip()
                    for theme, _ in themes[:2]:  # Top 2 themes
                        correlations[emotion_clean].append(theme)
        
        # Calculate most common theme for each emotion
        emotion_theme_patterns = {}
        for emotion, theme_list in correlations.items():
            if len(theme_list) >= 2:  # Need at least 2 occurrences
                theme_counter = Counter(theme_list)
                most_common = theme_counter.most_common(1)[0]
                emotion_theme_patterns[emotion] = {
                    'most_common_theme': most_common[0],
                    'frequency': most_common[1],
                    'total_occurrences': len(theme_list)
                }
        
        return emotion_theme_patterns