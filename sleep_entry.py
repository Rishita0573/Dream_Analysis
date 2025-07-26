# sleep_entry.py - Core Classes for Sleep Analytics Platform

import copy
from datetime import datetime

class SleepEntry:
    """Class to represent a single sleep entry"""
    
    def __init__(self, date, bedtime, wake_time, sleep_quality, 
                 had_dreams=False, dream_content="", dream_emotions=None):
        self.date = date
        self.bedtime = bedtime
        self.wake_time = wake_time
        self.sleep_quality = sleep_quality
        self.had_dreams = had_dreams
        self.dream_content = dream_content
        self.dream_emotions = dream_emotions if dream_emotions else []
        self.sleep_duration = self._calculate_sleep_duration()
    
    def _calculate_sleep_duration(self):
        """Calculate sleep duration in hours"""
        try:
            bed_hour, bed_min = map(int, self.bedtime.split(':'))
            wake_hour, wake_min = map(int, self.wake_time.split(':'))
            
            bed_minutes = bed_hour * 60 + bed_min
            wake_minutes = wake_hour * 60 + wake_min
            
            # Handle overnight sleep
            if wake_minutes < bed_minutes:
                wake_minutes += 24 * 60
            
            duration_minutes = wake_minutes - bed_minutes
            return round(duration_minutes / 60, 1)
        except:
            return 0.0
    
    def get_dream_emotion_summary(self):
        """Get summary of dream emotions"""
        if not self.dream_emotions:
            return "No emotions recorded"
        return ", ".join(self.dream_emotions)
    
    def __str__(self):
        """String representation of sleep entry"""
        dream_info = ""
        if self.had_dreams:
            dream_info = f"\n  Dreams: {self.dream_content[:50]}..."
            if self.dream_emotions:
                dream_info += f"\n  Emotions: {self.get_dream_emotion_summary()}"
        
        return f"""Date: {self.date}
  Sleep: {self.bedtime} - {self.wake_time} ({self.sleep_duration}h)
  Quality: {self.sleep_quality}/10{dream_info}"""

class PerformanceEntry:
    """Class to represent daily performance metrics"""
    
    def __init__(self, date, productivity, mood, energy_level, stress_level, 
                 activities="", notes=""):
        self.date = date
        self.productivity = productivity
        self.mood = mood
        self.energy_level = energy_level
        self.stress_level = stress_level
        self.activities = activities
        self.notes = notes
        self.overall_score = self._calculate_overall_score()
    
    def _calculate_overall_score(self):
        """Calculate overall performance score"""
        # Stress is inverted (lower stress = better)
        inverted_stress = 11 - self.stress_level
        return round((self.productivity + self.mood + self.energy_level + inverted_stress) / 4, 1)
    
    def __str__(self):
        """String representation of performance entry"""
        return f"""Date: {self.date}
  Productivity: {self.productivity}/10
  Mood: {self.mood}/10
  Energy: {self.energy_level}/10
  Stress: {self.stress_level}/10
  Overall Score: {self.overall_score}/10
  Activities: {self.activities}
  Notes: {self.notes}"""

class SleepAnalyzer:
    """Main analyzer class for sleep and performance data"""
    
    def __init__(self):
        self.sleep_entries = []
        self.performance_entries = []
    
    def add_sleep_entry(self, sleep_entry):
        """Add a new sleep entry"""
        if not isinstance(sleep_entry, SleepEntry):
            raise TypeError("Expected SleepEntry object")
        self.sleep_entries.append(sleep_entry)
    
    def add_performance_entry(self, performance_entry):
        """Add a new performance entry"""
        if not isinstance(performance_entry, PerformanceEntry):
            raise TypeError("Expected PerformanceEntry object")
        self.performance_entries.append(performance_entry)
    
    def get_recent_sleep_entries(self, count=10):
        """Get recent sleep entries"""
        return self.sleep_entries[-count:] if self.sleep_entries else []
    
    def get_recent_performance_entries(self, count=10):
        """Get recent performance entries"""
        return self.performance_entries[-count:] if self.performance_entries else []
    
    def calculate_average_sleep_quality(self):
        """Calculate average sleep quality"""
        if not self.sleep_entries:
            return 0
        
        total_quality = sum(entry.sleep_quality for entry in self.sleep_entries)
        return round(total_quality / len(self.sleep_entries), 1)
    
    def calculate_average_sleep_duration(self):
        """Calculate average sleep duration"""
        if not self.sleep_entries:
            return 0
        
        total_duration = sum(entry.sleep_duration for entry in self.sleep_entries)
        return round(total_duration / len(self.sleep_entries), 1)
    
    def calculate_average_performance(self):
        """Calculate average performance metrics"""
        if not self.performance_entries:
            return {}
        
        total_productivity = sum(entry.productivity for entry in self.performance_entries)
        total_mood = sum(entry.mood for entry in self.performance_entries)
        total_energy = sum(entry.energy_level for entry in self.performance_entries)
        total_stress = sum(entry.stress_level for entry in self.performance_entries)
        total_overall = sum(entry.overall_score for entry in self.performance_entries)
        
        count = len(self.performance_entries)
        
        return {
            'productivity': round(total_productivity / count, 1),
            'mood': round(total_mood / count, 1),
            'energy': round(total_energy / count, 1),
            'stress': round(total_stress / count, 1),
            'overall': round(total_overall / count, 1)
        }
    
    def get_dream_frequency(self):
        """Calculate dream frequency percentage"""
        if not self.sleep_entries:
            return 0
        
        dream_count = sum(1 for entry in self.sleep_entries if entry.had_dreams)
        return round((dream_count / len(self.sleep_entries)) * 100, 1)
    
    def get_most_common_dream_emotions(self):
        """Get most common dream emotions"""
        emotion_count = {}
        
        for entry in self.sleep_entries:
            if entry.had_dreams and entry.dream_emotions:
                for emotion in entry.dream_emotions:
                    emotion = emotion.lower().strip()
                    emotion_count[emotion] = emotion_count.get(emotion, 0) + 1
        
        # Sort by frequency
        sorted_emotions = sorted(emotion_count.items(), key=lambda x: x[1], reverse=True)
        return sorted_emotions[:5]  # Top 5 emotions
    
    def find_best_sleep_days(self):
        """Find days with best sleep quality"""
        if not self.sleep_entries:
            return []
        
        # Sort by sleep quality (descending)
        sorted_entries = sorted(self.sleep_entries, 
                              key=lambda x: x.sleep_quality, reverse=True)
        return sorted_entries[:5]  # Top 5 best sleep days
    
    def find_best_performance_days(self):
        """Find days with best performance"""
        if not self.performance_entries:
            return []
        
        # Sort by overall score (descending)
        sorted_entries = sorted(self.performance_entries, 
                              key=lambda x: x.overall_score, reverse=True)
        return sorted_entries[:5]  # Top 5 best performance days
    
    def analyze_correlations(self):
        """Analyze correlations between sleep and performance"""
        correlations = []
        
        if not self.sleep_entries or not self.performance_entries:
            return ["Insufficient data for correlation analysis"]
        
        # Create date-matched pairs
        sleep_dict = {entry.date: entry for entry in self.sleep_entries}
        performance_dict = {entry.date: entry for entry in self.performance_entries}
        
        matched_dates = set(sleep_dict.keys()) & set(performance_dict.keys())
        
        if len(matched_dates) < 3:
            return ["Need at least 3 matching dates for correlation analysis"]
        
        # Simple correlation observations
        high_sleep_quality_days = []
        low_sleep_quality_days = []
        
        for date in matched_dates:
            sleep_entry = sleep_dict[date]
            performance_entry = performance_dict[date]
            
            if sleep_entry.sleep_quality >= 7:
                high_sleep_quality_days.append(performance_entry.overall_score)
            elif sleep_entry.sleep_quality <= 4:
                low_sleep_quality_days.append(performance_entry.overall_score)
        
        if high_sleep_quality_days:
            avg_performance_good_sleep = round(sum(high_sleep_quality_days) / len(high_sleep_quality_days), 1)
            correlations.append(f"Average performance on good sleep days (7+): {avg_performance_good_sleep}/10")
        
        if low_sleep_quality_days:
            avg_performance_poor_sleep = round(sum(low_sleep_quality_days) / len(low_sleep_quality_days), 1)
            correlations.append(f"Average performance on poor sleep days (≤4): {avg_performance_poor_sleep}/10")
        
        # Dream correlation
        dream_performance = []
        no_dream_performance = []
        
        for date in matched_dates:
            sleep_entry = sleep_dict[date]
            performance_entry = performance_dict[date]
            
            if sleep_entry.had_dreams:
                dream_performance.append(performance_entry.overall_score)
            else:
                no_dream_performance.append(performance_entry.overall_score)
        
        if dream_performance and no_dream_performance:
            avg_dream_performance = round(sum(dream_performance) / len(dream_performance), 1)
            avg_no_dream_performance = round(sum(no_dream_performance) / len(no_dream_performance), 1)
            
            correlations.append(f"Average performance with dreams: {avg_dream_performance}/10")
            correlations.append(f"Average performance without dreams: {avg_no_dream_performance}/10")
        
        return correlations if correlations else ["No significant correlations found"]

# Iterator for sleep entries
class SleepEntryIterator:
    """Iterator for sleep entries"""
    
    def __init__(self, sleep_entries):
        self.sleep_entries = sleep_entries
        self.index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index < len(self.sleep_entries):
            entry = self.sleep_entries[self.index]
            self.index += 1
            return entry
        raise StopIteration

# Generator functions for efficient data processing
def monthly_sleep_data(sleep_entries, year, month):
    """Generator for monthly sleep data"""
    target_month = f"{year}-{month:02d}"
    for entry in sleep_entries:
        if entry.date.startswith(target_month):
            yield entry

def high_quality_sleep_generator(sleep_entries, min_quality=7):
    """Generator for high quality sleep entries"""
    for entry in sleep_entries:
        if entry.sleep_quality >= min_quality:
            yield entry