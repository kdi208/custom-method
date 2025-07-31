#!/usr/bin/env python3
"""
Persona-Based AI Agent UI A/B Testing Framework
Tests UI variants using AI agents with different user personas
"""

import google.generativeai as genai
import json
import os
import time
import statistics
from datetime import datetime
from PIL import Image
from dotenv import load_dotenv
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import random
import re

# =============================================================================
# CONFIGURATION SECTION - Central place for all test parameters
# =============================================================================
# 
# Configuration is now loaded from test_config.py
# To modify test parameters, edit test_config.py instead of this file
#
# =============================================================================

try:
    import sys
    import os
    # Add images directory to path to import test_config
    sys.path.append('images')
    from test_config import TEST_CONFIG, DISTRACTED_CONFIG
except ImportError:
    # Fallback configuration if test_config.py is not found
    TEST_CONFIG = {
        "num_personas": 20,           # Number of personas to test
        "iterations_per_persona": 2,  # Number of iterations per persona
        "max_steps_per_session": 5,   # Maximum steps per session
        "variant_a_elements_file": "elements_variant_a.json",
        "variant_b_elements_file": "elements_variant_b.json",
        "personas_directory": "data/example_data/personas/json/",
        "logs_directory": "results/",
        "screenshots_directory": "screenshots/",

    }

# =============================================================================
# END CONFIGURATION SECTION
# =============================================================================

# --- Configuration and Setup ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

# Ensure directories exist
os.makedirs(TEST_CONFIG["logs_directory"], exist_ok=True)

@dataclass
class Persona:
    """Represents a specific user persona for testing."""
    # --- All fields present in persona files ---
    persona: str
    name: str
    age: int
    profession: str
    income: int
    education: str
    location: str
    background: str
    core_motivation: str
    primary_anxiety: str
    decision_making_style: str
    technical_proficiency: str
    interaction_pattern: str
    work_habits: str
    device_context: str
    accessibility_needs: str
    dominant_trait: str
    failure_conditions: Dict
    archetype: str
    user_type: str
    core_value: str
    emotional_trigger: str
    
    # --- Utility field for logging ---
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
        
        # --- Separate timing metrics for success vs failure ---
        self.successful_processing_times = []
        self.failed_processing_times = []

        self.confidence_scores = []
        self.total_tests = 0 # Represents total sessions now
        self.successful_tests = 0 # Represents successful sessions
    
    def add_session_result(self, session_result: Dict):
        """Add a session result to the metrics"""
        self.total_tests += 1
        
        processing_time = session_result.get("total_processing_time", 0.0)
        
        if session_result["success"]:
            self.successful_tests += 1
            self.successful_processing_times.append(processing_time)
        else:
            self.failed_processing_times.append(processing_time)
            outcome = session_result.get("outcome", "unknown_error")
            if "abandoned" in outcome:
                self.abandoned_sessions += 1
            elif outcome == "parsing_error":
                self.parsing_errors += 1
            elif outcome == "misclick":
                self.misclick_errors += 1
        
        self.session_lengths.append(session_result.get("steps_taken", 0))
        self.hesitation_steps.append(session_result.get("total_hesitation", 0))
        self.processing_times.append(processing_time)

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
            "avg_processing_time": round(statistics.mean(self.processing_times), 2) if self.processing_times else 0,
            "avg_processing_time_to_success": round(statistics.mean(self.successful_processing_times), 2) if self.successful_processing_times else 0,
            "avg_processing_time_to_failure": round(statistics.mean(self.failed_processing_times), 2) if self.failed_processing_times else 0,
        }
        # Add old metrics for compatibility if they exist
        if self.processing_times:
            summary.update({
                "avg_processing_time": round(statistics.mean(self.processing_times), 2),
            })
        if self.capture_times:
            summary.update({
                "avg_capture_time": round(statistics.mean(self.capture_times), 2),
            })
        if self.ai_processing_times:
            summary.update({
                "avg_ai_processing_time": round(statistics.mean(self.ai_processing_times), 2),
            })
        if self.parse_times:
            summary.update({
                "avg_parse_time": round(statistics.mean(self.parse_times), 2),
            })
        return summary

class ABTestingFramework:
    """Main A/B testing framework for AI agent UI evaluation"""
    
    def __init__(self, num_personas: int = None):
        # Use default from config if not provided
        if num_personas is None:
            num_personas = TEST_CONFIG["num_personas"]
            
        self.metrics_a = ABTestMetrics()
        self.metrics_b = ABTestMetrics()
        self.personas = self._load_personas(num_personas)
        self.elements_map = self._load_elements_map()
    
    def _load_elements_map(self, filename: str = "elements.json") -> List[Dict]:
        """Load the UI elements map"""
        try:
            with open(filename, 'r') as f:
                elements = json.load(f)
            print(f"   📋 Loaded {len(elements)} elements from {filename}")
            
                        # Debug: Check if Terminate element is present
            terminate_elements = [e for e in elements if e.get("text") == "Cancel purchase"]
            if terminate_elements:
                print(f"   ✅ Terminate element found: {terminate_elements[0]}")
            else:
                print(f"   ⚠️  No Terminate element found in {filename}")
            
            return elements
        except FileNotFoundError:
            print(f"   ❌ Error: Elements file not found: {filename}")
            return []
        except json.JSONDecodeError as e:
            print(f"   ❌ Error: Invalid JSON in {filename}: {e}")
            return []
    


    def _load_personas(self, num_personas: int) -> List[Persona]:
        """Load a random sample of personas from the data directory."""
        # Use the new super personas directory
        persona_dir = TEST_CONFIG["personas_directory"]
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
                
                # Load all fields present in persona files
                persona = Persona(
                    persona_id=filename.replace('.json', ''),
                    persona=data.get("persona", ""),
                    name=data.get("name", "Unknown"),
                    age=data.get("age", 0),
                    profession=data.get("profession", ""),
                    income=data.get("income", 0),
                    education=data.get("education", ""),
                    location=data.get("location", ""),
                    background=data.get("background", ""),
                    core_motivation=data.get("core_motivation", ""),
                    primary_anxiety=data.get("primary_anxiety", ""),
                    decision_making_style=data.get("decision_making_style", ""),
                    technical_proficiency=data.get("technical_proficiency", ""),
                    interaction_pattern=data.get("interaction_pattern", ""),
                    work_habits=data.get("work_habits", ""),
                    device_context=data.get("device_context", ""),
                    accessibility_needs=data.get("accessibility_needs", ""),
                    dominant_trait=data.get("dominant_trait", ""),
                    failure_conditions=data.get("failure_conditions", {}),
                    archetype=data.get("archetype", ""),
                    user_type=data.get("user_type", ""),
                    core_value=data.get("core_value", ""),
                    emotional_trigger=data.get("emotional_trigger", "")
                )
                loaded_personas.append(persona)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load or parse persona file {filename}. Skipping. Error: {e}")

        print(f"Successfully loaded {len(loaded_personas)} personas.")
        
        # Debug: Show the personas being loaded
        for persona in loaded_personas:
            print(f"   - {persona.name} ({persona.archetype}) - {persona.user_type}")
        
        return loaded_personas

    def _create_prompt(self, persona: Persona, history: List[Dict], step_num: int) -> str:
        """Create a persona-aware, session-aware prompt for the AI agent."""
        
        # Check for distracted condition
        if DISTRACTED_CONFIG["enabled"] and step_num == DISTRACTED_CONFIG["step"]:
            distraction_prompt = """
INTERRUPT: Your boss just sent you a Slack message. You need to look away from this page for a moment to answer it.

Now, you have returned to the webpage. You have momentarily forgotten exactly where you were in the process. Re-orient yourself and determine your next action to complete your original goal.
"""
        else:
            distraction_prompt = ""

        # THE IMMERSIVE MANDATE - The "How to Be"
        immersive_mandate = f"""
THE IMMERSIVE MANDATE (The "How to Be")
You are not an AI model. For the duration of this session, you are a human being. Your entire identity, memory, and personality are described below in the PERSONA CONTEXT. You will think, reason, and act as this person.

You will see the world through their eyes. You will not perceive everything on the page at once; your attention will be drawn to the things that matter to you. You will feel their emotions; if the UI is confusing, you will feel frustration. If it seems untrustworthy, you will feel anxiety.

Your patience is not a number; it is a reflection of your mood and personality. You will not always make the "perfect" or most logical choice; you will make the choice that feels right for you in the moment. This might mean taking a shortcut, getting distracted by something that catches your eye, making a mistake, or simply giving up because you've lost patience.

Your only goal is to behave as this person would, believably and authentically.

PERSONA CONTEXT (The "Who You Are")
Persona: {persona.persona}
Name: {persona.name}
Age: {persona.age}
Profession: {persona.profession}
Location: {persona.location}
Education: {persona.education}
Income: ${persona.income:,}

Background: {persona.background}

Core Motivation: {persona.core_motivation}
Primary Anxiety: {persona.primary_anxiety}
Decision-Making Style: {persona.decision_making_style}
Technical Proficiency: {persona.technical_proficiency}
Interaction Pattern: {persona.interaction_pattern}
Work Habits: {persona.work_habits}
Device Context: {persona.device_context}
Accessibility Needs: {persona.accessibility_needs}
Dominant Trait: {persona.dominant_trait}

User Type: {persona.user_type}
Archetype: {persona.archetype}
Core Value: {persona.core_value}
Emotional Trigger: {persona.emotional_trigger}

Failure Conditions (What will make you abandon this task):
{json.dumps(persona.failure_conditions, indent=2)}
"""
        
        # Session history to provide context of previous actions and reasoning
        history_prompt = ""
        if history:
            history_prompt = "SESSION HISTORY (Your previous reasoning and actions):\n"
            for i, entry in enumerate(history):
                action_text = entry['action'].get('text', 'unknown')
                action_context = entry['action'].get('context', 'unknown location')
                reasoning = entry.get('reasoning', 'No reasoning provided')
                history_prompt += f"Step {i+1}:\n"
                history_prompt += f"Your reasoning: {reasoning}\n"
                history_prompt += f"Your action: You clicked '{action_text}' ({action_context}).\n\n"
            history_prompt += "\n"

        # The interface context and task
        task_prompt = f"""
"""
        
        # Add primary goal if enabled
        if TEST_CONFIG.get("primary_goal_enabled", False):
            task_prompt += f"""
YOUR PRIMARY GOAL: {TEST_CONFIG.get("primary_goal_text", "")}

"""
        
        task_prompt += f"""You are looking at a webpage. Here are all the clickable elements you can see:

AVAILABLE CLICKABLE ELEMENTS:
{json.dumps(self.elements_map, indent=2)}

Based on your previous reasoning and actions, continue your thought process. Provide your step-by-step reasoning for your next action as a numbered list, building upon what you've already thought about.
REASONING:
1. [Building on your previous thoughts...]
2. [Your next consideration...]
...

Finally, provide the JSON for your chosen action. Your response MUST be ONLY the JSON object for the single element you want to click. Use this exact format: {{"text": "Element Name", "context": "Element Context"}}. You can also choose to terminate the session if you feel you've explored enough.
To terminate, respond with: {{"action": "terminate"}}

ACTION:
"""
        
        return immersive_mandate + history_prompt + distraction_prompt + task_prompt



    def run_session(self, persona: Persona, variant: str = "A", max_steps: int = None) -> Dict:
        """
        Run a multi-step session for a given persona.
        A session continues until the task is complete, abandoned, or an error occurs.
        """
        # Use default max_steps if not provided
        if max_steps is None:
            max_steps = TEST_CONFIG["max_steps_per_session"]
            
        session_id = f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}_{persona.persona_id}_{variant}"
        print(f"\n🚀 Starting Session: {session_id}")
        print(f"   Persona: {persona.name} ({persona.persona_id})")
        
        # Verify elements are loaded correctly
        terminate_elements = [e for e in self.elements_map if e.get("text") == "Cancel purchase"]
        if terminate_elements:
            print(f"   ✅ Terminate element available: {terminate_elements[0]}")
        else:
            print(f"   ⚠️  No Terminate element in current elements map ({len(self.elements_map)} elements)")

        history = []
        session_log = {
            "session_id": session_id,
            "persona_id": persona.persona_id,
            "variant": variant,
            "steps": []
        }
        
        session_success = False
        final_outcome = "unknown"
        total_hesitation_steps = 0
        abandonment_reasoning = None
        total_processing_time = 0.0
        
        for step_num in range(max_steps):
            print(f"   - Step {step_num + 1}/{max_steps}...")
            step_log = {"step_number": step_num + 1}

            # Load static image for variant
            capture_start = time.time()
            image_file = TEST_CONFIG["variant_a_image"] if variant == "A" else TEST_CONFIG["variant_b_image"]
            image = Image.open(image_file)
            step_log["image_file"] = image_file
            capture_time = time.time() - capture_start

            # Create prompt
            prompt = self._create_prompt(persona, history, step_num + 1)
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
                    
                    # Extract Reasoning and Action - More robust parsing
                    action_json_str = re.search(r"ACTION:\s*(\{.*?\})", raw_response, re.DOTALL)
                    
                    # If ACTION: label not found, try to find JSON object at the end
                    if not action_json_str:
                        # Look for JSON object at the end of the response
                        json_objects = re.findall(r'\{[^{}]*"text"[^{}]*"context"[^{}]*\}', raw_response)
                        if json_objects:
                            json_str = json_objects[-1].strip()  # Take the last JSON object found
                        else:
                            # Try to find any JSON object that might be the action
                            json_objects = re.findall(r'\{[^{}]*\}', raw_response)
                            if json_objects:
                                json_str = json_objects[-1].strip()
                            else:
                                raise json.JSONDecodeError("Action block not found.", raw_response, 0)
                    else:
                        json_str = action_json_str.group(1).strip()
                    
                    # Clean up the JSON string
                    json_str = re.sub(r',\s*}', '}', json_str)
                    json_str = re.sub(r',\s*]', ']', json_str)
                    
                    try:
                        agent_action = json.loads(json_str)
                    except json.JSONDecodeError as json_err:
                        # Try to fix common JSON issues
                        json_str = re.sub(r'(["\w])\s*,\s*(["\w])', r'\1, \2', json_str)
                        json_str = re.sub(r'(["\w])\s*:\s*(["\w])', r'\1: \2', json_str)
                        agent_action = json.loads(json_str)
                    
                    step_log["parsed_action"] = agent_action

                    # Extract reasoning - handle cases where ACTION label might be missing
                    reasoning_str = re.search(r"REASONING:(.*?)(?:ACTION:|$)", raw_response, re.DOTALL)
                    reasoning = reasoning_str.group(1).strip() if reasoning_str else "No reasoning provided"
                    hesitation_steps = len(re.findall(r"^\s*\d+\.\s", reasoning, re.MULTILINE)) if reasoning_str else 0
                    total_hesitation_steps += hesitation_steps
                    step_log["hesitation_steps"] = hesitation_steps
                    step_log["reasoning"] = reasoning
                    step_log["ai_processing_time"] = ai_processing_time
                    total_processing_time += ai_processing_time
                    
                    break # Success, exit retry loop
                except (json.JSONDecodeError, AttributeError) as e:
                    print(f"     - ⚠️ LLM output parsing failed (Attempt {attempt + 1}/{parsing_attempts}). Error: {e}")
                    raw_response = getattr(e, 'doc', raw_response) # Store faulty response
                    prompt += "\n\nYour last response was not valid JSON. Please correct your thinking and provide the action in the correct format."
                    agent_action = None
                    step_log["error"] = f"Parsing failed on attempt {attempt + 1}: {e}"
                except Exception as e:
                    print(f"     - ⚠️ API error (Attempt {attempt + 1}/{parsing_attempts}). Error: {e}")
                    if attempt < parsing_attempts - 1:
                        # Check if it's a rate limit error
                        if "429" in str(e) or "quota" in str(e).lower():
                            wait_time = 60  # Wait 1 minute for rate limits
                            print(f"     - 🔄 Rate limit detected. Waiting {wait_time} seconds...")
                        else:
                            wait_time = 5  # Standard retry delay
                            print(f"     - 🔄 Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        print(f"     - ❌ API error after {parsing_attempts} attempts. Marking session as failed.")
                        step_log["error"] = f"API error after {parsing_attempts} attempts: {e}"
                        agent_action = None

            session_log["steps"].append(step_log)
            
            if agent_action is None:
                print("     - ❌ Session failed due to persistent parsing errors.")
                final_outcome = "parsing_error"
                break

            # --- Simplified Outcome Labeling Logic ---
            # 1. Check for termination action first
            if agent_action.get("action") == "terminate":
                reasoning = step_log.get("reasoning", "No reasoning provided")
                print("     - 🛑 Agent chose to terminate the session.")
                print(f"     - 💭 Reasoning: {reasoning}")
                final_outcome = "abandoned_by_agent"
                abandonment_reasoning = reasoning
                break

            # 2. Check for termination elements
            action_text = agent_action.get("text")
            termination_elements = ["Cancel purchase", "Browse other events", "Become Distracted", "BEST BUY logo", "Remove item", "Back to Delivery options"]
            if action_text in termination_elements:
                reasoning = step_log.get("reasoning", "No reasoning provided")
                print(f"     - 🚪 Agent clicked '{action_text}' - session terminated.")
                print(f"     - 💭 Reasoning: {reasoning}")
                final_outcome = "abandoned_by_agent"
                abandonment_reasoning = reasoning
                break

            # 3. Validate element exists
            is_valid_element = False
            if action_text:
                for element in self.elements_map:
                    if element.get("text") == action_text:
                        is_valid_element = True
                        break
            
            # 3. Check for success condition (checkout/continue buttons end session)
            success_elements = ["Checkout button", "Continue button", "Place Your Order"]
            if action_text in success_elements:
                print(f"     - ✅ Success! Agent clicked the '{action_text}' button.")
                session_success = True
                final_outcome = "converted"
                break
            
            # 4. Handle invalid elements (log but don't fail)
            if not is_valid_element:
                print(f"     - ⚠️ Agent chose a non-existent element: '{action_text}' (continuing...)")
                # Don't break - let them continue trying
            
            # 5. Record step and continue (for both valid and invalid clicks)
            if action_text:
                print(f"     - 👉 Agent clicked: '{action_text}'")
                history.append({
                    "action": agent_action,
                    "reasoning": step_log.get("reasoning", "No reasoning provided")
                })

        if final_outcome == "unknown":
            print("     - ⌛ Session ended due to reaching max steps.")
            final_outcome = "abandoned_max_steps"

        # Finalize and save log
        session_log["final_outcome"] = final_outcome
        session_log["success"] = session_success
        if abandonment_reasoning:
            session_log["abandonment_reasoning"] = abandonment_reasoning
        log_filename = f"{TEST_CONFIG['logs_directory']}{session_id}.json"
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
            "total_processing_time": total_processing_time,
            "abandonment_reasoning": abandonment_reasoning,
        }
    
    def run_full_test_suite(self, iterations: int = None) -> Dict:
        """Run the complete A/B test suite with persona-based testing"""
        # Use default from config if not provided
        if iterations is None:
            iterations = TEST_CONFIG["iterations_per_persona"]
            
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
        print("\n🔵 TESTING VARIANT A (Control)")
        print("=" * 40)
        # Load Variant A elements
        self.elements_map = self._load_elements_map(TEST_CONFIG["variant_a_elements_file"])
        for persona in self.personas:
            for i in range(iterations):
                session_result = self.run_session(persona, "A")
                results["variant_a_results"].append(session_result)
                self.metrics_a.add_session_result(session_result)
        
        # --- Test Variant B ---
        print("\n🟡 TESTING VARIANT B (Treatment)")
        print("=" * 40)
        # Load Variant B elements
        self.elements_map = self._load_elements_map(TEST_CONFIG["variant_b_elements_file"])
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
        
        # Calculate user experience groups
        results["user_experience_groups"] = self._calculate_user_experience_groups(results)
        
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
                    "background": persona.background,
                    "core_motivation": persona.core_motivation,
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

    def _calculate_user_experience_groups(self, results: Dict) -> Dict:
        """Calculate user experience summary into 4 groups: success/failure for A/B variants"""
        groups = {
            "variant_a_success": [],
            "variant_a_failure": [],
            "variant_b_success": [],
            "variant_b_failure": []
        }
        
        # Group Variant A sessions
        for session in results["variant_a_results"]:
            if session["success"]:
                groups["variant_a_success"].append(session)
            else:
                groups["variant_a_failure"].append(session)
        
        # Group Variant B sessions
        for session in results["variant_b_results"]:
            if session["success"]:
                groups["variant_b_success"].append(session)
            else:
                groups["variant_b_failure"].append(session)
        
        # Calculate summary statistics for each group
        summary = {}
        for group_name, sessions in groups.items():
            if sessions:
                summary[group_name] = {
                    "count": len(sessions),
                    "percentage": round((len(sessions) / len(results["variant_a_results"] + results["variant_b_results"])) * 100, 1),
                    "avg_steps": round(sum(s.get("steps_taken", 0) for s in sessions) / len(sessions), 2),
                    "avg_processing_time": round(sum(s.get("total_processing_time", 0) for s in sessions) / len(sessions), 2),
                    "avg_hesitation": round(sum(s.get("total_hesitation", 0) for s in sessions) / len(sessions), 2),
                    "personas": list(set(s["persona_id"] for s in sessions))
                }
            else:
                summary[group_name] = {
                    "count": 0,
                    "percentage": 0.0,
                    "avg_steps": 0.0,
                    "avg_processing_time": 0.0,
                    "avg_hesitation": 0.0,
                    "personas": []
                }
        
        return summary
    
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
        report.append(f"- **A/B Test Focus:** Treatment vs Control Impact on AI Agent Performance")
        report.append("")
        
        # Overall A/B Comparison
        report.append("## Overall A/B Test Results")
        variant_a_metrics = results["overall_metrics"]["variant_a"]
        variant_b_metrics = results["overall_metrics"]["variant_b"]
        
        report.append("### Variant A (Control)")
        for key, value in variant_a_metrics.items():
            report.append(f"- **{key.replace('_', ' ').title()}:** {value}")
        report.append("")

        report.append("### Variant B (Treatment)")
        for key, value in variant_b_metrics.items():
            report.append(f"- **{key.replace('_', ' ').title()}:** {value}")
        report.append("")
        
        # User Experience Groups Summary
        report.append("## User Experience Groups Summary")
        report.append("### 4-Group Analysis: Success/Failure for A/B Variants")
        report.append("")
        
        ux_groups = results["user_experience_groups"]
        
        report.append("#### 🔵 Variant A (Control) - Success")
        if ux_groups["variant_a_success"]["count"] > 0:
            report.append(f"- **Count:** {ux_groups['variant_a_success']['count']} sessions ({ux_groups['variant_a_success']['percentage']}%)")
            report.append(f"- **Avg Steps:** {ux_groups['variant_a_success']['avg_steps']}")
            report.append(f"- **Avg Processing Time:** {ux_groups['variant_a_success']['avg_processing_time']}s")
            report.append(f"- **Avg Hesitation:** {ux_groups['variant_a_success']['avg_hesitation']} steps")
            report.append(f"- **Personas:** {', '.join(ux_groups['variant_a_success']['personas'])}")
        else:
            report.append("- **No successful sessions**")
        report.append("")
        
        report.append("#### 🔴 Variant A (Control) - Failure")
        if ux_groups["variant_a_failure"]["count"] > 0:
            report.append(f"- **Count:** {ux_groups['variant_a_failure']['count']} sessions ({ux_groups['variant_a_failure']['percentage']}%)")
            report.append(f"- **Avg Steps:** {ux_groups['variant_a_failure']['avg_steps']}")
            report.append(f"- **Avg Processing Time:** {ux_groups['variant_a_failure']['avg_processing_time']}s")
            report.append(f"- **Avg Hesitation:** {ux_groups['variant_a_failure']['avg_hesitation']} steps")
            report.append(f"- **Personas:** {', '.join(ux_groups['variant_a_failure']['personas'])}")
        else:
            report.append("- **No failed sessions**")
        report.append("")
        
        report.append("#### 🟡 Variant B (Treatment) - Success")
        if ux_groups["variant_b_success"]["count"] > 0:
            report.append(f"- **Count:** {ux_groups['variant_b_success']['count']} sessions ({ux_groups['variant_b_success']['percentage']}%)")
            report.append(f"- **Avg Steps:** {ux_groups['variant_b_success']['avg_steps']}")
            report.append(f"- **Avg Processing Time:** {ux_groups['variant_b_success']['avg_processing_time']}s")
            report.append(f"- **Avg Hesitation:** {ux_groups['variant_b_success']['avg_hesitation']} steps")
            report.append(f"- **Personas:** {', '.join(ux_groups['variant_b_success']['personas'])}")
        else:
            report.append("- **No successful sessions**")
        report.append("")
        
        report.append("#### 🟠 Variant B (Treatment) - Failure")
        if ux_groups["variant_b_failure"]["count"] > 0:
            report.append(f"- **Count:** {ux_groups['variant_b_failure']['count']} sessions ({ux_groups['variant_b_failure']['percentage']}%)")
            report.append(f"- **Avg Steps:** {ux_groups['variant_b_failure']['avg_steps']}")
            report.append(f"- **Avg Processing Time:** {ux_groups['variant_b_failure']['avg_processing_time']}s")
            report.append(f"- **Avg Hesitation:** {ux_groups['variant_b_failure']['avg_hesitation']} steps")
            report.append(f"- **Personas:** {', '.join(ux_groups['variant_b_failure']['personas'])}")
        else:
            report.append("- **No failed sessions**")
        report.append("")
        
        return "\n".join(report)

def main():
    """Main function to run the persona-based A/B testing framework"""
    print("🔬 BLIND Persona-Based AI Agent UI A/B Testing Framework")
    print("🎯 Testing Treatment vs Control Impact on AI Agent Performance (No Bias)")
    print("=" * 60)
    
    # Initialize framework
    framework = ABTestingFramework(num_personas=TEST_CONFIG["num_personas"])
    
    # Display personas
    print(f"\n👥 Testing with {len(framework.personas)} Distinct Personas:")
    for i, persona in enumerate(framework.personas, 1):
        print(f"{i}. {persona.name} ({persona.persona_id})")

        print(f"   Background: {persona.background[:100].strip()}...")
        print()
    
    print(f"Running {TEST_CONFIG['iterations_per_persona']} iterations per persona...")
    
    print(f"\n🚀 Starting {TEST_CONFIG['iterations_per_persona']} iterations per persona...")
    print("This will test both Variant A and Variant B with all personas.")
    
    # Run tests
    results = framework.run_full_test_suite()
    
    # Generate and save report
    report = framework.generate_report(results)
    
    # Save report to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"results/persona_ab_test_report_{timestamp}.md"
    # Ensure results directory exists
    os.makedirs("results", exist_ok=True)
    with open(report_filename, 'w') as f:
        f.write(report)
    
    print(f"\n📊 Test completed! Report saved to: {report_filename}")
    print("\n" + "="*60)
    print("📈 Key A/B Test Results:")
    
    # A/B Test Summary
    variant_a_metrics = results["overall_metrics"]["variant_a"]
    variant_b_metrics = results["overall_metrics"]["variant_b"]
    
    print(f"🔵 Variant A (Control): {variant_a_metrics.get('task_success_rate', 0)}% success, {variant_a_metrics.get('avg_session_length', 0)} steps avg, {variant_a_metrics.get('avg_processing_time', 0):.2f}s processing")
    print(f"   ⏱️  Success: {variant_a_metrics.get('avg_processing_time_to_success', 0):.2f}s, Failure: {variant_a_metrics.get('avg_processing_time_to_failure', 0):.2f}s")
    print(f"🟡 Variant B (Treatment): {variant_b_metrics.get('task_success_rate', 0)}% success, {variant_b_metrics.get('avg_session_length', 0)} steps avg, {variant_b_metrics.get('avg_processing_time', 0):.2f}s processing")
    print(f"   ⏱️  Success: {variant_b_metrics.get('avg_processing_time_to_success', 0):.2f}s, Failure: {variant_b_metrics.get('avg_processing_time_to_failure', 0):.2f}s")
    
    success_diff = variant_b_metrics.get('task_success_rate', 0) - variant_a_metrics.get('task_success_rate', 0)
    steps_diff = variant_b_metrics.get('avg_session_length', 0) - variant_a_metrics.get('avg_session_length', 0)
    processing_diff = variant_b_metrics.get('avg_processing_time', 0) - variant_a_metrics.get('avg_processing_time', 0)
    success_time_diff = variant_b_metrics.get('avg_processing_time_to_success', 0) - variant_a_metrics.get('avg_processing_time_to_success', 0)
    failure_time_diff = variant_b_metrics.get('avg_processing_time_to_failure', 0) - variant_a_metrics.get('avg_processing_time_to_failure', 0)
    
    print(f"📊 UI Impact: {success_diff:+.1f}% success rate, {steps_diff:+.2f} steps, {processing_diff:+.2f}s processing time")
    print(f"⏱️  Time Impact: Success {success_time_diff:+.2f}s, Failure {failure_time_diff:+.2f}s")
    print(f"🎯 Total Sessions: {variant_a_metrics.get('total_sessions', 0) + variant_b_metrics.get('total_sessions', 0)}")
    
    # User Experience Groups Summary
    print(f"\n📊 User Experience Groups Summary:")
    ux_groups = results["user_experience_groups"]
    
    print(f"🔵 Variant A Success: {ux_groups['variant_a_success']['count']} sessions ({ux_groups['variant_a_success']['percentage']}%) - {ux_groups['variant_a_success']['avg_steps']} steps, {ux_groups['variant_a_success']['avg_processing_time']}s")
    print(f"🔴 Variant A Failure: {ux_groups['variant_a_failure']['count']} sessions ({ux_groups['variant_a_failure']['percentage']}%) - {ux_groups['variant_a_failure']['avg_steps']} steps, {ux_groups['variant_a_failure']['avg_processing_time']}s")
    print(f"🟡 Variant B Success: {ux_groups['variant_b_success']['count']} sessions ({ux_groups['variant_b_success']['percentage']}%) - {ux_groups['variant_b_success']['avg_steps']} steps, {ux_groups['variant_b_success']['avg_processing_time']}s")
    print(f"🟠 Variant B Failure: {ux_groups['variant_b_failure']['count']} sessions ({ux_groups['variant_b_failure']['percentage']}%) - {ux_groups['variant_b_failure']['avg_steps']} steps, {ux_groups['variant_b_failure']['avg_processing_time']}s")
    
    # TODO: Update persona interaction comparison
    # print(f"\n🎭 Persona Interaction Comparison:")
    # for persona_name, analysis in results["persona_analysis"].items():
    #     print(f"\n👤 {persona_name}:")
    #     print(f"   🔵 Variant A: {analysis['variant_a_performance']['avg_success_rate']}% success, {analysis['variant_a_performance']['avg_processing_time']}s")
    #     print(f"   🟡 Variant B: {analysis['variant_b_performance']['avg_success_rate']}% success, {analysis['variant_b_performance']['avg_processing_time']}s")
    #     print(f"   📈 Change: {analysis['improvement']['success_rate_change']:+.1f}% success, {analysis['improvement']['processing_time_change']:+.2f}s")

if __name__ == "__main__":
    main() 