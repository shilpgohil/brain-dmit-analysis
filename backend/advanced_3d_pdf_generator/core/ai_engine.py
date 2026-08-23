#!/usr/bin/env python3
"""
�� AI-Powered Content Generation Engine
======================================

Generates intelligent insights, recommendations, and content
automatically from DMIT analysis data.

Author: DMIT Research Team
Version: 3.0 - AI Enhancement
"""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class AIContentGenerator:
    """
    AI-powered content generation for DMIT reports.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def enhance_data(self, dmit_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enhance DMIT data with AI-generated insights and content.
        
        Args:
            dmit_data: Raw DMIT analysis data
            
        Returns:
            Enhanced data with AI-generated content
        """
        
        enhanced_data = dmit_data.copy()
        
        # Generate AI insights
        enhanced_data['ai_insights'] = self._generate_ai_insights(dmit_data)
        enhanced_data['career_recommendations'] = self._generate_career_recommendations(dmit_data)
        enhanced_data['development_plan'] = self._generate_development_plan(dmit_data)
        enhanced_data['personality_analysis'] = self._generate_personality_analysis(dmit_data)
        enhanced_data['executive_summary'] = self._generate_executive_summary(dmit_data)
        
        return enhanced_data
    
    def _generate_ai_insights(self, data: Dict[str, Any]) -> List[str]:
        """Generate AI-powered insights from intelligence scores"""
        
        insights = []
        intelligence_scores = data.get('intelligence_profile', {})
        
        if not intelligence_scores:
            return ["Analysis completed successfully with comprehensive intelligence mapping."]
        
        # Find dominant intelligence
        dominant = max(intelligence_scores.items(), key=lambda x: x[1]) if intelligence_scores else None
        
        if dominant:
            intel_type, score = dominant
            insights.append(f"Your dominant intelligence is {intel_type.replace('_', ' ').title()} ({score:.1f}%), indicating exceptional strength in this area.")
        
        # Generate pattern-based insights
        high_scores = [(k, v) for k, v in intelligence_scores.items() if v > 70]
        if len(high_scores) > 1:
            insights.append(f"You demonstrate exceptional strength in {len(high_scores)} intelligence areas, showing remarkable cognitive diversity.")
        
        # Balance insights
        score_range = max(intelligence_scores.values()) - min(intelligence_scores.values()) if intelligence_scores else 0
        if score_range < 20:
            insights.append("Your intelligence profile shows excellent balance across all areas, indicating versatile cognitive abilities.")
        elif score_range > 40:
            insights.append("Your intelligence profile shows distinct specialization, indicating focused cognitive strengths.")
        
        return insights
    
    def _generate_career_recommendations(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate AI-powered career recommendations"""
        
        recommendations = []
        intelligence_scores = data.get('intelligence_profile', {})
        
        # Career mapping based on intelligence types
        career_mapping = {
            'logical_mathematical': [
                {'title': 'Data Scientist', 'match': 95, 'description': 'Perfect for analytical thinking and problem-solving'},
                {'title': 'Software Engineer', 'match': 90, 'description': 'Excellent for logical reasoning and systematic approach'},
                {'title': 'Financial Analyst', 'match': 85, 'description': 'Great for numerical analysis and strategic thinking'}
            ],
            'linguistic_verbal': [
                {'title': 'Content Writer', 'match': 95, 'description': 'Perfect for communication and creative expression'},
                {'title': 'Marketing Manager', 'match': 90, 'description': 'Excellent for persuasive communication and strategy'},
                {'title': 'Public Relations', 'match': 85, 'description': 'Great for interpersonal communication and relationship building'}
            ],
            'spatial_visual': [
                {'title': 'Graphic Designer', 'match': 95, 'description': 'Perfect for visual creativity and spatial awareness'},
                {'title': 'Architect', 'match': 90, 'description': 'Excellent for spatial planning and design thinking'},
                {'title': 'Interior Designer', 'match': 85, 'description': 'Great for spatial arrangement and aesthetic sense'}
            ],
            'musical_rhythmic': [
                {'title': 'Music Producer', 'match': 95, 'description': 'Perfect for musical creativity and audio processing'},
                {'title': 'Sound Engineer', 'match': 90, 'description': 'Excellent for technical audio work and musical understanding'},
                {'title': 'Music Teacher', 'match': 85, 'description': 'Great for musical education and performance'}
            ],
            'bodily_kinesthetic': [
                {'title': 'Athletic Trainer', 'match': 95, 'description': 'Perfect for physical coordination and movement'},
                {'title': 'Physical Therapist', 'match': 90, 'description': 'Excellent for body mechanics and rehabilitation'},
                {'title': 'Dance Instructor', 'match': 85, 'description': 'Great for movement education and performance'}
            ],
            'interpersonal': [
                {'title': 'Human Resources Manager', 'match': 95, 'description': 'Perfect for people management and relationship building'},
                {'title': 'Sales Manager', 'match': 90, 'description': 'Excellent for persuasion and customer relationships'},
                {'title': 'Counselor', 'match': 85, 'description': 'Great for emotional intelligence and support'}
            ],
            'intrapersonal': [
                {'title': 'Life Coach', 'match': 95, 'description': 'Perfect for self-awareness and personal development'},
                {'title': 'Psychologist', 'match': 90, 'description': 'Excellent for understanding human behavior and emotions'},
                {'title': 'Leadership Consultant', 'match': 85, 'description': 'Great for self-reflection and strategic thinking'}
            ],
            'naturalistic': [
                {'title': 'Environmental Scientist', 'match': 95, 'description': 'Perfect for understanding natural systems and patterns'},
                {'title': 'Biologist', 'match': 90, 'description': 'Excellent for scientific research and natural observation'},
                {'title': 'Conservationist', 'match': 85, 'description': 'Great for environmental protection and sustainability'}
            ]
        }
        
        # Generate recommendations based on intelligence scores
        for intel_type, score in intelligence_scores.items():
            if intel_type in career_mapping and score > 60:
                for career in career_mapping[intel_type]:
                    # Adjust match percentage based on score
                    adjusted_match = min(100, career['match'] * (score / 100))
                    recommendations.append({
                        'title': career['title'],
                        'match_percentage': adjusted_match,
                        'description': career['description'],
                        'intelligence_type': intel_type,
                        'intelligence_score': score
                    })
        
        # Sort by match percentage and return top 10
        recommendations.sort(key=lambda x: x['match_percentage'], reverse=True)
        return recommendations[:10]
    
    def _generate_development_plan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered development plan"""
        intelligence_scores = data.get('intelligence_profile', {})
        plan = {}
        if not intelligence_scores:
            return plan
        # Find areas for development (scores below 50%)
        for intel_type, score in intelligence_scores.items():
            if score < 50:
                plan[intel_type] = {
                    'current_level': f"{score:.1f}%",
                    'target_level': "70%",
                    'description': f"Focus on enhancing your {intel_type.replace('_', ' ')} intelligence from current level of {score:.1f}%.",
                    'steps': [
                        f"Practice {intel_type.replace('_', ' ')} activities regularly.",
                        f"Seek feedback on {intel_type.replace('_', ' ')} performance.",
                        f"Set specific goals for {intel_type.replace('_', ' ')} improvement.",
                        f"Track progress in {intel_type.replace('_', ' ')} development."
                    ]
                }
        return plan
    
    def _generate_personality_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered personality analysis"""
        personality = data.get('personality_analysis', {})
        analysis = {}
        if not personality:
            return analysis
        for trait, score in personality.items():
            if score >= 80:
                level = "Very High"
            elif score >= 60:
                level = "High"
            elif score >= 40:
                level = "Moderate"
            elif score >= 20:
                level = "Low"
            else:
                level = "Very Low"
            analysis[trait] = {
                'score': score,
                'level': level,
                'description': f"{trait.replace('_', ' ').title()} is at a {level} level ({score:.1f}%)."
            }
        return analysis
    
    def _generate_executive_summary(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered executive summary"""
        summary = {}
        intelligence_scores = data.get('intelligence_profile', {})
        if not intelligence_scores:
            return summary
        dominant = max(intelligence_scores.items(), key=lambda x: x[1]) if intelligence_scores else None
        if dominant:
            intel_type, score = dominant
            summary['dominant_intelligence'] = {
                'type': intel_type,
                'score': score,
                'description': f"Dominant intelligence is {intel_type.replace('_', ' ').title()} with a score of {score:.1f}%."
            }
        # Add a brief summary of balance
        score_range = max(intelligence_scores.values()) - min(intelligence_scores.values()) if intelligence_scores else 0
        if score_range < 20:
            summary['balance'] = "Profile shows excellent balance across all intelligence areas."
        elif score_range > 40:
            summary['balance'] = "Profile shows distinct specialization in certain intelligence areas."
        else:
            summary['balance'] = "Profile shows moderate variation across intelligence areas."
        return summary 