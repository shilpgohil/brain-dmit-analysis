#!/usr/bin/env python3
"""
TEST: SCIENTIFIC MAPPING VERIFICATION
=====================================
Verifies that the new Weighted Slot Aggregation logic correctly prioritizes
signals from the scientifically associated fingers (Table 1.1).
"""

import unittest
from dmit_intelligence_mapper import map_features_to_dmit_profile, FingerType
from integrated_dmit_pipeline import IntegratedDMITPipeline

class TestScientificMapping(unittest.TestCase):
    
    def setUp(self):
        self.pipeline = IntegratedDMITPipeline()
        
        # Create Mock Feature Sets
        # 1. High Logic Features (Whorls, etc.)
        self.features_high_logic = {
            'whorl_logical_layering_score': 0.9,
            'box_counting_dimension': 1.8, # norm -> 0.8
            'topological_complexity': 0.9,
            'ridge_flow_quality': 0.9
        }
        
        # 2. Low Logic Features (Arches, chaotic)
        self.features_low_logic = {
            'whorl_logical_layering_score': 0.1,
            'box_counting_dimension': 1.1, # norm -> 0.1
            'topological_complexity': 0.2,
            'ridge_flow_quality': 0.2
        }
        
    def test_logical_intelligence_source(self):
        """
        Verify Logical-Math score is driven by INDEX finger.
        """
        print("\nTesting Logical-Math Source (Expect Index Driven)...")
        
        # Profile A: High Logic Index, Low Logic Little
        prof_high_index = map_features_to_dmit_profile(self.features_high_logic, "index")
        prof_low_little = map_features_to_dmit_profile(self.features_low_logic, "little")
        
        # Mock Pipeline Result Structure
        results_a = [
            {'pipeline_info': {'finger_type': 'index'}, 'dmit_analysis': {'dmit_profile': prof_high_index}},
            {'pipeline_info': {'finger_type': 'little'}, 'dmit_analysis': {'dmit_profile': prof_low_little}}
        ]
        
        agg_a = self.pipeline._aggregate_results_scientifically(results_a)
        score_a = agg_a['aggregated_analysis']['dmit_profile']['multiple_intelligences']['logical_mathematical']
        print(f"CASE A (High Index, Low Little): Logical Score = {score_a:.2f}")
        
        # Profile B: Low Logic Index, High Logic Little
        prof_low_index = map_features_to_dmit_profile(self.features_low_logic, "index")
        prof_high_little = map_features_to_dmit_profile(self.features_high_logic, "little")
        
        results_b = [
            {'pipeline_info': {'finger_type': 'index'}, 'dmit_analysis': {'dmit_profile': prof_low_index}},
            {'pipeline_info': {'finger_type': 'little'}, 'dmit_analysis': {'dmit_profile': prof_high_little}}
        ]
        
        agg_b = self.pipeline._aggregate_results_scientifically(results_b)
        score_b = agg_b['aggregated_analysis']['dmit_profile']['multiple_intelligences']['logical_mathematical']
        print(f"CASE B (Low Index, High Little): Logical Score = {score_b:.2f}")
        
        # ASSERTION: Score A should be >> Score B
        # Because Index is the source of Logic. Little finger's logic score should be ignored.
        self.assertGreater(score_a, score_b + 0.3, "High Index should produce higher Logical Score than High Little")
        self.assertGreater(score_a, 0.7, "High Index should result in High Logical Score")
        self.assertLess(score_b, 0.4, "High Little (but Low Index) should result in Low Logical Score")

    def test_interpersonal_source(self):
        """
        Verify Interpersonal score is driven by THUMB.
        """
        print("\nTesting Interpersonal Source (Expect Thumb Driven)...")
        
        # Features for Interpersonal (Network Efficiency)
        feat_high = {'network_efficiency': 0.9, 'brain_criticality_score': 0.9, 'cross_spectral_fusion_score': 0.9}
        feat_low = {'network_efficiency': 0.1, 'brain_criticality_score': 0.1, 'cross_spectral_fusion_score': 0.1}
        
        # Case A: High Thumb
        res_a = [
            {'pipeline_info': {'finger_type': 'thumb'}, 'dmit_analysis': {'dmit_profile': map_features_to_dmit_profile(feat_high, 'thumb')}},
            {'pipeline_info': {'finger_type': 'ring'}, 'dmit_analysis': {'dmit_profile': map_features_to_dmit_profile(feat_low, 'ring')}}
        ]
        score_a = self.pipeline._aggregate_results_scientifically(res_a)['aggregated_analysis']['dmit_profile']['multiple_intelligences']['interpersonal']
        
        # Case B: Low Thumb
        res_b = [
            {'pipeline_info': {'finger_type': 'thumb'}, 'dmit_analysis': {'dmit_profile': map_features_to_dmit_profile(feat_low, 'thumb')}},
            {'pipeline_info': {'finger_type': 'ring'}, 'dmit_analysis': {'dmit_profile': map_features_to_dmit_profile(feat_high, 'ring')}}
        ]
        score_b = self.pipeline._aggregate_results_scientifically(res_b)['aggregated_analysis']['dmit_profile']['multiple_intelligences']['interpersonal']
        
        print(f"High Thumb Score: {score_a:.2f}")
        print(f"Low Thumb Score: {score_b:.2f}")
        
        self.assertGreater(score_a, score_b, "Thumb should drive Interpersonal score")

    def test_personality_pattern_correlation(self):
        """
        Verify Pattern Family impacts Personality Traits (from Research Paper).
        Whorl (2) -> High Conscientiousness/Openness (Individualistic)
        Loop (1) -> High Agreeableness/Neuroticism (Empathetic/Sensitive)
        """
        print("\nTesting Pattern-Personality Correlations...")
        
        # Mock Features: Whorl (Family 2)
        feat_whorl = {'pattern_family': 2, 'feature_stability': 0.5, 'entropy': 0.5}
        prof_whorl = map_features_to_dmit_profile(feat_whorl, "thumb")
        
        # Mock Features: Loop (Family 1)
        feat_loop = {'pattern_family': 1, 'feature_stability': 0.5, 'entropy': 0.5}
        prof_loop = map_features_to_dmit_profile(feat_loop, "thumb")
        
        # 1. Agreeableness: Loop should be higher (Empathy)
        agree_whorl = prof_whorl['personality_behavior']['agreeableness']
        agree_loop = prof_loop['personality_behavior']['agreeableness']
        print(f"Agreeableness: Whorl={agree_whorl:.2f}, Loop={agree_loop:.2f}")
        self.assertGreater(agree_loop, agree_whorl, "Loop should score higher on Agreeableness (Empathy)")
        
        # 2. Conscientiousness: Whorl should be higher (Perfectionist)
        # Note: Whorl gets +0.2 boost, Loop gets 0
        cons_whorl = prof_whorl['personality_behavior']['conscientiousness']
        cons_loop = prof_loop['personality_behavior']['conscientiousness']
        print(f"Conscientiousness: Whorl={cons_whorl:.2f}, Loop={cons_loop:.2f}")
        self.assertGreater(cons_whorl, cons_loop, "Whorl should score higher on Conscientiousness (Perfectionism)")

if __name__ == '__main__':
    unittest.main()
