import json
import os

class MBTIService:
    """Service for MBTI insights and compatibility data"""
    
    def __init__(self):
        # Load MBTI data
        data_path = os.path.join(os.path.dirname(__file__), '../../data/mbti_data.json')
        with open(data_path, 'r') as f:
            self.mbti_data = json.load(f)
        
        # Load compatibility data
        compat_path = os.path.join(os.path.dirname(__file__), '../../data/mbti_compatibility.json')
        with open(compat_path, 'r') as f:
            self.compatibility_data = json.load(f)
    
    def get_insights(self, mbti_type):
        """Get all insights for an MBTI type"""
        mbti_type = mbti_type.upper()
        
        if mbti_type not in self.mbti_data:
            return None
        
        data = self.mbti_data[mbti_type].copy()
        
        # Add compatibility info
        if mbti_type in self.compatibility_data:
            data['compatibility'] = self.compatibility_data[mbti_type]
        
        return data
    
    def get_compatibility(self, mbti_type):
        """Get compatibility information for an MBTI type"""
        mbti_type = mbti_type.upper()
        
        if mbti_type not in self.compatibility_data:
            return None
        
        return self.compatibility_data[mbti_type]
    
    def get_careers(self, mbti_type):
        """Get career suggestions for an MBTI type"""
        mbti_type = mbti_type.upper()
        
        if mbti_type not in self.mbti_data:
            return []
        
        return self.mbti_data[mbti_type].get('careers', [])
    
    def get_growth_tips(self, mbti_type):
        """Get growth tips for an MBTI type"""
        mbti_type = mbti_type.upper()
        
        if mbti_type not in self.mbti_data:
            return []
        
        return self.mbti_data[mbti_type].get('growth_tips', [])