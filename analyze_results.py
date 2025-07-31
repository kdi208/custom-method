#!/usr/bin/env python3
"""
Comprehensive Analysis Script for A/B Testing Results
Extracts and analyzes all KPIs and metrics from session logs
"""

import json
import os
import statistics
from collections import defaultdict
from datetime import datetime

def load_session_logs(logs_dir="results"):
    """Load all session logs from the logs directory"""
    sessions = []
    for filename in os.listdir(logs_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(logs_dir, filename)
            with open(filepath, 'r') as f:
                session_data = json.load(f)
                sessions.append(session_data)
    return sessions

def analyze_demographics(sessions, personas_data):
    """Analyze performance by demographic segments"""
    demographic_analysis = {
        'age_groups': defaultdict(list),
        'genders': defaultdict(list),
        'income_groups': defaultdict(list)
    }
    
    for session in sessions:
        persona_id = session.get('persona_id', 'unknown')
        if persona_id in personas_data:
            persona = personas_data[persona_id]
            
            # Age group analysis
            if persona.get('age_group'):
                steps_taken = len(session.get('steps', []))
                total_hesitation = sum(step.get('hesitation_steps', 0) for step in session.get('steps', []))
                demographic_analysis['age_groups'][persona['age_group']].append({
                    'success': session['success'],
                    'steps_taken': steps_taken,
                    'hesitation': total_hesitation,
                    'outcome': session['final_outcome']
                })
            
            # Gender analysis
            if persona.get('gender'):
                steps_taken = len(session.get('steps', []))
                total_hesitation = sum(step.get('hesitation_steps', 0) for step in session.get('steps', []))
                demographic_analysis['genders'][persona['gender']].append({
                    'success': session['success'],
                    'steps_taken': steps_taken,
                    'hesitation': total_hesitation,
                    'outcome': session['final_outcome']
                })
            
            # Income group analysis
            if persona.get('income_group'):
                steps_taken = len(session.get('steps', []))
                total_hesitation = sum(step.get('hesitation_steps', 0) for step in session.get('steps', []))
                demographic_analysis['income_groups'][persona['income_group']].append({
                    'success': session['success'],
                    'steps_taken': steps_taken,
                    'hesitation': total_hesitation,
                    'outcome': session['final_outcome']
                })
    
    return demographic_analysis

def load_personas_data():
    """Load persona data from JSON files"""
    personas = {}
    persona_dir = "data/example_data/personas/json/"
    
    for filename in os.listdir(persona_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(persona_dir, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                persona_id = filename.replace('.json', '')
                personas[persona_id] = {
                    'age_group': data.get('age_group'),
                    'gender': data.get('gender'),
                    'income_group': data.get('income_group'),
                    'intent': data.get('intent')
                }
    
    return personas

def calculate_kpis(sessions):
    """Calculate comprehensive KPIs from session data"""
    kpis = {
        'total_sessions': len(sessions),
        'variant_a_sessions': len([s for s in sessions if s['variant'] == 'A']),
        'variant_b_sessions': len([s for s in sessions if s['variant'] == 'B']),
        
        # Conversion Metrics
        'conversion_rate': 0,
        'abandonment_rate': 0,
        'parsing_error_rate': 0,
        'misclick_rate': 0,
        
        # Behavioral Metrics
        'avg_session_length': 0,
        'avg_hesitation_steps': 0,
        'max_session_length': 0,
        'min_session_length': 0,
        
        # Outcome Breakdown
        'outcomes': defaultdict(int),
        'variant_a_outcomes': defaultdict(int),
        'variant_b_outcomes': defaultdict(int),
        
        # Top/Bottom Performers
        'top_performing_personas': [],
        'bottom_performing_personas': []
    }
    
    if sessions:
        # Calculate rates
        successful_sessions = [s for s in sessions if s['success']]
        abandoned_sessions = [s for s in sessions if 'abandoned' in s['final_outcome']]
        parsing_errors = [s for s in sessions if s['final_outcome'] == 'parsing_error']
        misclicks = [s for s in sessions if s['final_outcome'] == 'misclick']
        
        kpis['conversion_rate'] = len(successful_sessions) / len(sessions) * 100
        kpis['abandonment_rate'] = len(abandoned_sessions) / len(sessions) * 100
        kpis['parsing_error_rate'] = len(parsing_errors) / len(sessions) * 100
        kpis['misclick_rate'] = len(misclicks) / len(sessions) * 100
        
        # Calculate averages from session logs
        session_lengths = [len(s.get('steps', [])) for s in sessions]
        hesitation_steps = []
        for session in sessions:
            total_hesitation = 0
            steps = session.get('steps', [])
            for step in steps:
                total_hesitation += step.get('hesitation_steps', 0)
            hesitation_steps.append(total_hesitation)
        
        kpis['avg_session_length'] = statistics.mean(session_lengths)
        kpis['avg_hesitation_steps'] = statistics.mean(hesitation_steps)
        kpis['max_session_length'] = max(session_lengths)
        kpis['min_session_length'] = min(session_lengths)
        
        # Outcome breakdown
        for session in sessions:
            kpis['outcomes'][session['final_outcome']] += 1
            if session['variant'] == 'A':
                kpis['variant_a_outcomes'][session['final_outcome']] += 1
            else:
                kpis['variant_b_outcomes'][session['final_outcome']] += 1
    
    return kpis

def generate_comprehensive_report(sessions, kpis, demographic_analysis):
    """Generate a comprehensive report with all KPIs and insights"""
    
    report = []
    report.append("# Comprehensive A/B Testing Analysis Report")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"**Total Sessions Analyzed:** {kpis['total_sessions']}")
    report.append("")
    
    # Executive Summary
    report.append("## 📊 Executive Summary")
    report.append(f"- **Overall Conversion Rate:** {kpis['conversion_rate']:.1f}%")
    report.append(f"- **Abandonment Rate:** {kpis['abandonment_rate']:.1f}%")
    report.append(f"- **Average Session Length:** {kpis['avg_session_length']:.1f} steps")
    report.append(f"- **Average Hesitation:** {kpis['avg_hesitation_steps']:.1f} reasoning steps")
    report.append("")
    
    # Primary Business Metrics
    report.append("## 🎯 Primary Business Metrics")
    report.append("### Conversion & Abandonment")
    report.append(f"- **Conversion Rate:** {kpis['conversion_rate']:.1f}%")
    report.append(f"- **Abandonment Rate:** {kpis['abandonment_rate']:.1f}%")
    report.append(f"- **Parsing Error Rate:** {kpis['parsing_error_rate']:.1f}%")
    report.append(f"- **Misclick Rate:** {kpis['misclick_rate']:.1f}%")
    report.append("")
    
    # Behavioral & UX Metrics
    report.append("## 🧠 Behavioral & UX Metrics")
    report.append("### Session Analysis")
    report.append(f"- **Average Session Length:** {kpis['avg_session_length']:.1f} steps")
    report.append(f"- **Average Hesitation Steps:** {kpis['avg_hesitation_steps']:.1f}")
    report.append(f"- **Session Length Range:** {kpis['min_session_length']} - {kpis['max_session_length']} steps")
    report.append("")
    
    # A/B Test Comparison
    report.append("## 🔄 A/B Test Comparison")
    report.append("### Variant A (Current UI)")
    for outcome, count in kpis['variant_a_outcomes'].items():
        rate = count / kpis['variant_a_sessions'] * 100
        report.append(f"- **{outcome.replace('_', ' ').title()}:** {count} sessions ({rate:.1f}%)")
    report.append("")
    
    report.append("### Variant B (Button Color Change)")
    for outcome, count in kpis['variant_b_outcomes'].items():
        rate = count / kpis['variant_b_sessions'] * 100
        report.append(f"- **{outcome.replace('_', ' ').title()}:** {count} sessions ({rate:.1f}%)")
    report.append("")
    
    # Demographic Analysis
    report.append("## 👥 Demographic Analysis")
    
    # Age Groups
    if demographic_analysis['age_groups']:
        report.append("### Performance by Age Group")
        for age_group, sessions in demographic_analysis['age_groups'].items():
            success_rate = sum(1 for s in sessions if s['success']) / len(sessions) * 100
            avg_steps = statistics.mean([s['steps_taken'] for s in sessions])
            avg_hesitation = statistics.mean([s['hesitation'] for s in sessions])
            report.append(f"- **{age_group}:** {success_rate:.1f}% success, {avg_steps:.1f} steps, {avg_hesitation:.1f} hesitation")
        report.append("")
    
    # Gender
    if demographic_analysis['genders']:
        report.append("### Performance by Gender")
        for gender, sessions in demographic_analysis['genders'].items():
            success_rate = sum(1 for s in sessions if s['success']) / len(sessions) * 100
            avg_steps = statistics.mean([s['steps_taken'] for s in sessions])
            avg_hesitation = statistics.mean([s['hesitation'] for s in sessions])
            report.append(f"- **{gender.title()}:** {success_rate:.1f}% success, {avg_steps:.1f} steps, {avg_hesitation:.1f} hesitation")
        report.append("")
    
    # Income Groups
    if demographic_analysis['income_groups']:
        report.append("### Performance by Income Group")
        for income_group, sessions in demographic_analysis['income_groups'].items():
            success_rate = sum(1 for s in sessions if s['success']) / len(sessions) * 100
            avg_steps = statistics.mean([s['steps_taken'] for s in sessions])
            avg_hesitation = statistics.mean([s['hesitation'] for s in sessions])
            report.append(f"- **{income_group}:** {success_rate:.1f}% success, {avg_steps:.1f} steps, {avg_hesitation:.1f} hesitation")
        report.append("")
    
    # Detailed Session Analysis
    report.append("## 📋 Detailed Session Analysis")
    report.append("### Outcome Distribution")
    for outcome, count in kpis['outcomes'].items():
        rate = count / kpis['total_sessions'] * 100
        report.append(f"- **{outcome.replace('_', ' ').title()}:** {count} sessions ({rate:.1f}%)")
    report.append("")
    
    # Top and Bottom Performers
    report.append("## 🏆 Performance Rankings")
    
    # Group sessions by persona
    persona_performance = defaultdict(list)
    for session in sessions:
        persona_id = session.get('persona_id', 'unknown')
        persona_performance[persona_id].append(session)
    
    # Calculate persona-level metrics
    persona_metrics = []
    for persona_id, persona_sessions in persona_performance.items():
        success_rate = sum(1 for s in persona_sessions if s['success']) / len(persona_sessions) * 100
        
        # Calculate steps and hesitation from session logs
        steps_list = []
        hesitation_list = []
        for session in persona_sessions:
            steps = session.get('steps', [])
            steps_list.append(len(steps))
            total_hesitation = sum(step.get('hesitation_steps', 0) for step in steps)
            hesitation_list.append(total_hesitation)
        
        avg_steps = statistics.mean(steps_list)
        avg_hesitation = statistics.mean(hesitation_list)
        
        persona_metrics.append({
            'persona_id': persona_id,
            'success_rate': success_rate,
            'avg_steps': avg_steps,
            'avg_hesitation': avg_hesitation,
            'total_sessions': len(persona_sessions)
        })
    
    # Sort by success rate
    persona_metrics.sort(key=lambda x: x['success_rate'], reverse=True)
    
    report.append("### Top 5 Performing Personas")
    for i, persona in enumerate(persona_metrics[:5], 1):
        report.append(f"{i}. **{persona['persona_id']}:** {persona['success_rate']:.1f}% success, {persona['avg_steps']:.1f} steps")
    
    report.append("")
    report.append("### Bottom 5 Performing Personas")
    for i, persona in enumerate(persona_metrics[-5:], 1):
        report.append(f"{i}. **{persona['persona_id']}:** {persona['success_rate']:.1f}% success, {persona['avg_steps']:.1f} steps")
    
    report.append("")
    
    # Recommendations
    report.append("## 💡 Key Insights & Recommendations")
    report.append("### What the Data Tells Us:")
    
    if kpis['conversion_rate'] == 0:
        report.append("- **No conversions observed:** This suggests the current UI state doesn't match the personas' intents")
        report.append("- **High abandonment rate:** Users are correctly identifying when their goals can't be achieved")
        report.append("- **Agent behavior is rational:** The AI is making appropriate decisions to terminate impossible tasks")
    
    if kpis['avg_hesitation_steps'] > 5:
        report.append(f"- **High cognitive load:** Average {kpis['avg_hesitation_steps']:.1f} reasoning steps suggests complex decision-making")
    
    if kpis['parsing_error_rate'] > 0:
        report.append(f"- **LLM reliability:** {kpis['parsing_error_rate']:.1f}% parsing errors indicate potential prompt optimization opportunities")
    
    report.append("")
    report.append("### Next Steps:")
    report.append("1. **Test with matching UI state:** Run tests where personas' intents align with available actions")
    report.append("2. **Expand persona diversity:** Test with larger, more diverse persona samples")
    report.append("3. **Analyze demographic patterns:** Investigate any significant differences in performance by age, gender, or income")
    report.append("4. **Optimize prompts:** Reduce parsing errors and hesitation steps through prompt engineering")
    
    return "\n".join(report)

def main():
    """Main analysis function"""
    print("🔍 Loading session logs...")
    sessions = load_session_logs()
    
    if not sessions:
        print("❌ No session logs found in the logs directory")
        return
    
    print(f"📊 Analyzing {len(sessions)} sessions...")
    
    # Load persona data for demographic analysis
    personas_data = load_personas_data()
    
    # Calculate KPIs
    kpis = calculate_kpis(sessions)
    
    # Analyze demographics
    demographic_analysis = analyze_demographics(sessions, personas_data)
    
    # Generate comprehensive report
    report = generate_comprehensive_report(sessions, kpis, demographic_analysis)
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"comprehensive_analysis_{timestamp}.md"
    
    with open(report_filename, 'w') as f:
        f.write(report)
    
    print(f"✅ Comprehensive analysis saved to: {report_filename}")
    
    # Print key metrics to console
    print("\n" + "="*60)
    print("📈 KEY METRICS SUMMARY:")
    print("="*60)
    print(f"🎯 Conversion Rate: {kpis['conversion_rate']:.1f}%")
    print(f"🚪 Abandonment Rate: {kpis['abandonment_rate']:.1f}%")
    print(f"📏 Avg Session Length: {kpis['avg_session_length']:.1f} steps")
    print(f"🧠 Avg Hesitation: {kpis['avg_hesitation_steps']:.1f} steps")
    print(f"❌ Parsing Errors: {kpis['parsing_error_rate']:.1f}%")
    print(f"🎯 Misclicks: {kpis['misclick_rate']:.1f}%")
    print("="*60)

if __name__ == "__main__":
    main() 