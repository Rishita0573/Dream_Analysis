# reports.py - Report Generation for Sleep Analytics Platform

from datetime import datetime, timedelta
from utils import (timing_decorator, create_simple_chart, format_duration, 
                  format_percentage, get_statistics_summary, format_list_display)
from enhanced_dream_analysis import DreamThemeAnalyzer, DreamJournal

class ReportGenerator:
    """Generate comprehensive reports for sleep and performance analysis"""
    
    def __init__(self):
        self.report_sections = []
        self.dream_analyzer = DreamThemeAnalyzer()
        self.dream_journal = DreamJournal()
    
    @timing_decorator
    def generate_comprehensive_report(self, sleep_analyzer):
        """Generate a comprehensive analysis report"""
        report_sections = []
        
        # Header
        report_sections.append(self._generate_header())
        
        # Data Overview
        report_sections.append(self._generate_data_overview(sleep_analyzer))
        
        # Sleep Analysis
        report_sections.append(self._generate_sleep_analysis(sleep_analyzer))
        
        # Performance Analysis
        report_sections.append(self._generate_performance_analysis(sleep_analyzer))
        
        # Dream Analysis
        report_sections.append(self._generate_dream_analysis(sleep_analyzer))
        
        # Enhanced Dream Insights
        report_sections.append(self._generate_enhanced_dream_analysis(sleep_analyzer))
        
        # Correlation Analysis
        report_sections.append(self._generate_correlation_analysis(sleep_analyzer))
        
        # Recommendations
        report_sections.append(self._generate_recommendations(sleep_analyzer))
        
        # Footer
        report_sections.append(self._generate_footer())
        
        return "\n\n".join(report_sections)
    
    def _generate_header(self):
        """Generate report header"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     SLEEP ANALYTICS & PERFORMANCE REPORT                    ║
║                          Generated: {current_time}                    ║
╚══════════════════════════════════════════════════════════════════════════════╝"""
    
    def _generate_data_overview(self, sleep_analyzer):
        """Generate data overview section"""
        sleep_count = len(sleep_analyzer.sleep_entries)
        performance_count = len(sleep_analyzer.performance_entries)
        
        # Calculate date range
        date_range = "No data"
        if sleep_analyzer.sleep_entries:
            dates = [entry.date for entry in sleep_analyzer.sleep_entries]
            earliest = min(dates)
            latest = max(dates)
            date_range = f"{earliest} to {latest}"
        
        return f"""
📊 DATA OVERVIEW
{'='*50}
Total Sleep Entries: {sleep_count}
Total Performance Entries: {performance_count}
Date Range: {date_range}
Data Quality: {'Good' if sleep_count >= 7 else 'Limited' if sleep_count >= 3 else 'Insufficient'}"""
    
    def _generate_sleep_analysis(self, sleep_analyzer):
        """Generate sleep analysis section"""
        if not sleep_analyzer.sleep_entries:
            return """
😴 SLEEP ANALYSIS
{'='*50}
No sleep data available for analysis."""
        
        # Basic statistics
        avg_quality = sleep_analyzer.calculate_average_sleep_quality()
        avg_duration = sleep_analyzer.calculate_average_sleep_duration()
        
        # Quality distribution
        quality_distribution = {}
        duration_categories = {'<6h': 0, '6-7h': 0, '7-8h': 0, '8-9h': 0, '>9h': 0}
        
        for entry in sleep_analyzer.sleep_entries:
            # Quality distribution
            quality_range = f"{(entry.sleep_quality-1)//2*2+1}-{(entry.sleep_quality-1)//2*2+2}"
            if entry.sleep_quality >= 9:
                quality_range = "9-10"
            quality_distribution[quality_range] = quality_distribution.get(quality_range, 0) + 1
            
            # Duration categories
            duration = entry.sleep_duration
            if duration < 6:
                duration_categories['<6h'] += 1
            elif duration < 7:
                duration_categories['6-7h'] += 1
            elif duration < 8:
                duration_categories['7-8h'] += 1
            elif duration < 9:
                duration_categories['8-9h'] += 1
            else:
                duration_categories['>9h'] += 1
        
        # Best and worst sleep days
        best_sleep = max(sleep_analyzer.sleep_entries, key=lambda x: x.sleep_quality)
        worst_sleep = min(sleep_analyzer.sleep_entries, key=lambda x: x.sleep_quality)
        
        # Sleep quality trend
        recent_qualities = [entry.sleep_quality for entry in sleep_analyzer.sleep_entries[-7:]]
        quality_stats = get_statistics_summary([entry.sleep_quality for entry in sleep_analyzer.sleep_entries])
        
        return f"""
😴 SLEEP ANALYSIS
{'='*50}
Average Sleep Quality: {avg_quality}/10
Average Sleep Duration: {format_duration(avg_duration)}

Sleep Quality Distribution:
{create_simple_chart(quality_distribution)}

Sleep Duration Distribution:
{create_simple_chart(duration_categories)}

Sleep Quality Statistics:
- Minimum: {quality_stats['min']}/10
- Maximum: {quality_stats['max']}/10
- Trend: {quality_stats['trend']}

Best Sleep Day: {best_sleep.date} (Quality: {best_sleep.sleep_quality}/10)
Worst Sleep Day: {worst_sleep.date} (Quality: {worst_sleep.sleep_quality}/10)"""
    
    def _generate_performance_analysis(self, sleep_analyzer):
        """Generate performance analysis section"""
        if not sleep_analyzer.performance_entries:
            return """
📈 PERFORMANCE ANALYSIS
{'='*50}
No performance data available for analysis."""
        
        # Average performance metrics
        avg_performance = sleep_analyzer.calculate_average_performance()
        
        # Performance trends
        productivity_values = [entry.productivity for entry in sleep_analyzer.performance_entries]
        mood_values = [entry.mood for entry in sleep_analyzer.performance_entries]
        energy_values = [entry.energy_level for entry in sleep_analyzer.performance_entries]
        stress_values = [entry.stress_level for entry in sleep_analyzer.performance_entries]
        
        productivity_stats = get_statistics_summary(productivity_values)
        mood_stats = get_statistics_summary(mood_values)
        energy_stats = get_statistics_summary(energy_values)
        stress_stats = get_statistics_summary(stress_values)
        
        # Best and worst performance days
        best_performance = max(sleep_analyzer.performance_entries, key=lambda x: x.overall_score)
        worst_performance = min(sleep_analyzer.performance_entries, key=lambda x: x.overall_score)
        
        # Performance distribution
        performance_ranges = {'Low (1-3)': 0, 'Medium (4-6)': 0, 'High (7-10)': 0}
        for entry in sleep_analyzer.performance_entries:
            if entry.overall_score <= 3:
                performance_ranges['Low (1-3)'] += 1
            elif entry.overall_score <= 6:
                performance_ranges['Medium (4-6)'] += 1
            else:
                performance_ranges['High (7-10)'] += 1
        
        return f"""
📈 PERFORMANCE ANALYSIS
{'='*50}
Average Performance Metrics:
- Productivity: {avg_performance['productivity']}/10 (Trend: {productivity_stats['trend']})
- Mood: {avg_performance['mood']}/10 (Trend: {mood_stats['trend']})
- Energy: {avg_performance['energy']}/10 (Trend: {energy_stats['trend']})
- Stress: {avg_performance['stress']}/10 (Trend: {stress_stats['trend']})
- Overall Score: {avg_performance['overall']}/10

Performance Distribution:
{create_simple_chart(performance_ranges)}

Best Performance Day: {best_performance.date} (Score: {best_performance.overall_score}/10)
Worst Performance Day: {worst_performance.date} (Score: {worst_performance.overall_score}/10)

Performance Insights:
- Highest Productivity: {productivity_stats['max']}/10
- Best Mood Day: {mood_stats['max']}/10
- Peak Energy Level: {energy_stats['max']}/10
- Lowest Stress: {stress_stats['min']}/10"""
    
    def _generate_dream_analysis(self, sleep_analyzer):
        """Generate dream analysis section"""
        if not sleep_analyzer.sleep_entries:
            return """
🌙 DREAM ANALYSIS
{'='*50}
No sleep data available for dream analysis."""
        
        # Dream frequency
        dream_frequency = sleep_analyzer.get_dream_frequency()
        total_dreams = sum(1 for entry in sleep_analyzer.sleep_entries if entry.had_dreams)
        total_nights = len(sleep_analyzer.sleep_entries)
        
        # Most common emotions
        common_emotions = sleep_analyzer.get_most_common_dream_emotions()
        
        # Dream quality correlation
        dream_nights_quality = []
        no_dream_nights_quality = []
        
        for entry in sleep_analyzer.sleep_entries:
            if entry.had_dreams:
                dream_nights_quality.append(entry.sleep_quality)
            else:
                no_dream_nights_quality.append(entry.sleep_quality)
        
        avg_dream_quality = sum(dream_nights_quality) / len(dream_nights_quality) if dream_nights_quality else 0
        avg_no_dream_quality = sum(no_dream_nights_quality) / len(no_dream_nights_quality) if no_dream_nights_quality else 0
        
        # Recent dream patterns
        recent_dreams = [entry for entry in sleep_analyzer.sleep_entries[-10:] if entry.had_dreams]
        
        dream_section = f"""
🌙 DREAM ANALYSIS
{'='*50}
Dream Frequency: {dream_frequency}% ({total_dreams}/{total_nights} nights)

Sleep Quality Comparison:
- Nights with dreams: {avg_dream_quality:.1f}/10
- Nights without dreams: {avg_no_dream_quality:.1f}/10"""
        
        if common_emotions:
            emotion_chart = {emotion: count for emotion, count in common_emotions}
            dream_section += f"""

Most Common Dream Emotions:
{create_simple_chart(emotion_chart)}"""
        
        if recent_dreams:
            dream_section += f"""

Recent Dreams ({len(recent_dreams)} entries):"""
            for dream in recent_dreams[-3:]:  # Show last 3 dreams
                dream_section += f"""
- {dream.date}: {dream.dream_content[:60]}{'...' if len(dream.dream_content) > 60 else ''}"""
        
        return dream_section
    
    def _generate_enhanced_dream_analysis(self, sleep_analyzer):
        """Generate enhanced dream analysis with themes and insights"""
        if not any(entry.had_dreams for entry in sleep_analyzer.sleep_entries):
            return """
🎭 ENHANCED DREAM ANALYSIS
{'='*50}
No dreams recorded for enhanced analysis."""
        
        try:
            # Get comprehensive dream statistics
            dream_stats = self.dream_journal.get_dream_statistics(sleep_analyzer.sleep_entries)
            
            # Analyze dream patterns
            patterns = self.dream_analyzer.analyze_dream_patterns(sleep_analyzer.sleep_entries)
            
            enhanced_section = f"""
🎭 ENHANCED DREAM ANALYSIS
{'='*50}
Dream Frequency: {dream_stats['dream_frequency']}% ({dream_stats['dream_nights']}/{dream_stats['total_nights']} nights)
Average Dream Length: {dream_stats['average_dream_length_words']} words
Emotional Diversity: {dream_stats['unique_emotions']} unique emotions recorded"""
            
            # Theme analysis
            if patterns and patterns.get('most_common_themes'):
                enhanced_section += f"""

🎪 DOMINANT DREAM THEMES:"""
                
                for theme, count in patterns['most_common_themes'][:5]:
                    percentage = (count / patterns['total_dream_nights']) * 100
                    enhanced_section += f"""
• {theme}: {count} occurrences ({percentage:.1f}% of dreams)"""
                    
                    # Add interpretation for top 3 themes
                    if theme in list(dict(patterns['most_common_themes'][:3])):
                        interpretation = self.dream_analyzer.theme_interpretations.get(theme, "")
                        if interpretation:
                            enhanced_section += f"""
  💡 {interpretation[:100]}{'...' if len(interpretation) > 100 else ''}"""
            
            # Emotion patterns
            if dream_stats['most_common_emotions']:
                enhanced_section += f"""

😊 EMOTIONAL PATTERNS:"""
                
                for emotion, count in dream_stats['most_common_emotions'][:5]:
                    percentage = (count / dream_stats['total_emotions_recorded']) * 100
                    enhanced_section += f"""
• {emotion.title()}: {count} times ({percentage:.1f}%)"""""
            
            # Sleep quality correlation with dreams
            enhanced_section += f"""

💤 DREAM-SLEEP QUALITY CORRELATION:
• Sleep quality with dreams: {dream_stats['avg_sleep_quality_with_dreams']}/10
• Sleep quality without dreams: {dream_stats['avg_sleep_quality_without_dreams']}/10"""
            
            quality_diff = dream_stats['avg_sleep_quality_with_dreams'] - dream_stats['avg_sleep_quality_without_dreams']
            
            if abs(quality_diff) > 0.5:
                if quality_diff > 0:
                    enhanced_section += f"""
• Insight: You sleep {quality_diff:.1f} points better on nights when you remember dreams"""
                else:
                    enhanced_section += f"""
• Insight: You sleep {abs(quality_diff):.1f} points better on nights when you don't remember dreams"""
            
            # Personalized recommendations
            dream_entries = [entry for entry in sleep_analyzer.sleep_entries if entry.had_dreams]
            
            if patterns and patterns.get('most_common_themes'):
                enhanced_section += f"""

💡 PERSONALIZED DREAM INSIGHTS:"""
                
                # Get tips for top 2 themes
                top_themes = [theme for theme, _ in patterns['most_common_themes'][:2]]
                recommendations = set()
                
                for theme in top_themes:
                    theme_tips = self.dream_analyzer.theme_tips.get(theme, [])
                    recommendations.update(theme_tips[:2])
                
                for i, tip in enumerate(list(recommendations)[:4], 1):
                    enhanced_section += f"""
{i}. {tip}"""
            
            return enhanced_section
            
        except Exception as e:
            return f"""
🎭 ENHANCED DREAM ANALYSIS
{'='*50}
Error generating enhanced dream analysis: {e}"""
    
    def _generate_correlation_analysis(self, sleep_analyzer):
        """Generate correlation analysis section"""
        correlations = sleep_analyzer.analyze_correlations()
        
        if not correlations or correlations == ["Insufficient data for correlation analysis"]:
            return """
🔗 CORRELATION ANALYSIS
{'='*50}
Insufficient data for meaningful correlation analysis.
Need at least 3 matching sleep and performance entries."""
        
        correlation_section = f"""
🔗 CORRELATION ANALYSIS
{'='*50}"""
        
        for correlation in correlations:
            correlation_section += f"\n• {correlation}"
        
        # Additional insights if we have enough data
        if len(correlations) > 2:
            correlation_section += """

Key Insights:
• Track patterns over time to identify personal sleep-performance relationships
• Look for consistent patterns across multiple weeks
• Consider external factors (stress, activities, etc.) that might influence both sleep and performance"""
        
        return correlation_section
    
    def _generate_recommendations(self, sleep_analyzer):
        """Generate personalized recommendations"""
        recommendations = []
        
        # Sleep quality recommendations
        if sleep_analyzer.sleep_entries:
            avg_quality = sleep_analyzer.calculate_average_sleep_quality()
            avg_duration = sleep_analyzer.calculate_average_sleep_duration()
            
            if avg_quality < 6:
                recommendations.append("🎯 Focus on improving sleep quality - consider sleep hygiene practices")
            
            if avg_duration < 7:
                recommendations.append("⏰ Aim for 7-9 hours of sleep per night for optimal performance")
            elif avg_duration > 9:
                recommendations.append("⏰ Consider if you're oversleeping - 7-9 hours is typically optimal")
            
            # Dream-based recommendations
            dream_frequency = sleep_analyzer.get_dream_frequency()
            if dream_frequency > 80:
                recommendations.append("🌙 High dream recall - consider keeping detailed dream journal")
            elif dream_frequency < 20:
                recommendations.append("🌙 Low dream recall - try meditation or stress reduction techniques")
        
        # Performance recommendations
        if sleep_analyzer.performance_entries:
            avg_performance = sleep_analyzer.calculate_average_performance()
            
            if avg_performance['stress'] > 7:
                recommendations.append("😌 High stress levels detected - consider stress management techniques")
            
            if avg_performance['energy'] < 5:
                recommendations.append("⚡ Low energy levels - review sleep schedule and consider exercise")
            
            if avg_performance['productivity'] < 6:
                recommendations.append("📊 Focus on productivity optimization - analyze your peak performance times")
        
        # Data collection recommendations
        data_quality_recs = []
        if len(sleep_analyzer.sleep_entries) < 14:
            data_quality_recs.append("📝 Continue logging data for at least 2 weeks for meaningful insights")
        
        if len(sleep_analyzer.performance_entries) < len(sleep_analyzer.sleep_entries):
            data_quality_recs.append("📈 Log performance data consistently with sleep data for better correlations")
        
        recommendations.extend(data_quality_recs)
        
        if not recommendations:
            recommendations.append("✅ Great job maintaining consistent sleep and performance tracking!")
            recommendations.append("📊 Continue monitoring patterns for long-term insights")
        
        recommendation_section = f"""
💡 PERSONALIZED RECOMMENDATIONS
{'='*50}"""
        
        for i, rec in enumerate(recommendations, 1):
            recommendation_section += f"\n{i}. {rec}"
        
        return recommendation_section
    
    def _generate_footer(self):
        """Generate report footer"""
        return f"""
{'='*80}
Report generated by Sleep Analytics Platform
For questions or suggestions, continue tracking your sleep and performance patterns.
Remember: Consistency in data logging leads to better insights!
{'='*80}"""
    
    @timing_decorator
    def generate_weekly_summary(self, sleep_analyzer, weeks_back=1):
        """Generate a weekly summary report"""
        # This is a simplified version - you can expand this
        end_date = datetime.now()
        start_date = end_date - timedelta(weeks=weeks_back)
        
        # Filter entries for the week
        weekly_sleep = [entry for entry in sleep_analyzer.sleep_entries 
                       if start_date.strftime("%Y-%m-%d") <= entry.date <= end_date.strftime("%Y-%m-%d")]
        
        weekly_performance = [entry for entry in sleep_analyzer.performance_entries 
                            if start_date.strftime("%Y-%m-%d") <= entry.date <= end_date.strftime("%Y-%m-%d")]
        
        if not weekly_sleep and not weekly_performance:
            return "No data available for the selected week."
        
        summary = f"""
📅 WEEKLY SUMMARY ({start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")})
{'='*60}
Sleep Entries: {len(weekly_sleep)}
Performance Entries: {len(weekly_performance)}"""
        
        if weekly_sleep:
            avg_quality = sum(entry.sleep_quality for entry in weekly_sleep) / len(weekly_sleep)
            avg_duration = sum(entry.sleep_duration for entry in weekly_sleep) / len(weekly_sleep)
            summary += f"""
Average Sleep Quality: {avg_quality:.1f}/10
Average Sleep Duration: {format_duration(avg_duration)}"""
        
        if weekly_performance:
            avg_productivity = sum(entry.productivity for entry in weekly_performance) / len(weekly_performance)
            avg_mood = sum(entry.mood for entry in weekly_performance) / len(weekly_performance)
            summary += f"""
Average Productivity: {avg_productivity:.1f}/10
Average Mood: {avg_mood:.1f}/10"""
        
        return summary