# excel_handler.py - Excel Operations for Sleep Analytics Platform

import pandas as pd
import os
from datetime import datetime
from sleep_entry import SleepEntry, PerformanceEntry

class ExcelHandler:
    """Handle Excel operations for the Sleep Analytics Platform"""
    
    def __init__(self):
        self.data_dir = "data"
        self.excel_dir = os.path.join(self.data_dir, "excel")
        self.sleep_excel_file = os.path.join(self.excel_dir, "sleep_data.xlsx")
        self.performance_excel_file = os.path.join(self.excel_dir, "performance_data.xlsx")
        
        # Create directories if they don't exist
        self._create_directories()
        
        # Initialize Excel files if they don't exist
        self._initialize_excel_files()
    
    def _create_directories(self):
        """Create necessary directories"""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            os.makedirs(self.excel_dir, exist_ok=True)
        except OSError as e:
            print(f"Error creating directories: {e}")
    
    def _initialize_excel_files(self):
        """Initialize Excel files with headers if they don't exist"""
        # Sleep data Excel structure
        if not os.path.exists(self.sleep_excel_file):
            sleep_columns = [
                'Date', 'Bedtime', 'Wake_Time', 'Sleep_Quality', 
                'Had_Dreams', 'Dream_Content', 'Dream_Emotions'
            ]
            sleep_df = pd.DataFrame(columns=sleep_columns)
            sleep_df.to_excel(self.sleep_excel_file, index=False, sheet_name='Sleep_Data')
            print(f"Created new sleep Excel file: {self.sleep_excel_file}")
        
        # Performance data Excel structure
        if not os.path.exists(self.performance_excel_file):
            performance_columns = [
                'Date', 'Productivity', 'Mood', 'Energy_Level', 
                'Stress_Level', 'Activities', 'Notes'
            ]
            performance_df = pd.DataFrame(columns=performance_columns)
            performance_df.to_excel(self.performance_excel_file, index=False, sheet_name='Performance_Data')
            print(f"Created new performance Excel file: {self.performance_excel_file}")
    
    def create_template_files(self):
        """Create template Excel files with sample data for user reference"""
        try:
            # Sleep data template
            sleep_template_data = {
                'Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
                'Bedtime': ['23:00', '22:30', '23:15'],
                'Wake_Time': ['07:00', '06:45', '07:30'],
                'Sleep_Quality': [8, 7, 9],
                'Had_Dreams': [True, False, True],
                'Dream_Content': [
                    'Flying over mountains, feeling free and peaceful',
                    '',
                    'Swimming with dolphins in clear blue water'
                ],
                'Dream_Emotions': ['peaceful,happy,free', '', 'joyful,peaceful,excited']
            }
            
            sleep_template_df = pd.DataFrame(sleep_template_data)
            template_sleep_file = os.path.join(self.excel_dir, "sleep_data_template.xlsx")
            sleep_template_df.to_excel(template_sleep_file, index=False, sheet_name='Sleep_Data')
            
            # Performance data template
            performance_template_data = {
                'Date': ['2024-01-01', '2024-01-02', '2024-01-03'],
                'Productivity': [8, 6, 9],
                'Mood': [7, 5, 8],
                'Energy_Level': [8, 6, 9],
                'Stress_Level': [3, 7, 2],
                'Activities': [
                    'Work meetings, exercise, reading',
                    'Work, household chores',
                    'Creative projects, socializing'
                ],
                'Notes': [
                    'Great day overall, felt accomplished',
                    'Stressful day at work, tired',
                    'Very productive and energetic day'
                ]
            }
            
            performance_template_df = pd.DataFrame(performance_template_data)
            template_performance_file = os.path.join(self.excel_dir, "performance_data_template.xlsx")
            performance_template_df.to_excel(template_performance_file, index=False, sheet_name='Performance_Data')
            
            print(f"✅ Template files created:")
            print(f"   - {template_sleep_file}")
            print(f"   - {template_performance_file}")
            print(f"📝 You can use these templates to understand the expected format!")
            
        except Exception as e:
            print(f"Error creating template files: {e}")
    
    def load_sleep_data_from_excel(self):
        """Load sleep entries from Excel file"""
        sleep_entries = []
        
        try:
            if not os.path.exists(self.sleep_excel_file):
                print("No Excel sleep data file found.")
                return sleep_entries
            
            # Read Excel file
            df = pd.read_excel(self.sleep_excel_file, sheet_name='Sleep_Data')
            
            # Convert DataFrame to SleepEntry objects
            for index, row in df.iterrows():
                try:
                    # Handle missing or NaN values
                    date = str(row['Date']) if pd.notna(row['Date']) else ""
                    bedtime = str(row['Bedtime']) if pd.notna(row['Bedtime']) else "00:00"
                    wake_time = str(row['Wake_Time']) if pd.notna(row['Wake_Time']) else "00:00"
                    sleep_quality = int(row['Sleep_Quality']) if pd.notna(row['Sleep_Quality']) else 0
                    had_dreams = bool(row['Had_Dreams']) if pd.notna(row['Had_Dreams']) else False
                    dream_content = str(row['Dream_Content']) if pd.notna(row['Dream_Content']) else ""
                    
                    # Handle dream emotions
                    dream_emotions = []
                    if pd.notna(row['Dream_Emotions']) and str(row['Dream_Emotions']).strip():
                        emotions_str = str(row['Dream_Emotions'])
                        dream_emotions = [emotion.strip() for emotion in emotions_str.split(',') if emotion.strip()]
                    
                    # Skip empty rows
                    if not date or date == "nan":
                        continue
                    
                    # Convert date format if needed
                    if isinstance(row['Date'], pd.Timestamp):
                        date = row['Date'].strftime('%Y-%m-%d')
                    
                    entry = SleepEntry(
                        date=date,
                        bedtime=bedtime,
                        wake_time=wake_time,
                        sleep_quality=sleep_quality,
                        had_dreams=had_dreams,
                        dream_content=dream_content,
                        dream_emotions=dream_emotions
                    )
                    
                    sleep_entries.append(entry)
                    
                except Exception as e:
                    print(f"Error processing row {index + 1}: {e}")
                    continue
            
            print(f"✅ Loaded {len(sleep_entries)} sleep entries from Excel")
            
        except Exception as e:
            print(f"Error loading sleep data from Excel: {e}")
        
        return sleep_entries
    
    def load_performance_data_from_excel(self):
        """Load performance entries from Excel file"""
        performance_entries = []
        
        try:
            if not os.path.exists(self.performance_excel_file):
                print("No Excel performance data file found.")
                return performance_entries
            
            # Read Excel file
            df = pd.read_excel(self.performance_excel_file, sheet_name='Performance_Data')
            
            # Convert DataFrame to PerformanceEntry objects
            for index, row in df.iterrows():
                try:
                    # Handle missing or NaN values
                    date = str(row['Date']) if pd.notna(row['Date']) else ""
                    productivity = int(row['Productivity']) if pd.notna(row['Productivity']) else 0
                    mood = int(row['Mood']) if pd.notna(row['Mood']) else 0
                    energy_level = int(row['Energy_Level']) if pd.notna(row['Energy_Level']) else 0
                    stress_level = int(row['Stress_Level']) if pd.notna(row['Stress_Level']) else 0
                    activities = str(row['Activities']) if pd.notna(row['Activities']) else ""
                    notes = str(row['Notes']) if pd.notna(row['Notes']) else ""
                    
                    # Skip empty rows
                    if not date or date == "nan":
                        continue
                    
                    # Convert date format if needed
                    if isinstance(row['Date'], pd.Timestamp):
                        date = row['Date'].strftime('%Y-%m-%d')
                    
                    entry = PerformanceEntry(
                        date=date,
                        productivity=productivity,
                        mood=mood,
                        energy_level=energy_level,
                        stress_level=stress_level,
                        activities=activities,
                        notes=notes
                    )
                    
                    performance_entries.append(entry)
                    
                except Exception as e:
                    print(f"Error processing row {index + 1}: {e}")
                    continue
            
            print(f"✅ Loaded {len(performance_entries)} performance entries from Excel")
            
        except Exception as e:
            print(f"Error loading performance data from Excel: {e}")
        
        return performance_entries
    
    def save_sleep_data_to_excel(self, sleep_entries):
        """Save sleep entries to Excel file"""
        try:
            # Convert SleepEntry objects to DataFrame
            data = []
            for entry in sleep_entries:
                emotions_str = ','.join(entry.dream_emotions) if entry.dream_emotions else ""
                
                data.append({
                    'Date': entry.date,
                    'Bedtime': entry.bedtime,
                    'Wake_Time': entry.wake_time,
                    'Sleep_Quality': entry.sleep_quality,
                    'Had_Dreams': entry.had_dreams,
                    'Dream_Content': entry.dream_content,
                    'Dream_Emotions': emotions_str
                })
            
            df = pd.DataFrame(data)
            df.to_excel(self.sleep_excel_file, index=False, sheet_name='Sleep_Data')
            
            print(f"✅ Saved {len(sleep_entries)} sleep entries to Excel")
            
        except Exception as e:
            print(f"Error saving sleep data to Excel: {e}")
            raise
    
    def save_performance_data_to_excel(self, performance_entries):
        """Save performance entries to Excel file"""
        try:
            # Convert PerformanceEntry objects to DataFrame
            data = []
            for entry in performance_entries:
                data.append({
                    'Date': entry.date,
                    'Productivity': entry.productivity,
                    'Mood': entry.mood,
                    'Energy_Level': entry.energy_level,
                    'Stress_Level': entry.stress_level,
                    'Activities': entry.activities,
                    'Notes': entry.notes
                })
            
            df = pd.DataFrame(data)
            df.to_excel(self.performance_excel_file, index=False, sheet_name='Performance_Data')
            
            print(f"✅ Saved {len(performance_entries)} performance entries to Excel")
            
        except Exception as e:
            print(f"Error saving performance data to Excel: {e}")
            raise
    
    def add_single_sleep_entry_to_excel(self, sleep_entry):
        """Add a single sleep entry to existing Excel file"""
        try:
            # Read existing data
            existing_entries = self.load_sleep_data_from_excel()
            
            # Check if entry with same date already exists
            existing_dates = [entry.date for entry in existing_entries]
            if sleep_entry.date in existing_dates:
                print(f"⚠️  Entry for {sleep_entry.date} already exists. Updating...")
                # Remove existing entry
                existing_entries = [entry for entry in existing_entries if entry.date != sleep_entry.date]
            
            # Add new entry
            existing_entries.append(sleep_entry)
            
            # Sort by date
            existing_entries.sort(key=lambda x: x.date)
            
            # Save back to Excel
            self.save_sleep_data_to_excel(existing_entries)
            
            print(f"✅ Added/Updated sleep entry for {sleep_entry.date}")
            
        except Exception as e:
            print(f"Error adding sleep entry to Excel: {e}")
            raise
    
    def add_single_performance_entry_to_excel(self, performance_entry):
        """Add a single performance entry to existing Excel file"""
        try:
            # Read existing data
            existing_entries = self.load_performance_data_from_excel()
            
            # Check if entry with same date already exists
            existing_dates = [entry.date for entry in existing_entries]
            if performance_entry.date in existing_dates:
                print(f"⚠️  Entry for {performance_entry.date} already exists. Updating...")
                # Remove existing entry
                existing_entries = [entry for entry in existing_entries if entry.date != performance_entry.date]
            
            # Add new entry
            existing_entries.append(performance_entry)
            
            # Sort by date
            existing_entries.sort(key=lambda x: x.date)
            
            # Save back to Excel
            self.save_performance_data_to_excel(existing_entries)
            
            print(f"✅ Added/Updated performance entry for {performance_entry.date}")
            
        except Exception as e:
            print(f"Error adding performance entry to Excel: {e}")
            raise
    
    def export_to_excel_with_analysis(self, sleep_analyzer):
        """Export data with analysis to a comprehensive Excel file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_file = os.path.join(self.excel_dir, f"sleep_analysis_export_{timestamp}.xlsx")
            
            with pd.ExcelWriter(export_file, engine='openpyxl') as writer:
                # Sleep data sheet
                if sleep_analyzer.sleep_entries:
                    sleep_data = []
                    for entry in sleep_analyzer.sleep_entries:
                        emotions_str = ','.join(entry.dream_emotions) if entry.dream_emotions else ""
                        sleep_data.append({
                            'Date': entry.date,
                            'Bedtime': entry.bedtime,
                            'Wake_Time': entry.wake_time,
                            'Sleep_Duration_Hours': entry.sleep_duration,
                            'Sleep_Quality': entry.sleep_quality,
                            'Had_Dreams': entry.had_dreams,
                            'Dream_Content': entry.dream_content,
                            'Dream_Emotions': emotions_str
                        })
                    
                    sleep_df = pd.DataFrame(sleep_data)
                    sleep_df.to_excel(writer, sheet_name='Sleep_Data', index=False)
                
                # Performance data sheet
                if sleep_analyzer.performance_entries:
                    performance_data = []
                    for entry in sleep_analyzer.performance_entries:
                        performance_data.append({
                            'Date': entry.date,
                            'Productivity': entry.productivity,
                            'Mood': entry.mood,
                            'Energy_Level': entry.energy_level,
                            'Stress_Level': entry.stress_level,
                            'Overall_Score': entry.overall_score,
                            'Activities': entry.activities,
                            'Notes': entry.notes
                        })
                    
                    performance_df = pd.DataFrame(performance_data)
                    performance_df.to_excel(writer, sheet_name='Performance_Data', index=False)
                
                # Summary statistics sheet
                summary_data = []
                
                if sleep_analyzer.sleep_entries:
                    avg_quality = sleep_analyzer.calculate_average_sleep_quality()
                    avg_duration = sleep_analyzer.calculate_average_sleep_duration()
                    dream_frequency = sleep_analyzer.get_dream_frequency()
                    
                    summary_data.extend([
                        ['Metric', 'Value'],
                        ['Average Sleep Quality', f"{avg_quality}/10"],
                        ['Average Sleep Duration', f"{avg_duration} hours"],
                        ['Dream Frequency', f"{dream_frequency}%"],
                        ['Total Sleep Entries', len(sleep_analyzer.sleep_entries)]
                    ])
                
                if sleep_analyzer.performance_entries:
                    avg_performance = sleep_analyzer.calculate_average_performance()
                    summary_data.extend([
                        ['', ''],
                        ['Average Productivity', f"{avg_performance.get('productivity', 0)}/10"],
                        ['Average Mood', f"{avg_performance.get('mood', 0)}/10"],
                        ['Average Energy', f"{avg_performance.get('energy', 0)}/10"],
                        ['Average Stress', f"{avg_performance.get('stress', 0)}/10"],
                        ['Total Performance Entries', len(sleep_analyzer.performance_entries)]
                    ])
                
                if summary_data:
                    summary_df = pd.DataFrame(summary_data[1:], columns=summary_data[0])
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            print(f"✅ Comprehensive Excel export created: {export_file}")
            return export_file
            
        except Exception as e:
            print(f"Error creating Excel export: {e}")
            raise
    
    def get_excel_file_info(self):
        """Get information about Excel files"""
        info = {
            'sleep_file_exists': os.path.exists(self.sleep_excel_file),
            'performance_file_exists': os.path.exists(self.performance_excel_file),
            'sleep_file_path': self.sleep_excel_file,
            'performance_file_path': self.performance_excel_file,
            'sleep_entries_count': 0,
            'performance_entries_count': 0
        }
        
        try:
            if info['sleep_file_exists']:
                df = pd.read_excel(self.sleep_excel_file, sheet_name='Sleep_Data')
                info['sleep_entries_count'] = len(df.dropna(subset=['Date']))
        except Exception as e:
            print(f"Error reading sleep Excel file: {e}")
        
        try:
            if info['performance_file_exists']:
                df = pd.read_excel(self.performance_excel_file, sheet_name='Performance_Data')
                info['performance_entries_count'] = len(df.dropna(subset=['Date']))
        except Exception as e:
            print(f"Error reading performance Excel file: {e}")
        
        return info
    
    def validate_excel_format(self, file_path, data_type='sleep'):
        """Validate Excel file format"""
        try:
            df = pd.read_excel(file_path)
            
            if data_type == 'sleep':
                required_columns = ['Date', 'Bedtime', 'Wake_Time', 'Sleep_Quality', 'Had_Dreams']
                optional_columns = ['Dream_Content', 'Dream_Emotions']
            else:  # performance
                required_columns = ['Date', 'Productivity', 'Mood', 'Energy_Level', 'Stress_Level']
                optional_columns = ['Activities', 'Notes']
            
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                print(f"❌ Missing required columns: {missing_columns}")
                return False
            
            print(f"✅ Excel file format is valid for {data_type} data")
            return True
            
        except Exception as e:
            print(f"Error validating Excel file: {e}")
            return False
