# Backend Implementation Plan for Strategic Memo Results

## Overview

This plan outlines the backend components needed to support the "Single-Page Strategic Memo" results UI described in `results.md`. The goal is to transform raw A/B testing data into compelling, narrative-driven insights that provide actionable business intelligence.

## Current State Analysis

### What We Have ✅
- Session-based testing framework with persona diversity
- Comprehensive metrics collection (conversion rates, session lengths, etc.)
- Demographic analysis capabilities
- Structured logging system with detailed session data
- A/B comparison functionality
- Rich persona data with psychological profiles

### What We're Missing for the Strategic Memo ❌
- Executive summary headline generation
- Insight theme extraction and analysis
- "Voice of the User" quote extraction
- Psychological pattern identification
- Strategic narrative synthesis
- Theme-based failure mode categorization

## Core Backend Components to Build

### 1. Strategic Memo Data Generator (`strategic_memo_generator.py`)

**Purpose:** Transform raw session data into the structured format needed for the Strategic Memo UI.

**Key Methods:**
```python
class StrategicMemoGenerator:
    def generate_executive_headline(self, results: Dict) -> str
    def extract_primary_kpi(self, results: Dict) -> Dict
    def generate_persona_breakdown_chart(self, results: Dict) -> Dict
    def identify_insight_themes(self, session_logs: List[Dict]) -> List[Dict]
    def extract_voice_of_user_quotes(self, session_logs: List[Dict]) -> List[Dict]
    def generate_strategic_memo_data(self, test_results: Dict) -> Dict
```

### 2. Insight Theme Analyzer (`insight_analyzer.py`)

**Purpose:** Analyze session logs to identify psychological patterns and behavioral themes.

**Key Methods:**
```python
class InsightAnalyzer:
    def analyze_frustration_patterns(self, session_logs: List[Dict]) -> List[Dict]
    def identify_cognitive_load_issues(self, session_logs: List[Dict]) -> List[Dict]
    def extract_emotional_trajectories(self, session_logs: List[Dict]) -> List[Dict]
    def find_workflow_interruptions(self, session_logs: List[Dict]) -> List[Dict]
    def categorize_failure_modes(self, session_logs: List[Dict]) -> List[Dict]
    def detect_trust_issues(self, session_logs: List[Dict]) -> List[Dict]
    def identify_attention_distractions(self, session_logs: List[Dict]) -> List[Dict]
```

### 3. Quote Extractor (`quote_extractor.py`)

**Purpose:** Extract and curate the most representative "internal monologue" quotes from persona sessions.

**Key Methods:**
```python
class QuoteExtractor:
    def extract_reasoning_quotes(self, session_logs: List[Dict]) -> List[Dict]
    def find_representative_quotes(self, theme: str, session_logs: List[Dict]) -> List[Dict]
    def attribute_quotes_to_personas(self, quotes: List[Dict]) -> List[Dict]
    def rank_quotes_by_impact(self, quotes: List[Dict]) -> List[Dict]
    def filter_quotes_by_relevance(self, quotes: List[Dict], theme: str) -> List[Dict]
    def extract_abandonment_quotes(self, session_logs: List[Dict]) -> List[Dict]
```

## Data Flow Architecture

### Phase 1: Data Collection Enhancement

**Modify existing `ab_testing_framework.py`:**

1. **Enhance Session Logging**
   - Add `reasoning_text` field to capture full internal monologue
   - Add `emotional_state` field to track frustration/confidence
   - Add `focus_area` field to track what caught attention
   - Add `abandonment_reasoning` field for failed sessions
   - Add `cognitive_load_score` based on hesitation steps
   - Add `frustration_trajectory` tracking emotional state changes
   - Add `workflow_interruption_count` for UI friction measurement

2. **Enhanced Metrics Collection**
   ```python
   # In ABTestMetrics class
   def add_session_result(self, session_result: Dict):
       # Existing metrics...
       
       # New psychological metrics
       self.cognitive_load_scores.append(session_result.get("cognitive_load_score", 0))
       self.frustration_trajectories.append(session_result.get("frustration_trajectory", []))
       self.workflow_interruptions.append(session_result.get("workflow_interruption_count", 0))
       self.abandonment_reasonings.append(session_result.get("abandonment_reasoning", ""))
   ```

### Phase 2: Analysis Pipeline

**Create new analysis modules:**

1. **Psychological Pattern Detection**
   ```python
   # In insight_analyzer.py
   def detect_psychological_patterns(session_logs):
       patterns = {
           'frustration_build_up': [],
           'cognitive_overload': [],
           'trust_issues': [],
           'workflow_confusion': [],
           'attention_distraction': [],
           'decision_paralysis': [],
           'goal_confusion': []
       }
       
       for session in session_logs:
           reasoning_text = session.get('reasoning_text', '')
           emotional_trajectory = session.get('frustration_trajectory', [])
           
           # Analyze patterns in reasoning and emotional states
           if self._detect_frustration_build_up(emotional_trajectory):
               patterns['frustration_build_up'].append(session)
           
           if self._detect_cognitive_overload(reasoning_text):
               patterns['cognitive_overload'].append(session)
       
       return patterns
   ```

2. **Theme Synthesis**
   ```python
   # In strategic_memo_generator.py
   def synthesize_insight_themes(patterns, session_logs):
       themes = []
       
       for pattern_type, instances in patterns.items():
           if len(instances) > 0:  # Only create themes for detected patterns
               theme = {
                   'title': f"Theme: {self._format_theme_title(pattern_type)}",
                   'summary': self._generate_theme_summary(pattern_type, instances),
                   'impact_score': self._calculate_impact_score(instances),
                   'representative_quotes': self._extract_quotes_for_theme(pattern_type, instances),
                   'persona_breakdown': self._analyze_persona_impact(instances),
                   'recommendation': self._generate_theme_recommendation(pattern_type, instances)
               }
               themes.append(theme)
       
       # Sort themes by impact score
       themes.sort(key=lambda x: x['impact_score'], reverse=True)
       return themes
   ```

### Phase 3: Strategic Narrative Generation

**Create narrative synthesis:**

1. **Executive Headline Generation**
   ```python
   def generate_executive_headline(results):
       # Extract primary KPI improvement
       primary_kpi = results['ab_comparison']['primary_metric']
       improvement = results['ab_comparison']['improvement_percentage']
       
       # Identify top psychological factor
       top_theme = results['insight_themes'][0]
       theme_name = top_theme['title'].replace('Theme: ', '')
       
       # Generate headline based on improvement direction
       if improvement > 0:
           return f"Variant B Lifts {primary_kpi} by {improvement:.1f}% by Reducing {theme_name}"
       else:
           return f"Variant B Reduces {primary_kpi} by {abs(improvement):.1f}% Due to Increased {theme_name}"
   ```

2. **Primary KPI Calculation**
   ```python
   def calculate_primary_kpi(results):
       # Determine most impactful metric based on business priority
       metrics = ['conversion_rate', 'abandonment_rate', 'avg_session_length']
       impact_scores = [self._calculate_metric_impact(results, m) for m in metrics]
       primary_metric = metrics[impact_scores.index(max(impact_scores))]
       
       improvement = results['ab_comparison'].get(f'{primary_metric}_improvement', 0)
       
       return {
           'metric_name': primary_metric.replace('_', ' ').title(),
           'value': results['ab_comparison'][primary_metric],
           'improvement': improvement,
           'color': 'green' if improvement > 0 else 'red',
           'significance': self._calculate_statistical_significance(results, primary_metric)
       }
   ```

## Integration Points

### 1. Modify `analyze_results.py`

**Add strategic memo generation:**

```python
def generate_strategic_memo_report(sessions, kpis, demographic_analysis):
    """Generate the strategic memo data structure"""
    
    # Initialize generators
    memo_generator = StrategicMemoGenerator()
    insight_analyzer = InsightAnalyzer()
    quote_extractor = QuoteExtractor()
    
    # Generate strategic memo data
    strategic_data = {
        'headline': memo_generator.generate_executive_headline(kpis),
        'primary_kpi': memo_generator.extract_primary_kpi(kpis),
        'persona_breakdown': memo_generator.generate_persona_breakdown_chart(demographic_analysis),
        'insight_themes': insight_analyzer.analyze_all_patterns(sessions),
        'voice_of_user': quote_extractor.extract_all_quotes(sessions),
        'generated_at': datetime.now().isoformat(),
        'test_summary': {
            'total_sessions': len(sessions),
            'variant_a_sessions': len([s for s in sessions if s['variant'] == 'A']),
            'variant_b_sessions': len([s for s in sessions if s['variant'] == 'B']),
            'overall_conversion_rate': kpis['conversion_rate']
        }
    }
    
    return strategic_data
```

### 2. Enhance `ab_testing_framework.py`

**Add strategic memo output:**

```python
def generate_report(self, results: Dict) -> Dict:
    """Generate both traditional and strategic memo reports"""
    
    # Generate traditional report (existing)
    traditional_report = self._generate_traditional_report(results)
    
    # Generate strategic memo data (new)
    strategic_memo_data = self._generate_strategic_memo_data(results)
    
    return {
        'traditional_report': traditional_report,
        'strategic_memo_data': strategic_memo_data
    }

def _generate_strategic_memo_data(self, results: Dict) -> Dict:
    """Generate strategic memo data structure"""
    
    # Load session logs for detailed analysis
    session_logs = self._load_session_logs()
    
    # Initialize generators
    memo_generator = StrategicMemoGenerator()
    insight_analyzer = InsightAnalyzer()
    quote_extractor = QuoteExtractor()
    
    # Generate strategic memo components
    strategic_data = {
        'headline': memo_generator.generate_executive_headline(results),
        'primary_kpi': memo_generator.extract_primary_kpi(results),
        'persona_breakdown': memo_generator.generate_persona_breakdown_chart(results),
        'insight_themes': insight_analyzer.analyze_all_patterns(session_logs),
        'voice_of_user': quote_extractor.extract_all_quotes(session_logs)
    }
    
    return strategic_data
```

## Data Structure for Strategic Memo

### Expected Output Format:

```python
strategic_memo_data = {
    'headline': "Variant B Lifts Conversion Rate by 45.2% by Reducing Cognitive Overload",
    'primary_kpi': {
        'metric_name': 'Conversion Rate',
        'value': 78.5,
        'improvement': 45.2,
        'color': 'green',
        'significance': 'p < 0.001'
    },
    'persona_breakdown': {
        'chart_title': 'Conversion Rate by Persona Type',
        'data': [
            {'persona': 'New User', 'value': 85.2, 'color': 'green', 'sample_size': 150},
            {'persona': 'Power User', 'value': 72.1, 'color': 'red', 'sample_size': 120},
            {'persona': 'Cautious User', 'value': 68.3, 'color': 'red', 'sample_size': 80}
        ]
    },
    'insight_themes': [
        {
            'title': 'Theme: Workflow Interruption & Frustration',
            'summary': 'The new design introduced three extra steps to a previously simple task, causing significant frustration for experienced users who rely on muscle memory.',
            'impact_score': 8.5,
            'affected_sessions': 45,
            'persona_breakdown': {
                'Power User': 28,
                'New User': 12,
                'Cautious User': 5
            },
            'representative_quotes': [
                {
                    'quote': 'This is a step backward. My muscle memory for this task is completely broken. Why would they take a one-click action and bury it behind a menu? This is infuriating.',
                    'persona': 'The Power User',
                    'context': 'Frustration with workflow changes',
                    'session_id': 'session_20250729_123456'
                }
            ],
            'recommendation': 'Simplify the workflow by reducing the number of steps required for common actions, especially for power users.'
        }
    ],
    'voice_of_user': {
        'top_quotes': [
            {
                'quote': 'I just want to get this done quickly. Why is everything so complicated?',
                'persona': 'The Busy Professional',
                'theme': 'Frustration with Complexity',
                'impact_score': 9.2
            }
        ],
        'abandonment_quotes': [
            {
                'quote': 'I\'ve been trying to figure this out for 10 minutes. I give up.',
                'persona': 'The Novice User',
                'reason': 'Cognitive Overload',
                'session_length': 12
            }
        ]
    },
    'generated_at': '2025-01-27T10:30:00Z',
    'test_summary': {
        'total_sessions': 350,
        'variant_a_sessions': 175,
        'variant_b_sessions': 175,
        'overall_conversion_rate': 78.5
    }
}
```
