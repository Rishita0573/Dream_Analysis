# __init__.py - Sleep Analytics Platform Package

"""
Sleep Analytics & Performance Platform

A comprehensive Python application for tracking and analyzing sleep patterns,
dream content, and daily performance metrics to optimize personal well-being.

Author: Rishita
Version: 1.0.0
Python Version: 3.6+

Modules:
- main: Main program entry point and user interface
- sleep_entry: Core classes for sleep and performance data
- file_handler: File operations and data persistence
- reports: Report generation and analysis
- utils: Utility functions, decorators, and helpers

Features:
- Sleep quality tracking and analysis
- Performance metrics monitoring
- Dream pattern analysis
- Correlation analysis between sleep and performance
- Automated report generation
- Data backup and recovery
- Personalized recommendations

Usage:
    python main.py

This project demonstrates advanced Python concepts including:
OOP, file handling, decorators, generators, iterators, exception handling,
and modular programming.
"""

__version__ = "1.0.0"
__author__ = "Rishita"
__email__ = "sharma.rishita0573@gmail.com"

# Import main classes for easy access
from .sleep_entry import SleepEntry, PerformanceEntry, SleepAnalyzer
from .file_handler import FileHandler
from .reports import ReportGenerator
from .utils import (
    log_activity, 
    timing_decorator, 
    get_valid_input, 
    create_range_validator,
    format_duration
)

# Package metadata
__all__ = [
    'SleepEntry',
    'PerformanceEntry', 
    'SleepAnalyzer',
    'FileHandler',
    'ReportGenerator',
    'log_activity',
    'timing_decorator',
    'get_valid_input',
    'create_range_validator',
    'format_duration'
]

# Package information
PACKAGE_INFO = {
    'name': 'Sleep Analytics Platform',
    'version': __version__,
    'description': 'Personal sleep and performance optimization tool',
    'python_requires': '>=3.6',
    'keywords': ['sleep', 'analytics', 'performance', 'health', 'tracking'],
    'features': [
        'Sleep quality tracking',
        'Performance monitoring', 
        'Dream analysis',
        'Correlation analysis',
        'Report generation',
        'Data visualization',
        'Backup system'
    ]
}