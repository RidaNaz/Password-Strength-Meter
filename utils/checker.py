import re
import pandas as pd
from typing import Tuple, Dict

class PasswordAnalyzer:
    def __init__(self):
        self.common_passwords = set(pd.read_csv('common_passwords.txt', header=None)[0].str.strip())
    
    def calculate_entropy(self, password: str) -> float:
        """Calculate password entropy"""
        charset_size = 0
        if re.search(r'[a-z]', password): charset_size += 26
        if re.search(r'[A-Z]', password): charset_size += 26
        if re.search(r'\d', password): charset_size += 10
        if re.search(r'[!@#$%^&*]', password): charset_size += 8
        return len(password) * (charset_size ** 0.5)
    
    def analyze_password(self, password: str) -> Tuple[int, Dict, float]:
        """Comprehensive password analysis"""
        analysis = {
            'length': len(password) >= 8,
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'lowercase': bool(re.search(r'[a-z]', password)),
            'digit': bool(re.search(r'\d', password)),
            'special': bool(re.search(r'[!@#$%^&*]', password)),
            'common': password.lower() in self.common_passwords,
            'repeats': bool(re.search(r'(.)\1{2}', password)),
            'sequential': bool(re.search(r'(abc|123|xyz|\d{3})', password.lower()))
        }
        
        score = sum(analysis.values())
        entropy = self.calculate_entropy(password)
        
        # Adjust score based on advanced factors
        if len(password) >= 12: score += 1
        if entropy > 50: score += 1
        if analysis['common']: score = 0  # Instant fail
        
        return min(score, 10), analysis, entropy