# main.py - Sleep Analytics Platform Main Program

from sleep_entry import SleepEntry, PerformanceEntry, SleepAnalyzer
from file_handler import FileHandler
from reports import ReportGenerator
from dream_journal import DreamJournal
from dream_analyzer import DreamThemeAnalyzer
from utils import get_valid_input, clear_screen, log_activity
import sys

class SleepAnalyticsPlatform:
    def __init__(self):
        self.sleep_analyzer = SleepAnalyzer()
        self.file_handler = FileHandler()
        self.report_generator = ReportGenerator()
        self.dream_journal = DreamJournal()
        self.dream_analyzer = DreamThemeAnalyzer()
        
        # Load existing data on startup
        self.sleep_analyzer.sleep_entries = self.file_handler.load_sleep_data()
        self.sleep_analyzer.performance_entries = self.file_handler.load_performance_data()
    
    @log_activity
    def display_menu(self):
        """Display main menu options"""
        print("\n" + "="*50)
        print("    SLEEP ANALYTICS & PERFORMANCE PLATFORM")
        print("="*50)
        print("1. Record Sleep Data")
        print("2. Record Performance Data")
        print("3. View Sleep History")
        print("4. View Performance History")
        print("5. Generate Analysis Report")
        print("6. View Correlations")
        print("7. 🌙 Advanced Dream Analysis")
        print("8. 🎭 Dream Theme Explorer")
        print("9. 🔍 Search Dreams")
        print("10. 📊 Dream Statistics")
        print("11. Backup Data")
        print("12. Exit")
        print("="*50)
    
    def run(self):
        """Main program loop"""
        print("Welcome to Sleep Analytics Platform!")
        
        while True:
            try:
                self.display_menu()
                choice = get_valid_input("Enter your choice (1-12): ", int, range(1, 13))
                
                if choice == 1:
                    self.record_sleep_data()
                elif choice == 2:
                    self.record_performance_data()
                elif choice == 3:
                    self.view_sleep_history()
                elif choice == 4:
                    self.view_performance_history()
                elif choice == 5:
                    self.generate_analysis_report()
                elif choice == 6:
                    self.view_correlations()
                elif choice == 7:
                    self.advanced_dream_analysis()
                elif choice == 8:
                    self.dream_theme_explorer()
                elif choice == 9:
                    self.search_dreams()
                elif choice == 10:
                    self.dream_statistics()
                elif choice == 11:
                    self.backup_data()
                elif choice == 12:
                    self.exit_program()
                    break
                    
            except KeyboardInterrupt:
                print("\n\nProgram interrupted by user.")
                self.exit_program()
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Please try again.")
    
    @log_activity
    def record_sleep_data(self):
        """Record new sleep entry"""
        print("\n--- Record Sleep Data ---")
        
        try:
            date = input("Enter date (YYYY-MM-DD): ")
            bedtime = input("Enter bedtime (HH:MM): ")
            wake_time = input("Enter wake time (HH:MM): ")
            sleep_quality = get_valid_input("Rate sleep quality (1-10): ", int, range(1, 11))
            
            # Dream data
            had_dreams = input("Did you remember any dreams? (y/n): ").lower() == 'y'
            dream_content = ""
            dream_emotions = []
            
            if had_dreams:
                dream_content = input("Describe your dream in detail: ")
                emotions_input = input("Dream emotions (happy, sad, anxious, peaceful, etc.): ")
                dream_emotions = [emotion.strip() for emotion in emotions_input.split(',') if emotion.strip()]
                
                # Analyze dream themes immediately
                print("\n🌙 Analyzing your dream...")
                themes = self.dream_analyzer.analyze_dream_themes(dream_content)
                
                if themes:
                    print("\n🎭 Detected Dream Themes:")
                    for theme, data in themes[:3]:  # Show top 3 themes
                        print(f"   • {theme} (Confidence: {data['confidence']:.1f}%)")
                    
                    # Get interpretation for top theme
                    interpretations = self.dream_analyzer.get_dream_interpretation(themes[:1])
                    if interpretations:
                        print(f"\n💡 Theme Insight: {interpretations[0]['interpretation']}")
                        print(f"💭 Suggestion: {interpretations[0]['tips'][0]}")
            
            sleep_entry = SleepEntry(date, bedtime, wake_time, sleep_quality, 
                                   had_dreams, dream_content, dream_emotions)
            
            self.sleep_analyzer.add_sleep_entry(sleep_entry)
            self.file_handler.save_sleep_data(self.sleep_analyzer.sleep_entries)
            
            print("Sleep data recorded successfully!")
            
        except Exception as e:
            print(f"Error recording sleep data: {e}")
    
    @log_activity
    def record_performance_data(self):
        """Record performance metrics for the day"""
        print("\n--- Record Performance Data ---")
        
        try:
            date = input("Enter date (YYYY-MM-DD): ")
            productivity = get_valid_input("Rate productivity (1-10): ", int, range(1, 11))
            mood = get_valid_input("Rate mood (1-10): ", int, range(1, 11))
            energy_level = get_valid_input("Rate energy level (1-10): ", int, range(1, 11))
            stress_level = get_valid_input("Rate stress level (1-10): ", int, range(1, 11))
            
            activities = input("Main activities of the day: ")
            notes = input("Any additional notes: ")
            
            performance_entry = PerformanceEntry(date, productivity, mood, 
                                               energy_level, stress_level, activities, notes)
            
            self.sleep_analyzer.add_performance_entry(performance_entry)
            self.file_handler.save_performance_data(self.sleep_analyzer.performance_entries)
            
            print("Performance data recorded successfully!")
            
        except Exception as e:
            print(f"Error recording performance data: {e}")
    
    def view_sleep_history(self):
        """Display sleep history"""
        print("\n--- Sleep History ---")
        
        if not self.sleep_analyzer.sleep_entries:
            print("No sleep data found.")
            return
        
        for entry in self.sleep_analyzer.get_recent_sleep_entries(10):
            print(entry)
            print("-" * 40)
    
    def view_performance_history(self):
        """Display performance history"""
        print("\n--- Performance History ---")
        
        if not self.sleep_analyzer.performance_entries:
            print("No performance data found.")
            return
        
        for entry in self.sleep_analyzer.get_recent_performance_entries(10):
            print(entry)
            print("-" * 40)
    
    def generate_analysis_report(self):
        """Generate comprehensive analysis report"""
        print("\n--- Generating Analysis Report ---")
        
        try:
            report = self.report_generator.generate_comprehensive_report(self.sleep_analyzer)
            print(report)
            
            # Save report to file
            self.file_handler.save_report(report)
            print("\nReport saved to data/reports/")
            
        except Exception as e:
            print(f"Error generating report: {e}")
    
    def view_correlations(self):
        """Display correlation analysis"""
        print("\n--- Sleep-Performance Correlations ---")
        
        try:
            correlations = self.sleep_analyzer.analyze_correlations()
            for correlation in correlations:
                print(correlation)
        except Exception as e:
            print(f"Error analyzing correlations: {e}")
    
    @log_activity
    def advanced_dream_analysis(self):
        """Comprehensive dream analysis with insights"""
        print("\n🌙 --- Advanced Dream Analysis ---")
        
        if not any(entry.had_dreams for entry in self.sleep_analyzer.sleep_entries):
            print("No dreams found in your data. Start recording dreams to see analysis!")
            return
        
        try:
            # Generate comprehensive dream insights
            insights = self.dream_journal.generate_dream_insights(self.sleep_analyzer.sleep_entries)
            print(insights)
            
            # Show recent dream patterns
            patterns = self.dream_analyzer.analyze_dream_patterns(self.sleep_analyzer.sleep_entries)
            
            if patterns and patterns.get('dreams_by_date'):
                print(f"\n📅 RECENT DREAM TIMELINE ({patterns['analysis_period']}):")
                recent_dates = sorted(patterns['dreams_by_date'].keys())[-5:]  # Last 5 dates
                
                for date in recent_dates:
                    themes = patterns['dreams_by_date'][date]
                    theme_str = ', '.join(themes[:2]) if themes else 'No themes detected'
                    print(f"   • {date}: {theme_str}")
        
        except Exception as e:
            print(f"Error in dream analysis: {e}")
    
    @log_activity
    def dream_theme_explorer(self):
        """Explore dreams by themes"""
        print("\n🎭 --- Dream Theme Explorer ---")
        
        dream_entries = [entry for entry in self.sleep_analyzer.sleep_entries if entry.had_dreams]
        
        if not dream_entries:
            print("No dreams found to explore!")
            return
        
        try:
            # Show available themes
            print("\nAvailable Dream Themes:")
            themes = list(self.dream_analyzer.dream_themes.keys())
            for i, theme in enumerate(themes, 1):
                if i % 3 == 0:
                    print(f"{i:2d}. {theme}")
                else:
                    print(f"{i:2d}. {theme:<15}", end="")
            
            print("\n")
            
            # Get theme choice
            theme_choice = get_valid_input("Enter theme number to explore: ", int, range(1, len(themes) + 1))
            selected_theme = themes[theme_choice - 1]
            
            # Search dreams by theme
            matching_dreams = self.dream_journal.search_dreams_by_theme(
                self.sleep_analyzer.sleep_entries, selected_theme
            )
            
            if not matching_dreams:
                print(f"\nNo dreams found with '{selected_theme}' theme.")
                return
            
            print(f"\n🔍 Dreams with '{selected_theme}' theme ({len(matching_dreams)} found):")
            print("=" * 60)
            
            for dream in matching_dreams[-5:]:  # Show last 5 matching dreams
                print(f"\nDate: {dream['date']}")
                print(f"Content: {dream['content'][:100]}{'...' if len(dream['content']) > 100 else ''}")
                print(f"Emotions: {', '.join(dream['emotions']) if dream['emotions'] else 'None recorded'}")
                print(f"Sleep Quality: {dream['sleep_quality']}/10")
                print("-" * 40)
            
            # Show theme interpretation
            interpretation_data = self.dream_analyzer.get_dream_interpretation([(selected_theme, {'confidence': 100, 'keywords': []})])
            
            if interpretation_data:
                interp = interpretation_data[0]
                print(f"\n💡 THEME INTERPRETATION:")
                print(f"Theme: {interp['theme']}")
                print(f"Meaning: {interp['interpretation']}")
                print(f"\n💭 PERSONALIZED TIPS:")
                for i, tip in enumerate(interp['tips'][:3], 1):
                    print(f"   {i}. {tip}")
        
        except Exception as e:
            print(f"Error exploring dream themes: {e}")
    
    @log_activity
    def search_dreams(self):
        """Search dreams by various criteria"""
        print("\n🔍 --- Dream Search ---")
        
        dream_entries = [entry for entry in self.sleep_analyzer.sleep_entries if entry.had_dreams]
        
        if not dream_entries:
            print("No dreams found to search!")
            return
        
        try:
            print("\nSearch Options:")
            print("1. Search by keyword")
            print("2. Search by emotion")
            print("3. Search by sleep quality")
            print("4. Search by date range")
            
            search_choice = get_valid_input("Choose search type (1-4): ", int, range(1, 5))
            
            if search_choice == 1:
                keyword = input("Enter keyword to search for: ").strip()
                
                results = []
                for entry in dream_entries:
                    if keyword.lower() in entry.dream_content.lower():
                        results.append(entry)
                
                print(f"\n📝 Found {len(results)} dreams containing '{keyword}':")
                
            elif search_choice == 2:
                emotion = input("Enter emotion to search for: ").strip()
                
                results = []
                for entry in dream_entries:
                    if entry.dream_emotions:
                        emotions_lower = [e.lower() for e in entry.dream_emotions]
                        if emotion.lower() in emotions_lower:
                            results.append(entry)
                
                print(f"\n😊 Found {len(results)} dreams with '{emotion}' emotion:")
                
            elif search_choice == 3:
                min_quality = get_valid_input("Enter minimum sleep quality (1-10): ", int, range(1, 11))
                
                results = []
                for entry in dream_entries:
                    if entry.sleep_quality >= min_quality:
                        results.append(entry)
                
                print(f"\n⭐ Found {len(results)} dreams with sleep quality {min_quality}+:")
                
            elif search_choice == 4:
                start_date = input("Enter start date (YYYY-MM-DD): ")
                end_date = input("Enter end date (YYYY-MM-DD): ")
                
                results = []
                for entry in dream_entries:
                    if start_date <= entry.date <= end_date:
                        results.append(entry)
                
                print(f"\n📅 Found {len(results)} dreams between {start_date} and {end_date}:")
            
            # Display results
            if results:
                for i, entry in enumerate(results[-3:], 1):  # Show last 3 results
                    print(f"\n{i}. Date: {entry.date}")
                    print(f"   Sleep Quality: {entry.sleep_quality}/10")
                    print(f"   Dream: {entry.dream_content[:80]}{'...' if len(entry.dream_content) > 80 else ''}")
                    if entry.dream_emotions:
                        print(f"   Emotions: {', '.join(entry.dream_emotions)}")
                    
                    # Show themes for this dream
                    themes = self.dream_analyzer.analyze_dream_themes(entry.dream_content)
                    if themes:
                        theme_names = [theme for theme, _ in themes[:2]]
                        print(f"   Themes: {', '.join(theme_names)}")
                    print("-" * 50)
                
                if len(results) > 3:
                    print(f"\n... and {len(results) - 3} more results")
            else:
                print("No dreams found matching your criteria.")
        
        except Exception as e:
            print(f"Error searching dreams: {e}")
    
    @log_activity
    def dream_statistics(self):
        """Display comprehensive dream statistics"""
        print("\n📊 --- Dream Statistics ---")
        
        try:
            stats = self.dream_journal.get_dream_statistics(self.sleep_analyzer.sleep_entries)
            
            if not stats or stats.get('dream_nights', 0) == 0:
                print("No dream data available for statistics.")
                return
            
            print(f"\n📈 OVERALL STATISTICS:")
            print(f"Total nights tracked: {stats['total_nights']}")
            print(f"Nights with dreams: {stats['dream_nights']}")
            print(f"Dream frequency: {stats['dream_frequency']}%")
            print(f"Average dream length: {stats['average_dream_length_words']} words")
            
            print(f"\n😴 SLEEP QUALITY COMPARISON:")
            print(f"Average sleep quality with dreams: {stats['avg_sleep_quality_with_dreams']}/10")
            print(f"Average sleep quality without dreams: {stats['avg_sleep_quality_without_dreams']}/10")
            
            if stats['avg_sleep_quality_with_dreams'] > stats['avg_sleep_quality_without_dreams']:
                print("💡 You tend to sleep better on nights when you remember dreams!")
            elif stats['avg_sleep_quality_with_dreams'] < stats['avg_sleep_quality_without_dreams']:
                print("💡 You tend to sleep better on nights when you don't remember dreams.")
            else:
                print("💡 Dream recall doesn't seem to affect your sleep quality.")
            
            if stats['most_common_emotions']:
                print(f"\n😊 MOST COMMON DREAM EMOTIONS:")
                for emotion, count in stats['most_common_emotions']:
                    percentage = (count / stats['total_emotions_recorded']) * 100
                    print(f"   • {emotion.title()}: {count} times ({percentage:.1f}%)")
            
            print(f"\n🎭 EMOTION DIVERSITY:")
            print(f"Total emotions recorded: {stats['total_emotions_recorded']}")
            print(f"Unique emotions: {stats['unique_emotions']}")
            
            # Theme frequency analysis
            patterns = self.dream_analyzer.analyze_dream_patterns(self.sleep_analyzer.sleep_entries)
            
            if patterns and patterns.get('most_common_themes'):
                print(f"\n🎪 MOST COMMON DREAM THEMES:")
                for theme, count in patterns['most_common_themes']:
                    percentage = (count / patterns['total_dream_nights']) * 100
                    print(f"   • {theme}: {count} dreams ({percentage:.1f}%)")
            
            # Recent trends
            recent_dreams = [entry for entry in self.sleep_analyzer.sleep_entries[-14:] if entry.had_dreams]
            if len(recent_dreams) >= 3:
                recent_quality = [entry.sleep_quality for entry in recent_dreams]
                avg_recent_quality = sum(recent_quality) / len(recent_quality)
                
                print(f"\n📅 RECENT TRENDS (Last 14 days):")
                print(f"Recent dreams recorded: {len(recent_dreams)}")
                print(f"Average recent sleep quality: {avg_recent_quality:.1f}/10")
                
                # Trend analysis
                if len(recent_quality) >= 5:
                    first_half = recent_quality[:len(recent_quality)//2]
                    second_half = recent_quality[len(recent_quality)//2:]
                    
                    if sum(second_half) > sum(first_half):
                        print("📈 Your sleep quality with dreams is improving!")
                    elif sum(second_half) < sum(first_half):
                        print("📉 Your sleep quality with dreams has declined recently.")
                    else:
                        print("📊 Your sleep quality with dreams is stable.")
        
        except Exception as e:
            print(f"Error generating dream statistics: {e}")
    
    def backup_data(self):
        """Backup all data"""
        try:
            self.file_handler.create_backup()
            print("Data backup created successfully!")
        except Exception as e:
            print(f"Error creating backup: {e}")
    
    def exit_program(self):
        """Clean exit with data save"""
        print("\nSaving data and exiting...")
        try:
            self.file_handler.save_sleep_data(self.sleep_analyzer.sleep_entries)
            self.file_handler.save_performance_data(self.sleep_analyzer.performance_entries)
            print("Data saved successfully!")
        except Exception as e:
            print(f"Error saving data: {e}")
        
        print("Thank you for using Sleep Analytics Platform!")

def main():
    """Program entry point"""
    platform = SleepAnalyticsPlatform()
    platform.run()

if __name__ == "__main__":
    main()