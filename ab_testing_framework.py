#!/usr/bin/env python3
"""
A/B Testing Framework for AI Agent UI Evaluation
Implements quantifiable metrics to measure UI effectiveness for AI agents
"""

import google.generativeai as genai
import pyautogui
import json
import os
import time
import webbrowser
import statistics
from datetime import datetime
from PIL import Image
from dotenv import load_dotenv
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import random
import re

# --- Configuration and Setup ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

# Ensure directories exist
os.makedirs("logs", exist_ok=True)
os.makedirs("screenshots/variant_a", exist_ok=True)
os.makedirs("screenshots/variant_b", exist_ok=True)

@dataclass
class Persona:
    """Represents a specific user persona for testing."""
    name: str
    description: str
    primary_goal: str  # This will now hold the 'intent'
    
    # --- New demographic fields ---
    age_group: Optional[str] = None
    gender: Optional[str] = None
    income_group: Optional[str] = None
    
    # --- Deprecated fields, made optional ---
    behavioral_pattern: Optional[str] = ""
    core_test_question: Optional[str] = ""
    expected_processing_time: Optional[str] = ""
    
    # --- Add persona ID for logging ---
    persona_id: Optional[str] = None

class ABTestMetrics:
    """Core metrics for A/B testing AI agent UI performance"""
    
    def __init__(self):
        self.task_success_rate = 0.0
        self.error_rate = 0.0
        self.misinterpretation_errors = 0 # Kept for single test comparison
        self.navigation_errors = 0 # Kept for single test comparison
        self.hallucination_errors = 0 # Kept for single test comparison
        
        # --- Session-based metrics ---
        self.abandoned_sessions = 0
        self.parsing_errors = 0
        self.misclick_errors = 0
        self.session_lengths = []
        self.hesitation_steps = []

        # --- Timing metrics ---
        self.processing_times = []
        self.capture_times = []
        self.ai_processing_times = []
        self.parse_times = []

        self.confidence_scores = []
        self.total_tests = 0 # Represents total sessions now
        self.successful_tests = 0 # Represents successful sessions
    
    def add_session_result(self, session_result: Dict):
        """Add a session result to the metrics"""
        self.total_tests += 1
        
        if session_result["success"]:
            self.successful_tests += 1
        else:
            outcome = session_result.get("outcome", "unknown_error")
            if "abandoned" in outcome:
                self.abandoned_sessions += 1
            elif outcome == "parsing_error":
                self.parsing_errors += 1
            elif outcome == "misclick":
                self.misclick_errors += 1
        
        self.session_lengths.append(session_result.get("steps_taken", 0))
        self.hesitation_steps.append(session_result.get("total_hesitation", 0))

        # Update rates
        if self.total_tests > 0:
            self.task_success_rate = self.successful_tests / self.total_tests
            self.error_rate = 1 - self.task_success_rate

    def add_result(self, success: bool, error_type: str = None, 
                   processing_time: float = 0.0, capture_time: float = 0.0,
                   ai_processing_time: float = 0.0, parse_time: float = 0.0,
                   confidence: float = None):
        """Add a test result to the metrics"""
        self.total_tests += 1
        self.processing_times.append(processing_time)
        self.capture_times.append(capture_time)
        self.ai_processing_times.append(ai_processing_time)
        self.parse_times.append(parse_time)
        
        if confidence is not None:
            self.confidence_scores.append(confidence)
        
        if success:
            self.successful_tests += 1
        else:
            self.error_rate += 1
            if error_type == "misinterpretation":
                self.misinterpretation_errors += 1
            elif error_type == "navigation":
                self.navigation_errors += 1
            elif error_type == "hallucination":
                self.hallucination_errors += 1
        
        # Update rates
        self.task_success_rate = self.successful_tests / self.total_tests
        self.error_rate = 1 - self.task_success_rate
    
    def get_summary(self) -> Dict:
        """Get a summary of all metrics"""
        summary = {
            "task_success_rate": round(self.task_success_rate * 100, 2),
            "total_sessions": self.total_tests,
            "successful_sessions": self.successful_tests,
            "abandoned_sessions": self.abandoned_sessions,
            "parsing_errors": self.parsing_errors,
            "misclick_errors": self.misclick_errors,
            "avg_session_length": round(statistics.mean(self.session_lengths), 2) if self.session_lengths else 0,
            "avg_hesitation_steps": round(statistics.mean(self.hesitation_steps), 2) if self.hesitation_steps else 0,
        }
        # Add old metrics for compatibility if they exist
        if self.processing_times:
            summary.update({
                "avg_processing_time": round(statistics.mean(self.processing_times), 2),
                "avg_capture_time": round(statistics.mean(self.capture_times), 2),
                "avg_ai_processing_time": round(statistics.mean(self.ai_processing_times), 2),
                "avg_parse_time": round(statistics.mean(self.parse_times), 2),
            })
        return summary

class ABTestingFramework:
    """Main A/B testing framework for AI agent UI evaluation"""
    
    def __init__(self, num_personas: int = 10):
        self.metrics_a = ABTestMetrics()
        self.metrics_b = ABTestMetrics()
        self.personas = self._load_personas(num_personas)
        self.elements_map = self._load_elements_map()
    
    def _load_elements_map(self, filename: str = "elements.json") -> List[Dict]:
        """Load the UI elements map"""
        with open(filename, 'r') as f:
            return json.load(f)
    
    def _extract_name_from_description(self, description: str) -> str:
        """Extracts the persona name from the description string."""
        if not description:
            return "Unknown Persona"
        first_line = description.split('\n')[0]
        match = re.match(r"Persona: (.*)", first_line)
        if match:
            return match.group(1).strip()
        return "Unknown Persona"

    def _load_personas(self, num_personas: int) -> List[Persona]:
        """Load a random sample of personas from the data directory."""
        persona_dir = "data/example_data/personas/json/"
        if not os.path.isdir(persona_dir):
            print(f"Error: Persona directory not found at {persona_dir}")
            return []
        
        all_persona_files = [f for f in os.listdir(persona_dir) if f.endswith('.json')]
        
        if len(all_persona_files) < num_personas:
            print(f"Warning: Requested {num_personas} personas, but only found {len(all_persona_files)}. Using all available.")
            num_personas = len(all_persona_files)

        if num_personas == 0:
            return []

        sampled_files = random.sample(all_persona_files, num_personas)
        
        loaded_personas = []
        for filename in sampled_files:
            filepath = os.path.join(persona_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                description = data.get("persona", "")
                name = self._extract_name_from_description(description)
                
                persona = Persona(
                    persona_id=filename.replace('.json', ''),
                    name=name,
                    description=description,
                    primary_goal=data.get("intent", ""),
                    age_group=data.get("age_group"),
                    gender=data.get("gender"),
                    income_group=data.get("income_group")
                )
                loaded_personas.append(persona)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load or parse persona file {filename}. Skipping. Error: {e}")

        print(f"Successfully loaded {len(loaded_personas)} personas.")
        return loaded_personas

    def _create_prompt(self, persona: Persona, history: List[Dict]) -> str:
        """Create a persona-aware, session-aware prompt for the AI agent."""
        
        # Base prompt explaining the agent's core task
        base_prompt = f"""
You are an AI agent testing a webpage UI. Your goal is to choose the single best action that corresponds to the user's intent, taking into account the user's persona.
You will be given a screenshot and a JSON list of all clickable elements on the screen.
"""
        
        # Persona context
        persona_prompt = f"""
PERSONA CONTEXT:
You are acting as: {persona.name}
Description: {persona.description}
Primary Goal for this session: {persona.primary_goal}
"""

        # Session history to provide context of previous actions
        history_prompt = ""
        if history:
            history_prompt = "SESSION HISTORY (Your previous actions):\n"
            for i, entry in enumerate(history):
                history_prompt += f"{i+1}. You chose to click '{entry['action']['text']}' ({entry['action']['context']}).\n"
            history_prompt += "\n"

        # The core task, including the prompt for step-by-step reasoning
        user_intent_prompt = f"""
USER'S INTENT: "{persona.primary_goal}"

AVAILABLE CLICKABLE ELEMENTS:
{json.dumps(self.elements_map, indent=2)}

First, provide your step-by-step reasoning for your next action as a numbered list. This is for analysis of your cognitive process.
REASONING:
1. [Your first thought]
2. [Your second thought]
...

Finally, provide the JSON for your chosen action. Your response MUST be ONLY the JSON object for the single element you have decided to click. You can also choose to terminate the session if you believe the goal is complete or cannot be achieved.
To terminate, respond with: {{"action": "terminate"}}

ACTION:
"""
        
        return base_prompt + persona_prompt + history_prompt + user_intent_prompt

    def capture_screen(self, filename="screenshot.png") -> str:
        """Capture the current screen"""
        pyautogui.screenshot().save(filename)
        return filename
    
    def _validate_action(self, agent_action: Dict) -> bool:
        """Validates if the agent's chosen action exists in the elements map."""
        if not agent_action or "text" not in agent_action:
            return False # Invalid action format

        action_text = agent_action.get("text")
        
        # Allow terminate action
        if action_text == "terminate":
            return True

        for element in self.elements_map:
            if element.get("text") == action_text:
                return True
        return False

    def run_session(self, persona: Persona, variant: str = "A", max_steps: int = 5) -> Dict:
        """
        Run a multi-step session for a given persona.
        A session continues until the task is complete, abandoned, or an error occurs.
        """
        session_id = f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}_{persona.persona_id}_{variant}"
        print(f"\n🚀 Starting Session: {session_id}")
        print(f"   Persona: {persona.name} ({persona.persona_id})")
        print(f"   Intent: {persona.primary_goal}")

        history = []
        session_log = {
            "session_id": session_id,
            "persona_id": persona.persona_id,
            "intent": persona.primary_goal,
            "variant": variant,
            "steps": []
        }
        
        session_success = False
        final_outcome = "unknown"
        total_hesitation_steps = 0
        
        for step_num in range(max_steps):
            print(f"   - Step {step_num + 1}/{max_steps}...")
            step_log = {"step_number": step_num + 1}

            # Capture screen
            capture_start = time.time()
            screenshot_file = self.capture_screen(f"screenshots/{variant}_{step_num}.png")
            image = Image.open(screenshot_file)
            step_log["screenshot_file"] = screenshot_file
            capture_time = time.time() - capture_start

            # Create prompt
            prompt = self._create_prompt(persona, history)
            step_log["prompt"] = prompt
            
            # --- LLM Interaction with Retry Logic ---
            agent_action = None
            raw_response = ""
            parsing_attempts = 3
            for attempt in range(parsing_attempts):
                try:
                    # print("     - 🧠 Agent thinking...")
                    ai_start = time.time()
                    response = model.generate_content([prompt, image])
                    raw_response = response.text
                    step_log["raw_llm_response"] = raw_response
                    ai_processing_time = time.time() - ai_start
                    
                    # Extract Reasoning and Action
                    action_json_str = re.search(r"ACTION:\s*(\{.*\})", raw_response, re.DOTALL)
                    if not action_json_str:
                        raise json.JSONDecodeError("Action block not found.", raw_response, 0)
                    
                    agent_action = json.loads(action_json_str.group(1))
                    step_log["parsed_action"] = agent_action

                    reasoning_str = re.search(r"REASONING:(.*?)ACTION:", raw_response, re.DOTALL)
                    hesitation_steps = len(re.findall(r"^\s*\d+\.\s", reasoning_str.group(1), re.MULTILINE)) if reasoning_str else 0
                    total_hesitation_steps += hesitation_steps
                    step_log["hesitation_steps"] = hesitation_steps
                    
                    break # Success, exit retry loop
                except (json.JSONDecodeError, AttributeError) as e:
                    print(f"     - ⚠️ LLM output parsing failed (Attempt {attempt + 1}/{parsing_attempts}). Error: {e}")
                    raw_response = getattr(e, 'doc', raw_response) # Store faulty response
                    prompt += "\n\nYour last response was not valid JSON. Please correct your thinking and provide the action in the correct format."
                    agent_action = None
                    step_log["error"] = f"Parsing failed on attempt {attempt + 1}: {e}"

            session_log["steps"].append(step_log)
            
            if agent_action is None:
                print("     - ❌ Session failed due to persistent parsing errors.")
                final_outcome = "parsing_error"
                break

            # Validate action
            is_misclick = not self._validate_action(agent_action)
            if is_misclick:
                print(f"     - ❌ Misclick detected. Agent chose non-existent element: {agent_action.get('text')}")
                final_outcome = "misclick"
                break
            
            # Check for termination by agent
            if agent_action.get("action") == "terminate":
                print(f"     - 🛑 Agent chose to terminate the session.")
                final_outcome = "abandoned_by_agent"
                break

            # Universal success condition for a checkout page
            if agent_action.get("text") == "Place Your Order":
                print(f"     - ✅ Success! Agent clicked the final 'Place Your Order' button.")
                session_success = True
                final_outcome = "converted"
                break
            
            # Record step and continue
            history.append({"action": agent_action, "context": agent_action.get("context", "")})

        if final_outcome == "unknown":
            print("     - ⌛ Session ended due to reaching max steps.")
            final_outcome = "abandoned_max_steps"

        # Finalize and save log
        session_log["final_outcome"] = final_outcome
        session_log["success"] = session_success
        log_filename = f"logs/{session_id}.json"
        with open(log_filename, 'w') as f:
            json.dump(session_log, f, indent=2)
        print(f"   - 💾 Log saved to {log_filename}")

        return {
            "session_id": session_id,
            "persona_id": persona.persona_id,
            "variant": variant,
            "success": session_success,
            "outcome": final_outcome,
            "steps_taken": len(history) + 1,
            "total_hesitation": total_hesitation_steps,
        }
    
    def run_full_test_suite(self, iterations: int = 1) -> Dict: # Reduced default for session-based testing
        """Run the complete A/B test suite with persona-based testing"""
        print("🚀 Starting Advanced Persona-Based A/B Test Suite...")
        print(f"📊 Running tests for {len(self.personas)} personas")
        print("=" * 60)
        
        results = {
            "test_config": {
                "total_personas": len(self.personas),
                "iterations_per_persona": iterations,
                "total_sessions": len(self.personas) * iterations * 2,
                "personas": [p.persona_id for p in self.personas]
            },
            "variant_a_results": [],
            "variant_b_results": [],
            "ab_comparison": {},
            "persona_analysis": {}
        }
        
        # --- Test Variant A ---
        print("\n🔵 TESTING VARIANT A (Current UI)")
        print("=" * 40)
        self._load_elements_map("elements_variant_a.json")
        for persona in self.personas:
            for i in range(iterations):
                session_result = self.run_session(persona, "A")
                results["variant_a_results"].append(session_result)
                self.metrics_a.add_session_result(session_result)
        
        # --- Test Variant B ---
        print("\n🟡 TESTING VARIANT B (Button Color Change)")
        print("=" * 40)
        self._load_elements_map("elements_variant_b.json")
        for persona in self.personas:
            for i in range(iterations):
                session_result = self.run_session(persona, "B")
                results["variant_b_results"].append(session_result)
                self.metrics_b.add_session_result(session_result)

        # TODO: Update calculation and reporting logic
        # results["ab_comparison"] = self._calculate_ab_comparison(results)
        # results["persona_analysis"] = self._calculate_persona_analysis(results)
        
        # Overall metrics
        results["overall_metrics"] = {
            "variant_a": self.metrics_a.get_summary(),
            "variant_b": self.metrics_b.get_summary()
        }
        
        return results

    def _calculate_ab_comparison(self, results: Dict) -> Dict:
        """Calculate the differences between Variant A and B"""
        comparison = {
            "ab_test_scenarios": [],
            "control_scenarios": [],
            "overall_improvement": {}
        }
        
        # Create a mapping of persona names to results
        variant_a_map = {r["persona_id"]: r for r in results["variant_a_results"]}
        variant_b_map = {r["persona_id"]: r for r in results["variant_b_results"]}
        
        for persona_id in variant_a_map.keys():
            a_result = variant_a_map[persona_id]
            b_result = variant_b_map[persona_id]
            
            # Calculate differences
            success_rate_diff = b_result["success_rate"] - a_result["success_rate"]
            processing_time_diff = b_result["avg_processing_time"] - a_result["avg_processing_time"]
            
            comparison_item = {
                "persona_id": persona_id,
                "persona": a_result["persona"], # Assuming persona name is consistent
                "variant_a": {
                    "success_rate": a_result["success_rate"],
                    "avg_processing_time": a_result["avg_processing_time"]
                },
                "variant_b": {
                    "success_rate": b_result["success_rate"],
                    "avg_processing_time": b_result["avg_processing_time"]
                },
                "differences": {
                    "success_rate_change": round(success_rate_diff, 2),
                    "processing_time_change": round(processing_time_diff, 2)
                }
            }
            
            # The original code had is_ab_test, but TestScenario was removed.
            # For now, we'll assume all sessions are A/B tests or control.
            # If specific scenarios were intended, this logic would need to be re-evaluated.
            # For now, we'll just append to ab_test_scenarios as there's no scenario distinction.
            comparison["ab_test_scenarios"].append(comparison_item)
        
        return comparison

    def _calculate_persona_analysis(self, results: Dict) -> Dict:
        """Analyze performance by persona"""
        persona_analysis = {}
        
        for persona in self.personas:
            persona_name = persona.name
            
            # Get all sessions for this persona
            persona_sessions_a = [r for r in results["variant_a_results"] if r["persona_id"] == persona.persona_id]
            persona_sessions_b = [r for r in results["variant_b_results"] if r["persona_id"] == persona.persona_id]
            
            if persona_sessions_a:
                avg_success_a = sum(s["success_rate"] for s in persona_sessions_a) / len(persona_sessions_a)
                avg_time_a = sum(s["avg_processing_time"] for s in persona_sessions_a) / len(persona_sessions_a)
                
                avg_success_b = sum(s["success_rate"] for s in persona_sessions_b) / len(persona_sessions_b)
                avg_time_b = sum(s["avg_processing_time"] for s in persona_sessions_b) / len(persona_sessions_b)
                
                persona_analysis[persona_name] = {
                    "description": persona.description,
                    "primary_goal": persona.primary_goal,
                    "variant_a_performance": {
                        "avg_success_rate": round(avg_success_a, 2),
                        "avg_processing_time": round(avg_time_a, 2)
                    },
                    "variant_b_performance": {
                        "avg_success_rate": round(avg_success_b, 2),
                        "avg_processing_time": round(avg_time_b, 2)
                    },
                    "improvement": {
                        "success_rate_change": round(avg_success_b - avg_success_a, 2),
                        "processing_time_change": round(avg_time_b - avg_time_a, 2)
                    }
                }
        
        return persona_analysis
    
    def generate_report(self, results: Dict) -> str:
        """Generate a comprehensive persona-based A/B test report"""
        report = []
        report.append("# Persona-Based AI Agent UI A/B Test Report")
        report.append(f"**Test Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Total Sessions:** {results['test_config']['total_sessions']}")
        report.append(f"**Personas Tested:** {results['test_config']['total_personas']}")
        report.append("")
        
        # Test Configuration
        report.append("## Test Configuration")
        report.append(f"- **Personas Tested:** {results['test_config']['total_personas']}")
        report.append(f"- **Iterations per Persona:** {results['test_config']['iterations_per_persona']}")
        report.append(f"- **A/B Test Focus:** UI Impact on AI Agent Performance")
        report.append("")
        
        # Overall A/B Comparison
        report.append("## Overall A/B Test Results")
        variant_a_metrics = results["overall_metrics"]["variant_a"]
        variant_b_metrics = results["overall_metrics"]["variant_b"]
        
        report.append("### Variant A (Current UI)")
        for key, value in variant_a_metrics.items():
            report.append(f"- **{key.replace('_', ' ').title()}:** {value}")
        report.append("")

        report.append("### Variant B (Button Color Change)")
        for key, value in variant_b_metrics.items():
            report.append(f"- **{key.replace('_', ' ').title()}:** {value}")
        report.append("")
        
        # TODO: Add demographic and detailed scenario reporting here
        
        return "\n".join(report)

def main():
    """Main function to run the persona-based A/B testing framework"""
    print("🔬 BLIND Persona-Based AI Agent UI A/B Testing Framework")
    print("🎯 Testing Button Color Impact on AI Agent Performance (No Bias)")
    print("=" * 60)
    
    # Initialize framework
    framework = ABTestingFramework(num_personas=10) # Using 10 for a test run
    
    # Display personas
    print(f"\n👥 Testing with {len(framework.personas)} Distinct Personas:")
    for i, persona in enumerate(framework.personas, 1):
        print(f"{i}. {persona.name} ({persona.persona_id})")
        print(f"   Goal: {persona.primary_goal}")
        print(f"   Description: {persona.description[:100].strip()}...")
        print()
    
    # Use default iterations for automated testing
    iterations = 1 # Keep this low for session-based testing
    print(f"Running {iterations} iterations per persona...")
    
    print(f"\n🚀 Starting {iterations} iterations per persona...")
    print("This will test both Variant A and Variant B with all personas.")
    
    # Run tests
    results = framework.run_full_test_suite(iterations)
    
    # Generate and save report
    report = framework.generate_report(results)
    
    # Save report to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"persona_ab_test_report_{timestamp}.md"
    with open(report_filename, 'w') as f:
        f.write(report)
    
    print(f"\n📊 Test completed! Report saved to: {report_filename}")
    print("\n" + "="*60)
    print("📈 Key A/B Test Results:")
    
    # A/B Test Summary
    variant_a_metrics = results["overall_metrics"]["variant_a"]
    variant_b_metrics = results["overall_metrics"]["variant_b"]
    
    print(f"🔵 Variant A (Current): {variant_a_metrics.get('task_success_rate', 0)}% success, {variant_a_metrics.get('avg_session_length', 0)} steps avg")
    print(f"🟡 Variant B (Color Change): {variant_b_metrics.get('task_success_rate', 0)}% success, {variant_b_metrics.get('avg_session_length', 0)} steps avg")
    
    success_diff = variant_b_metrics.get('task_success_rate', 0) - variant_a_metrics.get('task_success_rate', 0)
    time_diff = variant_b_metrics.get('avg_session_length', 0) - variant_a_metrics.get('avg_session_length', 0)
    
    print(f"📊 UI Impact: {success_diff:+.1f}% success rate, {time_diff:+.2f} steps processing time")
    print(f"🎯 Total Sessions: {variant_a_metrics.get('total_sessions', 0) + variant_b_metrics.get('total_sessions', 0)}")
    
    # TODO: Update persona interaction comparison
    # print(f"\n🎭 Persona Interaction Comparison:")
    # for persona_name, analysis in results["persona_analysis"].items():
    #     print(f"\n👤 {persona_name}:")
    #     print(f"   🔵 Variant A: {analysis['variant_a_performance']['avg_success_rate']}% success, {analysis['variant_a_performance']['avg_processing_time']}s")
    #     print(f"   🟡 Variant B: {analysis['variant_b_performance']['avg_success_rate']}% success, {analysis['variant_b_performance']['avg_processing_time']}s")
    #     print(f"   📈 Change: {analysis['improvement']['success_rate_change']:+.1f}% success, {analysis['improvement']['processing_time_change']:+.2f}s")

if __name__ == "__main__":
    main() 