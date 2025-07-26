# file_handler.py - File Operations for Sleep Analytics Platform

import os
import copy
from datetime import datetime
from sleep_entry import SleepEntry, PerformanceEntry

class FileHandler:
    """Handle all file operations for the platform"""
    
    def __init__(self):
        self.data_dir = "data"
        self.backup_dir = os.path.join(self.data_dir, "backup")
        self.reports_dir = os.path.join(self.data_dir, "reports")
        self.sleep_file = os.path.join(self.data_dir, "sleep_data.txt")
        self.performance_file = os.path.join(self.data_dir, "performance_data.txt")
        
        # Create directories if they don't exist
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary directories"""
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            os.makedirs(self.backup_dir, exist_ok=True)
            os.makedirs(self.reports_dir, exist_ok=True)
        except OSError as e:
            print(f"Error creating directories: {e}")
    
    def save_sleep_data(self, sleep_entries):
        """Save sleep entries to file"""
        try:
            with open(self.sleep_file, 'w', encoding='utf-8') as file:
                for entry in sleep_entries:
                    # Convert to string format for saving
                    emotions_str = ','.join(entry.dream_emotions) if entry.dream_emotions else ""
                    
                    line = f"{entry.date}|{entry.bedtime}|{entry.wake_time}|{entry.sleep_quality}|{entry.had_dreams}|{entry.dream_content}|{emotions_str}\n"
                    file.write(line)
            
            print(f"Sleep data saved: {len(sleep_entries)} entries")
        
        except IOError as e:
            print(f"Error saving sleep data: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error saving sleep data: {e}")
            raise
    
    def load_sleep_data(self):
        """Load sleep entries from file"""
        sleep_entries = []
        
        try:
            if not os.path.exists(self.sleep_file):
                print("No existing sleep data found. Starting fresh.")
                return sleep_entries
            
            with open(self.sleep_file, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    try:
                        line = line.strip()
                        if not line:
                            continue
                        
                        parts = line.split('|')
                        if len(parts) != 7:
                            print(f"Warning: Invalid format in line {line_num}, skipping")
                            continue
                        
                        date, bedtime, wake_time, sleep_quality, had_dreams, dream_content, emotions_str = parts
                        
                        # Convert data types
                        sleep_quality = int(sleep_quality)
                        had_dreams = had_dreams.lower() == 'true'
                        dream_emotions = emotions_str.split(',') if emotions_str else []
                        dream_emotions = [emotion.strip() for emotion in dream_emotions if emotion.strip()]
                        
                        entry = SleepEntry(date, bedtime, wake_time, sleep_quality,
                                         had_dreams, dream_content, dream_emotions)
                        sleep_entries.append(entry)
                    
                    except (ValueError, IndexError) as e:
                        print(f"Error parsing line {line_num}: {e}")
                        continue
            
            print(f"Loaded {len(sleep_entries)} sleep entries")
        
        except FileNotFoundError:
            print("Sleep data file not found. Starting fresh.")
        except IOError as e:
            print(f"Error loading sleep data: {e}")
        except Exception as e:
            print(f"Unexpected error loading sleep data: {e}")
        
        return sleep_entries
    
    def save_performance_data(self, performance_entries):
        """Save performance entries to file"""
        try:
            with open(self.performance_file, 'w', encoding='utf-8') as file:
                for entry in performance_entries:
                    line = f"{entry.date}|{entry.productivity}|{entry.mood}|{entry.energy_level}|{entry.stress_level}|{entry.activities}|{entry.notes}\n"
                    file.write(line)
            
            print(f"Performance data saved: {len(performance_entries)} entries")
        
        except IOError as e:
            print(f"Error saving performance data: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error saving performance data: {e}")
            raise
    
    def load_performance_data(self):
        """Load performance entries from file"""
        performance_entries = []
        
        try:
            if not os.path.exists(self.performance_file):
                print("No existing performance data found. Starting fresh.")
                return performance_entries
            
            with open(self.performance_file, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    try:
                        line = line.strip()
                        if not line:
                            continue
                        
                        parts = line.split('|')
                        if len(parts) != 7:
                            print(f"Warning: Invalid format in line {line_num}, skipping")
                            continue
                        
                        date, productivity, mood, energy_level, stress_level, activities, notes = parts
                        
                        # Convert data types
                        productivity = int(productivity)
                        mood = int(mood)
                        energy_level = int(energy_level)
                        stress_level = int(stress_level)
                        
                        entry = PerformanceEntry(date, productivity, mood, energy_level,
                                               stress_level, activities, notes)
                        performance_entries.append(entry)
                    
                    except (ValueError, IndexError) as e:
                        print(f"Error parsing line {line_num}: {e}")
                        continue
            
            print(f"Loaded {len(performance_entries)} performance entries")
        
        except FileNotFoundError:
            print("Performance data file not found. Starting fresh.")
        except IOError as e:
            print(f"Error loading performance data: {e}")
        except Exception as e:
            print(f"Unexpected error loading performance data: {e}")
        
        return performance_entries
    
    def save_report(self, report_content):
        """Save analysis report to file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_filename = f"sleep_analysis_report_{timestamp}.txt"
            report_path = os.path.join(self.reports_dir, report_filename)
            
            with open(report_path, 'w', encoding='utf-8') as file:
                file.write(f"Sleep Analytics Report - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("=" * 80 + "\n\n")
                file.write(report_content)
            
            print(f"Report saved as: {report_filename}")
        
        except IOError as e:
            print(f"Error saving report: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error saving report: {e}")
            raise
    
    def create_backup(self):
        """Create backup of all data files"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Backup sleep data
            if os.path.exists(self.sleep_file):
                backup_sleep_file = os.path.join(self.backup_dir, f"sleep_data_backup_{timestamp}.txt")
                self._copy_file(self.sleep_file, backup_sleep_file)
            
            # Backup performance data
            if os.path.exists(self.performance_file):
                backup_performance_file = os.path.join(self.backup_dir, f"performance_data_backup_{timestamp}.txt")
                self._copy_file(self.performance_file, backup_performance_file)
            
            print(f"Backup created with timestamp: {timestamp}")
        
        except Exception as e:
            print(f"Error creating backup: {e}")
            raise
    
    def _copy_file(self, source, destination):
        """Copy file from source to destination"""
        try:
            with open(source, 'r', encoding='utf-8') as src:
                content = src.read()
            
            with open(destination, 'w', encoding='utf-8') as dst:
                dst.write(content)
        
        except IOError as e:
            print(f"Error copying file from {source} to {destination}: {e}")
            raise
    
    def get_data_statistics(self):
        """Get statistics about data files"""
        stats = {
            'sleep_entries': 0,
            'performance_entries': 0,
            'sleep_file_size': 0,
            'performance_file_size': 0,
            'last_backup': 'Never'
        }
        
        try:
            # Count sleep entries
            if os.path.exists(self.sleep_file):
                with open(self.sleep_file, 'r', encoding='utf-8') as file:
                    stats['sleep_entries'] = sum(1 for line in file if line.strip())
                stats['sleep_file_size'] = os.path.getsize(self.sleep_file)
            
            # Count performance entries
            if os.path.exists(self.performance_file):
                with open(self.performance_file, 'r', encoding='utf-8') as file:
                    stats['performance_entries'] = sum(1 for line in file if line.strip())
                stats['performance_file_size'] = os.path.getsize(self.performance_file)
            
            # Check last backup
            if os.path.exists(self.backup_dir):
                backup_files = os.listdir(self.backup_dir)
                if backup_files:
                    backup_files.sort(reverse=True)
                    latest_backup = backup_files[0]
                    # Extract timestamp from filename
                    if '_' in latest_backup:
                        timestamp_part = latest_backup.split('_')[-1].replace('.txt', '')
                        try:
                            backup_date = datetime.strptime(timestamp_part, "%Y%m%d_%H%M%S")
                            stats['last_backup'] = backup_date.strftime("%Y-%m-%d %H:%M:%S")
                        except ValueError:
                            pass
        
        except Exception as e:
            print(f"Error getting data statistics: {e}")
        
        return stats