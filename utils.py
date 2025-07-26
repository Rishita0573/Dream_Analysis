# utils.py - Utility Functions and Decorators for Sleep Analytics Platform

import os
import time
from datetime import datetime
from functools import wraps

# Decorator for logging function calls
def log_activity(func):
    """Decorator to log function activities"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Executing: {func.__name__}")
        
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = round(end_time - start_time, 3)
            print(f"[{timestamp}] Completed: {func.__name__} (took {duration}s)")
            return result
        except Exception as e:
            end_time = time.time()
            duration = round(end_time - start_time, 3)
            print(f"[{timestamp}] Error in {func.__name__} after {duration}s: {e}")
            raise
    return wrapper

# Decorator for timing functions
def timing_decorator(func):
    """Decorator to measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"⏱️  {func.__name__} executed in {duration:.3f} seconds")
        return result
    return wrapper

# Decorator for input validation
def validate_input(validation_func):
    """Decorator to validate function inputs"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not validation_func(*args, **kwargs):
                raise ValueError(f"Invalid input for function {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Closure for creating specialized validators
def create_range_validator(min_val, max_val):
    """Create a range validator using closure"""
    def validator(value):
        try:
            num_value = float(value)
            return min_val <= num_value <= max_val
        except (ValueError, TypeError):
            return False
    return validator

def create_date_validator():
    """Create a date validator using closure"""
    def validator(date_string):
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    return validator

def create_time_validator():
    """Create a time validator using closure"""
    def validator(time_string):
        try:
            datetime.strptime(time_string, "%H:%M")
            return True
        except ValueError:
            return False
    return validator

# Input validation functions
def get_valid_input(prompt, input_type=str, valid_range=None, validator=None):
    """Get valid input from user with type checking and validation"""
    while True:
        try:
            user_input = input(prompt)
            
            # Convert to required type
            if input_type == int:
                converted_input = int(user_input)
            elif input_type == float:
                converted_input = float(user_input)
            else:
                converted_input = user_input.strip()
            
            # Check range if provided
            if valid_range is not None:
                if hasattr(valid_range, '__contains__'):  # Range or list
                    if converted_input not in valid_range:
                        print(f"Please enter a value in range: {valid_range}")
                        continue
                elif hasattr(valid_range, '__call__'):  # Function
                    if not valid_range(converted_input):
                        print("Invalid input. Please try again.")
                        continue
            
            # Custom validator
            if validator and not validator(converted_input):
                print("Invalid input format. Please try again.")
                continue
            
            return converted_input
        
        except ValueError as e:
            print(f"Invalid input type. Expected {input_type.__name__}. Please try again.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise
        except Exception as e:
            print(f"Error: {e}. Please try again.")

def get_valid_date(prompt="Enter date (YYYY-MM-DD): "):
    """Get valid date input"""
    date_validator = create_date_validator()
    return get_valid_input(prompt, str, validator=date_validator)

def get_valid_time(prompt="Enter time (HH:MM): "):
    """Get valid time input"""
    time_validator = create_time_validator()
    return get_valid_input(prompt, str, validator=time_validator)

def get_valid_rating(prompt, min_val=1, max_val=10):
    """Get valid rating input"""
    range_validator = create_range_validator(min_val, max_val)
    return get_valid_input(prompt, int, validator=range_validator)

def clear_screen():
    """Clear the screen (cross-platform)"""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_for_user():
    """Pause and wait for user to press Enter"""
    input("\nPress Enter to continue...")

def format_duration(hours):
    """Format duration in a readable format"""
    if hours == 0:
        return "0 hours"
    elif hours < 1:
        minutes = int(hours * 60)
        return f"{minutes} minutes"
    else:
        whole_hours = int(hours)
        minutes = int((hours - whole_hours) * 60)
        if minutes == 0:
            return f"{whole_hours} hour{'s' if whole_hours != 1 else ''}"
        else:
            return f"{whole_hours}h {minutes}m"

def format_percentage(value, total):
    """Format percentage with proper handling of zero division"""
    if total == 0:
        return "0%"
    percentage = (value / total) * 100
    return f"{percentage:.1f}%"

def create_progress_bar(current, total, width=30):
    """Create a simple text-based progress bar"""
    if total == 0:
        return "[" + "=" * width + "] 100%"
    
    progress = current / total
    filled_width = int(width * progress)
    bar = "=" * filled_width + "-" * (width - filled_width)
    percentage = progress * 100
    return f"[{bar}] {percentage:.1f}%"

def create_simple_chart(data_dict, max_width=40):
    """Create a simple horizontal bar chart"""
    if not data_dict:
        return "No data to display"
    
    max_value = max(data_dict.values()) if data_dict.values() else 1
    chart_lines = []
    
    for label, value in data_dict.items():
        # Calculate bar width
        if max_value > 0:
            bar_width = int((value / max_value) * max_width)
        else:
            bar_width = 0
        
        # Create bar
        bar = "█" * bar_width
        chart_lines.append(f"{label:15} | {bar} {value}")
    
    return "\n".join(chart_lines)

def safe_divide(numerator, denominator, default=0):
    """Safely divide two numbers, returning default if division by zero"""
    try:
        if denominator == 0:
            return default
        return numerator / denominator
    except (TypeError, ValueError):
        return default

def safe_average(numbers):
    """Safely calculate average of a list of numbers"""
    if not numbers:
        return 0
    try:
        return sum(numbers) / len(numbers)
    except (TypeError, ValueError):
        return 0

def truncate_text(text, max_length=50, suffix="..."):
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def format_list_display(items, max_items=5):
    """Format a list for display, showing only top items"""
    if not items:
        return "None"
    
    if len(items) <= max_items:
        return ", ".join(str(item) for item in items)
    else:
        shown_items = items[:max_items]
        remaining = len(items) - max_items
        formatted = ", ".join(str(item) for item in shown_items)
        return f"{formatted} and {remaining} more..."

# Data analysis helper functions
def calculate_trend(values):
    """Calculate simple trend (increasing, decreasing, stable)"""
    if len(values) < 2:
        return "Insufficient data"
    
    # Simple trend calculation
    increases = 0
    decreases = 0
    
    for i in range(1, len(values)):
        if values[i] > values[i-1]:
            increases += 1
        elif values[i] < values[i-1]:
            decreases += 1
    
    if increases > decreases:
        return "Improving"
    elif decreases > increases:
        return "Declining"
    else:
        return "Stable"

def find_outliers(values, threshold=2):
    """Find outliers in a list of values using simple threshold method"""
    if len(values) < 3:
        return []
    
    mean_val = safe_average(values)
    outliers = []
    
    for value in values:
        if abs(value - mean_val) > threshold:
            outliers.append(value)
    
    return outliers

def get_statistics_summary(values):
    """Get basic statistics summary for a list of values"""
    if not values:
        return {
            'count': 0,
            'min': 0,
            'max': 0,
            'average': 0,
            'trend': 'No data'
        }
    
    return {
        'count': len(values),
        'min': min(values),
        'max': max(values),
        'average': round(safe_average(values), 2),
        'trend': calculate_trend(values)
    }

# File utility functions
def ensure_directory_exists(directory):
    """Ensure directory exists, create if it doesn't"""
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except OSError as e:
        print(f"Error creating directory {directory}: {e}")
        return False

def get_file_age_days(filepath):
    """Get age of file in days"""
    try:
        if not os.path.exists(filepath):
            return -1
        
        file_time = os.path.getmtime(filepath)
        current_time = time.time()
        age_seconds = current_time - file_time
        age_days = age_seconds / (24 * 3600)
        return round(age_days, 1)
    except OSError:
        return -1