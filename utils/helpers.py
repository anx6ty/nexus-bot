from datetime import datetime, timedelta
from typing import Optional
import re

def format_time(seconds: int) -> str:
    """Convert seconds to readable time format."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes}m {secs}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def format_duration(ms: int) -> str:
    """Convert milliseconds to MM:SS or HH:MM:SS format."""
    seconds = ms // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"

def parse_time(time_str: str) -> Optional[int]:
    """Parse time string to seconds."""
    pattern = r"(\d+)\s*(s|m|h|d)"
    matches = re.findall(pattern, time_str.lower())
    
    if not matches:
        return None
    
    total_seconds = 0
    for value, unit in matches:
        value = int(value)
        if unit == 's':
            total_seconds += value
        elif unit == 'm':
            total_seconds += value * 60
        elif unit == 'h':
            total_seconds += value * 3600
        elif unit == 'd':
            total_seconds += value * 86400
    
    return total_seconds

def get_expire_time(seconds: int) -> datetime:
    """Get expiration time from now."""
    return datetime.utcnow() + timedelta(seconds=seconds)