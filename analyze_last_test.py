#!/usr/bin/env python3
"""
Analysis script for the last test with 4 users
"""

import json
import os
from datetime import datetime

def analyze_last_test():
    """Analyze only the 8 sessions from the last test with 4 users"""
    
    # Specific session files from the last test with Individualized Intents
    test_sessions = [
        "session_20250729173006_virtual customer 378_A.json",
        "session_20250729173010_virtual customer 182_A.json", 
        "session_20250729173035_virtual customer 399_A.json",
        "session_20250729173106_virtual customer 416_A.json",
        "session_20250729173116_virtual customer 378_B.json",
        "session_20250729173136_virtual customer 182_B.json",
        "session_20250729173211_virtual customer 399_B.json",
        "session_20250729173253_virtual customer 416_B.json"
    ]
    
    sessions = []
    for filename in test_sessions:
        filepath = os.path.join("logs", filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                session_data = json.load(f)
                sessions.append(session_data)
    
    # Separate variants
    variant_a_sessions = [s for s in sessions if s['variant'] == 'A']
    variant_b_sessions = [s for s in sessions if s['variant'] == 'B']
    
    print("=" * 60)
    print("🔬 LAST TEST ANALYSIS (4 Users)")
    print("=" * 60)
    print(f"📊 Total Sessions: {len(sessions)}")
    print(f"🔵 Variant A Sessions: {len(variant_a_sessions)}")
    print(f"🟡 Variant B Sessions: {len(variant_b_sessions)}")
    print("")
    
    # Variant A Analysis
    print("🔵 VARIANT A (Control - Current UI)")
    print("-" * 40)
    if variant_a_sessions:
        successful_a = [s for s in variant_a_sessions if s['success']]
        abandoned_a = [s for s in variant_a_sessions if 'abandoned' in s['final_outcome']]
        parsing_errors_a = [s for s in variant_a_sessions if s['final_outcome'] == 'parsing_error']
        misclicks_a = [s for s in variant_a_sessions if s['final_outcome'] == 'misclick']
        
        conversion_rate_a = len(successful_a) / len(variant_a_sessions) * 100
        abandonment_rate_a = len(abandoned_a) / len(variant_a_sessions) * 100
        parsing_error_rate_a = len(parsing_errors_a) / len(variant_a_sessions) * 100
        misclick_rate_a = len(misclicks_a) / len(variant_a_sessions) * 100
        
        # Calculate session lengths and hesitation
        session_lengths_a = [len(s.get('steps', [])) for s in variant_a_sessions]
        hesitation_steps_a = []
        for session in variant_a_sessions:
            total_hesitation = 0
            for step in session.get('steps', []):
                total_hesitation += step.get('hesitation_steps', 0)
            hesitation_steps_a.append(total_hesitation)
        
        avg_session_length_a = sum(session_lengths_a) / len(session_lengths_a)
        avg_hesitation_a = sum(hesitation_steps_a) / len(hesitation_steps_a)
        
        print(f"✅ Conversion Rate: {conversion_rate_a:.1f}% ({len(successful_a)}/{len(variant_a_sessions)})")
        print(f"🚪 Abandonment Rate: {abandonment_rate_a:.1f}% ({len(abandoned_a)}/{len(variant_a_sessions)})")
        print(f"❌ Parsing Error Rate: {parsing_error_rate_a:.1f}% ({len(parsing_errors_a)}/{len(variant_a_sessions)})")
        print(f"🎯 Misclick Rate: {misclick_rate_a:.1f}% ({len(misclicks_a)}/{len(variant_a_sessions)})")
        print(f"📏 Avg Session Length: {avg_session_length_a:.1f} steps")
        print(f"🧠 Avg Hesitation Steps: {avg_hesitation_a:.1f}")
        
        # Show individual session outcomes
        print("\n📋 Individual Session Outcomes:")
        for i, session in enumerate(variant_a_sessions, 1):
            persona_id = session.get('persona_id', 'unknown')
            outcome = session['final_outcome']
            steps = len(session.get('steps', []))
            print(f"  {i}. {persona_id}: {outcome} ({steps} steps)")
    
    print("")
    
    # Variant B Analysis
    print("🟡 VARIANT B (Treatment - Button Color Change)")
    print("-" * 40)
    if variant_b_sessions:
        successful_b = [s for s in variant_b_sessions if s['success']]
        abandoned_b = [s for s in variant_b_sessions if 'abandoned' in s['final_outcome']]
        parsing_errors_b = [s for s in variant_b_sessions if s['final_outcome'] == 'parsing_error']
        misclicks_b = [s for s in variant_b_sessions if s['final_outcome'] == 'misclick']
        
        conversion_rate_b = len(successful_b) / len(variant_b_sessions) * 100
        abandonment_rate_b = len(abandoned_b) / len(variant_b_sessions) * 100
        parsing_error_rate_b = len(parsing_errors_b) / len(variant_b_sessions) * 100
        misclick_rate_b = len(misclicks_b) / len(variant_b_sessions) * 100
        
        # Calculate session lengths and hesitation
        session_lengths_b = [len(s.get('steps', [])) for s in variant_b_sessions]
        hesitation_steps_b = []
        for session in variant_b_sessions:
            total_hesitation = 0
            for step in session.get('steps', []):
                total_hesitation += step.get('hesitation_steps', 0)
            hesitation_steps_b.append(total_hesitation)
        
        avg_session_length_b = sum(session_lengths_b) / len(session_lengths_b)
        avg_hesitation_b = sum(hesitation_steps_b) / len(hesitation_steps_b)
        
        print(f"✅ Conversion Rate: {conversion_rate_b:.1f}% ({len(successful_b)}/{len(variant_b_sessions)})")
        print(f"🚪 Abandonment Rate: {abandonment_rate_b:.1f}% ({len(abandoned_b)}/{len(variant_b_sessions)})")
        print(f"❌ Parsing Error Rate: {parsing_error_rate_b:.1f}% ({len(parsing_errors_b)}/{len(variant_b_sessions)})")
        print(f"🎯 Misclick Rate: {misclick_rate_b:.1f}% ({len(misclicks_b)}/{len(variant_b_sessions)})")
        print(f"📏 Avg Session Length: {avg_session_length_b:.1f} steps")
        print(f"🧠 Avg Hesitation Steps: {avg_hesitation_b:.1f}")
        
        # Show individual session outcomes
        print("\n📋 Individual Session Outcomes:")
        for i, session in enumerate(variant_b_sessions, 1):
            persona_id = session.get('persona_id', 'unknown')
            outcome = session['final_outcome']
            steps = len(session.get('steps', []))
            print(f"  {i}. {persona_id}: {outcome} ({steps} steps)")
    
    print("")
    
    # Comparison
    print("🔄 CONTROL VS TREATMENT COMPARISON")
    print("-" * 40)
    if variant_a_sessions and variant_b_sessions:
        successful_a = [s for s in variant_a_sessions if s['success']]
        successful_b = [s for s in variant_b_sessions if s['success']]
        
        conversion_rate_a = len(successful_a) / len(variant_a_sessions) * 100
        conversion_rate_b = len(successful_b) / len(variant_b_sessions) * 100
        
        conversion_diff = conversion_rate_b - conversion_rate_a
        conversion_improvement = (conversion_diff / conversion_rate_a * 100) if conversion_rate_a > 0 else 0
        
        print(f"🎯 Conversion Rate:")
        print(f"   Control (A): {conversion_rate_a:.1f}%")
        print(f"   Treatment (B): {conversion_rate_b:.1f}%")
        print(f"   Difference: {conversion_diff:+.1f} percentage points")
        print(f"   Relative Change: {conversion_improvement:+.1f}%")
        
        # Session length comparison
        session_lengths_a = [len(s.get('steps', [])) for s in variant_a_sessions]
        session_lengths_b = [len(s.get('steps', [])) for s in variant_b_sessions]
        
        avg_length_a = sum(session_lengths_a) / len(session_lengths_a)
        avg_length_b = sum(session_lengths_b) / len(session_lengths_b)
        
        print(f"\n📏 Session Length:")
        print(f"   Control (A): {avg_length_a:.1f} steps")
        print(f"   Treatment (B): {avg_length_b:.1f} steps")
        print(f"   Difference: {avg_length_b - avg_length_a:+.1f} steps")
    
    print("")
    print("=" * 60)

if __name__ == "__main__":
    analyze_last_test() 