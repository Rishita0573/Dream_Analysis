# main.py - Sleep Analytics Platform Main Program with Excel Integration

from sleep_entry import SleepEntry, PerformanceEntry, SleepAnalyzer
from file_handler import FileHandler
from excel_handler import ExcelHandler
from reports import ReportGenerator
from dream_journal import DreamJournal
from dream_analyzer import DreamThemeAnalyzer
from utils import get_valid_input, clear_screen, log_activity
import sys
import os

class SleepAnalyticsPlatform:
    def __init__(self):
        self.sleep_analyzer = SleepAnalyzer()
        self.file_handler = FileHandler()
        self.excel_handler = ExcelHandler()
        self.report_generator = ReportGenerator()
        self.dream_journal = DreamJournal()
        self.dream_analyzer = DreamThemeAnalyzer()
        
        # Data loading preference (default: text files for backward compatibility)
        self.data_source = "text"  # Can be "text" or "excel"
        
        # Load existing data on startup
        self._load_initial_data()
    
    def _load_initial_data(self):
        """Load data from the preferred source"""
        try:
            # Check if Excel files exist and have data
            excel_info = self.excel_handler.get_excel_file_info()
            
            if excel_info['sleep_entries_count'] > 0 or excel_info['performance_entries_count'] > 0:
                print("📊 Excel files found with data. Loading from Excel...")
                self.data_source = "excel"
                self.sleep_analyzer.sleep_entries = self.excel_handler.load_sleep_data_from_excel()
                self.sleep_analyzer.performance_entries = self.excel_handler.load_performance_data_from_excel()
            else:
                print("📄 Loading from text files...")
                self.data_source = "text"
                self.sleep_analyzer.sleep_entries = self.file_handler.load_sleep_data()
                self.sleep_analyzer.performance_entries = self.file_handler.load_performance_data()
                
        except Exception as e:
            print(f"Error loading initial data: {e}")
            print("Starting with empty data...")
    
    @log_activity
    def display_menu(self):
        """Display main menu options with Excel integration"""
        print("\n" + "="*60)
        print("    SLEEP ANALYTICS & PERFORMANCE PLATFORM")
        print("    📊 Excel Integration Enabled")
        print("="*60)
        print("📝 DATA ENTRY:")
        print("1. Record Sleep Data (Terminal)")
        print("2. Record Performance Data (Terminal)")
        print("3. 📊 Load Data from Excel")
        print("4. 📁 Create Excel Templates")
        print("5. 🔄 Switch Data Source (Text/Excel)")
        
        print("\n📈 DATA VIEWING:")
        print("6. View Sleep History")
        print("7. View Performance History")
        print("8. Generate Analysis Report")
        print("9. View Correlations")
        
        print("\n🌙 DREAM ANALYSIS:")
        print("10. Advanced Dream Analysis")
        print("11. Dream Theme Explorer")
        print("12. Search Dreams")
        print("13. Dream Statistics")
        
        print("\n💾 DATA MANAGEMENT:")
        print("14. Export to Excel with Analysis")
        print("15. Backup Data")
        print("16. View Data Source Info")
        print("17. Exit")
        print("="*60)
        print(f"Current Data Source: {self.data_source.upper()}")
    
    def run(self):
        """Main program loop"""
        print("🌙 Welcome to Sleep Analytics Platform with Excel Integration!")
        
        while True:
            try:
                self.display_menu()
                choice = get_valid_input("Enter your choice (1-17): ", int, range(1, 18))
                
                if choice == 1:
                    self.record_sleep_data()
                elif choice == 2:
                    self.record_performance_data()
                elif choice == 3:
                    self.load_data_from_excel()
                elif choice == 4:
                    self.create_excel_templates()
                elif choice == 5:
                    self.switch_data_source()
                elif choice == 6:
                    self.view_sleep_history()
                elif choice == 7:
                    self.view_performance_history()
                elif choice == 8:
                    self.generate_analysis_report()
                elif choice == 9:
                    self.view_correlations()
                elif choice == 10:
                    self.advanced_dream_analysis()
                elif choice == 11:
                    self.dream_theme_explorer()
                elif choice == 12:
                    self.search_dreams()
                elif choice == 13:
                    self.dream_statistics()
                elif choice == 14:
                    self.export_to_excel_with_analysis()
                elif choice == 15:
                    self.backup_data()
                elif choice == 16:
                    self.view_data_source_info()
                elif choice == 17:
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
    def load_data_from_excel(self):
        """Load data from Excel files"""
        print("\n📊 --- Load Data from Excel ---")
        
        try:
            excel_info = self.excel_handler.get_excel_file_info()
            
            print(f"Sleep Excel file: {'✅ Exists' if excel_info['sleep_file_exists'] else '❌ Not found'}")
            print(f"Performance Excel file: {'✅ Exists' if excel_info['performance_file_exists'] else '❌ Not found'}")
            
            if not excel_info['sleep_file_exists'] and not excel_info['performance_file_exists']:
                print("\n❌ No Excel files found!")
                print("💡 Tip: Use option 4 to create Excel templates first.")
                return
            
            print("\nWhat would you like to load?")
            print("1. Sleep data only")
            print("2. Performance data only")
            print("3. Both sleep and performance data")
            
            load_choice = get_valid_input("Enter choice (1-3): ", int, range(1, 4))
            
            if load_choice in [1, 3]:
                if excel_info['sleep_file_exists']:
                    new_sleep_entries = self.excel_handler.load_sleep_data_from_excel()
                    if new_sleep_entries:
                        # Ask whether to replace or merge
                        if self.sleep_analyzer.sleep_entries:
                            print(f"\n⚠️  You already have {len(self.sleep_analyzer.sleep_entries)} sleep entries.")
                            merge_choice = input("Replace existing data? (y/n): ").lower()
                            if merge_choice == 'y':
                                self.sleep_analyzer.sleep_entries = new_sleep_entries
                            else:
                                # Merge data (avoid duplicates by date)
                                existing_dates = [entry.date for entry in self.sleep_analyzer.sleep_entries]
                                new_entries = [entry for entry in new_sleep_entries if entry.date not in existing_dates]
                                self.sleep_analyzer.sleep_entries.extend(new_entries)
                                print(f"✅ Merged {len(new_entries)} new sleep entries")
                        else:
                            self.sleep_analyzer.sleep_entries = new_sleep_entries
                else:
                    print("❌ Sleep Excel file not found")
            
            if load_choice in [2, 3]:
                if excel_info['performance_file_exists']:
                    new_performance_entries = self.excel_handler.load_performance_data_from_excel()
                    if new_performance_entries:
                        # Ask whether to replace or merge
                        if self.sleep_analyzer.performance_entries:
                            print(f"\n⚠️  You already have {len(self.sleep_analyzer.performance_entries)} performance entries.")
                            merge_choice = input("Replace existing data? (y/n): ").lower()
                            if merge_choice == 'y':
                                self.sleep_analyzer.performance_entries = new_performance_entries
                            else:
                                # Merge data (avoid duplicates by date)
                                existing_dates = [entry.date for entry in self.sleep_analyzer.performance_entries]
                                new_entries = [entry for entry in new_performance_entries if entry.date not in existing_dates]
                                self.sleep_analyzer.performance_entries.extend(new_entries)
                                print(f"✅ Merged {len(new_entries)} new performance entries")
                        else:
                            self.sleep_analyzer.performance_entries = new_performance_entries
                else:
                    print("❌ Performance Excel file not found")
            
            # Switch to Excel as data source if data was loaded successfully
            if self.sleep_analyzer.sleep_entries or self.sleep_analyzer.performance_entries:
                self.data_source = "excel"
                print(f"\n✅ Data loaded successfully! Switched to Excel data source.")
            
        except Exception as e:
            print(f"Error loading data from Excel: {e}")
    
    @log_activity
    def create_excel_templates(self):
        """Create Excel template files"""
        print("\n📁 --- Create Excel Templates ---")
        
        try:
            self.excel_handler.create_template_files()
            
            excel_info = self.excel_handler.get_excel_file_info()
            
            print(f"\n📍 Excel files location:")
            print(f"Sleep data: {excel_info['sleep_file_path']}")
            print(f"Performance data: {excel_info['performance_file_path']}")
            
            print(f"\n📋 How to use Excel files:")
            print(f"1. Open the Excel files in your spreadsheet application")
            print(f"2. Add your data following the template format")
            print(f"3. Save the files")
            print(f"4. Use option 3 in this program to load the data")
            
            print(f"\n💡 Tips for Excel data entry:")
            print(f"• Date format: YYYY-MM-DD (e.g., 2024-01-15)")
            print(f"• Time format: HH:MM (e.g., 23:30)")
            print(f"• Ratings: Use numbers 1-10")
            print(f"• Dream emotions: Separate multiple emotions with commas")
            print(f"• Had_Dreams: Use TRUE or FALSE")
            print(f"• Save as .xlsx format")
            
        except Exception as e:
            print(f"Error creating Excel templates: {e}")
    
    @log_activity
    def switch_data_source(self):
        """Switch between text files and Excel as data source"""
        print("\n🔄 --- Switch Data Source ---")
        
        current_source = self.data_source
        
        print(f"Current data source: {current_source.upper()}")
        print("\nAvailable data sources:")
        print("1. Text files (.txt)")
        print("2. Excel files (.xlsx)")
        
        choice = get_valid_input("Choose new data source (1-2): ", int, range(1, 3))
        
        if choice == 1:
            new_source = "text"
        else:
            new_source = "excel"
        
        if new_source == current_source:
            print(f"Already using {new_source} as data source!")
            return
        
        # Ask user if they want to save current data before switching
        if self.sleep_analyzer.sleep_entries or self.sleep_analyzer.performance_entries:
            save_choice = input(f"Save current data to {current_source} before switching? (y/n): ").lower()
            if save_choice == 'y':
                self._save_data_to_current_source()
        
        # Switch source and reload data
        self.data_source = new_source
        
        try:
            if new_source == "excel":
                self.sleep_analyzer.sleep_entries = self.excel_handler.load_sleep_data_from_excel()
                self.sleep_analyzer.performance_entries = self.excel_handler.load_performance_data_from_excel()
            else:
                self.sleep_analyzer.sleep_entries = self.file_handler.load_sleep_data()
                self.sleep_analyzer.performance_entries = self.file_handler.load_performance_data()
            
            print(f"✅ Switched to {new_source.upper()} data source!")
            
        except Exception as e:
            print(f"Error switching data source: {e}")
            self.data_source = current_source  # Revert on error
    
    def _save_data_to_current_source(self):
        """Save data to current data source"""
        try:
            if self.data_source == "excel":
                if self.sleep_analyzer.sleep_entries:
                    self.excel_handler.save_sleep_data_to_excel(self.sleep_analyzer.sleep_entries)
                if self.sleep_analyzer.performance_entries:
                    self.excel_handler.save_performance_data_to_excel(self.sleep_analyzer.performance_entries)
            else:
                if self.sleep_analyzer.sleep_entries:
                    self.file_handler.save_sleep_data(self.sleep_analyzer.sleep_entries)
                if self.sleep_analyzer.performance_entries:
                    self.file_handler.save_performance_data(self.sleep_analyzer.performance_entries)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    @log_activity
    def record_sleep_data(self):
        """Record new sleep entry (terminal input)"""
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
            
            # Save to current data source
            if self.data_source == "excel":
                self.excel_handler.add_single_sleep_entry_to_excel(sleep_entry)
            else:
                self.file_handler.save_sleep_data(self.sleep_analyzer.sleep_entries)
            
            print("✅ Sleep data recorded successfully!")
            
        except Exception as e:
            print(f"Error recording sleep data: {e}")
    
    @log_activity
    def record_performance_data(self):
        """Record performance metrics for the day (terminal input)"""
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
            
            # Save to current data source
            if self.data_source == "excel":
                self.excel_handler.add_single_performance_entry_to_excel(performance_entry)
            else:
                self.file_handler.save_performance_data(self.sleep_analyzer.performance_entries)
            
            print("✅ Performance data recorded successfully!")
            
        except Exception as e:
            print(f"Error recording performance data: {e}")
    
    @log_activity
    def export_to_excel_with_analysis(self):
        """Export all data to Excel with comprehensive analysis"""
        print("\n📊 --- Export to Excel with Analysis ---")
        
        try:
            if not self.sleep_analyzer.sleep_entries and not self.sleep_analyzer.performance_entries:
                print("❌ No data available for export!")
                return
            
            export_file = self.excel_handler.export_to_excel_with_analysis(self.sleep_analyzer)
            
            print(f"\n✅ Comprehensive Excel export created!")
            print(f"📁 File location: {export_file}")
            print(f"\n📋 Export includes:")
            print(f"• Sleep data with calculated duration")
            print(f"• Performance data with overall scores")
            print(f"• Summary statistics")
            print(f"• Multiple sheets for easy analysis")
            
        except Exception as e:
            print(f"Error exporting to Excel: {e}")
    
    def view_data_source_info(self):
        """Display information about current data sources"""
        print("\n📊 --- Data Source Information ---")
        
        print(f"Current active source: {self.data_source.upper()}")
        
        # Text files info
        text_stats = self.file_handler.get_data_statistics()
        print(f"\n📄 TEXT FILES:")
        print(f"Sleep entries: {text_stats['sleep_entries']}")
        print(f"Performance entries: {text_stats['performance_entries']}")
        print(f"Sleep file size: {text_stats['sleep_file_size']} bytes")
        print(f"Performance file size: {text_stats['performance_file_size']} bytes")
        print(f"Last backup: {text_stats['last_backup']}")
        
        # Excel files info
        excel_info = self.excel_handler.get_excel_file_info()
        print(f"\n📊 EXCEL FILES:")
        print(f"Sleep entries: {excel_info['sleep_entries_count']}")
        print(f"Performance entries: {excel_info['performance_entries_count']}")
        print(f"Sleep file exists: {'✅' if excel_info['sleep_file_exists'] else '❌'}")
        print(f"Performance file exists: {'✅' if excel_info['performance_file_exists'] else '❌'}")
        
        # Current memory data
        print(f"\n💾 CURRENT LOADED DATA:")
        print(f"Sleep entries in memory: {len(self.sleep_analyzer.sleep_entries)}")
        print(f"Performance entries in memory: {len(self.sleep_analyzer.performance_entries)}")
    
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
        
        except Exception as e:
            print(f"Error generating dream statistics: {e}")
    
    def backup_data(self):
        """Backup all data"""
        try:
            self.file_handler.create_backup()
            print("✅ Text data backup created successfully!")
            
            # Also backup Excel files if they exist
            excel_info = self.excel_handler.get_excel_file_info()
            if excel_info['sleep_file_exists'] or excel_info['performance_file_exists']:
                # Create a backup export
                if self.sleep_analyzer.sleep_entries or self.sleep_analyzer.performance_entries:
                    self.excel_handler.export_to_excel_with_analysis(self.sleep_analyzer)
                    print("✅ Excel backup export created successfully!")
            
        except Exception as e:
            print(f"Error creating backup: {e}")
    
    def exit_program(self):
        """Clean exit with data save"""
        print("\n💾 Saving data and exiting...")
        try:
            # Save to both sources to ensure data persistence
            if self.sleep_analyzer.sleep_entries or self.sleep_analyzer.performance_entries:
                
                if self.data_source == "excel":
                    if self.sleep_analyzer.sleep_entries:
                        self.excel_handler.save_sleep_data_to_excel(self.sleep_analyzer.sleep_entries)
                    if self.sleep_analyzer.performance_entries:
                        self.excel_handler.save_performance_data_to_excel(self.sleep_analyzer.performance_entries)
                else:
                    if self.sleep_analyzer.sleep_entries:
                        self.file_handler.save_sleep_data(self.sleep_analyzer.sleep_entries)
                    if self.sleep_analyzer.performance_entries:
                        self.file_handler.save_performance_data(self.sleep_analyzer.performance_entries)
                
                print("✅ Data saved successfully!")
            
        except Exception as e:
            print(f"Error saving data: {e}")
        
        print("🌙 Thank you for using Sleep Analytics Platform with Excel Integration!")
        print("💡 Remember: You can now use Excel files for easier data entry!")

def main():
    """Program entry point"""
    try:
        # Check if pandas is available for Excel functionality
        import pandas as pd
        platform = SleepAnalyticsPlatform()
        platform.run()
    except ImportError:
        print("❌ Excel functionality requires pandas library.")
        print("Install with: pip install pandas openpyxl")
        print("Running with text-only mode...")
        # Fallback to original functionality
        from main import SleepAnalyticsPlatform as OriginalPlatform
        platform = OriginalPlatform()
        platform.run()

if __name__ == "__main__":
    main()
