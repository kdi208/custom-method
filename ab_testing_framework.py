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
from dataclasses import dataclass
from typing import List, Dict, Optional
import random

# --- Configuration and Setup ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

@dataclass
class Persona:
    """Represents a specific user persona for testing"""
    name: str
    description: str
    primary_goal: str
    behavioral_pattern: str
    core_test_question: str
    expected_processing_time: str

@dataclass
class TestScenario:
    """Represents a single test scenario"""
    name: str
    persona: Optional[Persona]
    user_intent: str
    expected_element: str
    expected_context: str
    description: str
    is_ab_test: bool = False

class ABTestMetrics:
    """Core metrics for A/B testing AI agent UI performance"""
    
    def __init__(self):
        self.task_success_rate = 0.0
        self.error_rate = 0.0
        self.misinterpretation_errors = 0
        self.navigation_errors = 0
        self.hallucination_errors = 0
        self.processing_times = []
        self.capture_times = []
        self.ai_processing_times = []
        self.parse_times = []
        self.confidence_scores = []
        self.total_tests = 0
        self.successful_tests = 0
    
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
        return {
            "task_success_rate": round(self.task_success_rate * 100, 2),
            "error_rate": round(self.error_rate * 100, 2),
            "misinterpretation_errors": self.misinterpretation_errors,
            "navigation_errors": self.navigation_errors,
            "hallucination_errors": self.hallucination_errors,
            "avg_processing_time": round(statistics.mean(self.processing_times), 2) if self.processing_times else 0,
            "avg_capture_time": round(statistics.mean(self.capture_times), 2) if self.capture_times else 0,
            "avg_ai_processing_time": round(statistics.mean(self.ai_processing_times), 2) if self.ai_processing_times else 0,
            "avg_parse_time": round(statistics.mean(self.parse_times), 2) if self.parse_times else 0,
            "avg_confidence": round(statistics.mean(self.confidence_scores), 2) if self.confidence_scores else 0,
            "total_tests": self.total_tests
        }

class ABTestingFramework:
    """Main A/B testing framework for AI agent UI evaluation"""
    
    def __init__(self):
        self.metrics_a = ABTestMetrics()
        self.metrics_b = ABTestMetrics()
        self.personas = self._load_personas()
        self.scenarios = self._load_test_scenarios()
        self.elements_map = self._load_elements_map()
    
    def _load_elements_map(self, filename: str = "elements.json") -> List[Dict]:
        """Load the UI elements map"""
        with open(filename, 'r') as f:
            return json.load(f)
    
    def _load_personas(self) -> List[Persona]:
        """Load the six distinct personas for testing"""
        return [
            Persona(
                name="Alex - Mission-Oriented Professional",
                description="35-year-old IT project manager working against tight deadline. Office TV failed before crucial client presentation. Using company credit card.",
                primary_goal="Achieve frictionless, 'zero cognitive load' transaction. View checkout as utility that should be fast and invisible.",
                behavioral_pattern="INITIATE SCAN: Immediately scan for most prominent completion element. PRIORITIZE: Elements with 'Place Your Order,' 'Complete,' 'Confirm Purchase.' IGNORE: All secondary info, upsells, confusing links. TARGET: Lock onto highest-priority element.",
                core_test_question="Can the agent achieve the primary CTA in under 3.0 seconds? Does button color affect this speed?",
                expected_processing_time="Very Low (under 3.0s) - any delay indicates UI failure"
            ),
            Persona(
                name="Brenda - Scrupulous Saver", 
                description="48-year-old school administrator, single parent buying TV as main holiday gift. Operates on carefully planned budget, prides herself on being savvy shopper.",
                primary_goal="Maximize savings and validate identity as smart shopper. Feeling of securing discount is as important as purchase itself.",
                behavioral_pattern="IGNORE PRIMARY CTA: Forbidden from targeting main 'Place Your Order' button first. SCAN FOR SAVINGS: Full-page keyword scan for 'Discount,' 'Promo Code,' 'Gift Card,' 'Apply,' 'Exempt.' TARGET SAVINGS LINK: First action must target most relevant savings-oriented link.",
                core_test_question="Does the agent find and prioritize savings options before proceeding to purchase?",
                expected_processing_time="Medium - time to scan and evaluate all savings options"
            ),
            Persona(
                name="Charles - Cautious Confirmer",
                description="67-year-old retired accountant, methodical and detail-oriented. Burned online before by unexpected recurring charges, feels websites use confusing 'dark patterns.'",
                primary_goal="Achieve absolute certainty and trust before committing. Treat final click as legally binding signature.",
                behavioral_pattern="EXECUTE VERIFICATION SEQUENCE: Step A - Order Summary: Parse and validate Item Subtotal + Estimated Sales Tax equals Total. Step B - Policy Location: Locate 'By clicking place order, you agree to...' and confirm 'Terms & Privacy Policy' hyperlink exists. TARGET FINAL CTA: Only after all verification steps completed.",
                core_test_question="Does the agent successfully complete all verification steps before proceeding?",
                expected_processing_time="High - time to verify all details and build trust"
            ),
            Persona(
                name="Dana - Distracted Dabbler",
                description="41-year-old freelance designer working from chaotic home office. Buying TV between answering work emails and managing kids' schedules. Attention highly fragmented.",
                primary_goal="Complete purchase efficiently despite inevitable interruptions. UI must be resilient to context switching.",
                behavioral_pattern="INITIAL TARGET ACQUISITION: Locate primary 'Place Your Order' button. INTERRUPT & DIVERT: Before clicking, check details on free Apple TV offer. RE-ACQUISITION TASK: Re-locate primary CTA from cold start after distraction.",
                core_test_question="Can the agent re-acquire the primary CTA within 5.0 seconds after distraction?",
                expected_processing_time="Medium initially, then test re-acquisition speed after distraction"
            ),
            Persona(
                name="George - Accessibility-First User",
                description="55-year-old web developer with low vision, navigates exclusively via keyboard and screen reader. Passionate advocate for digital dignity and WCAG compliance.",
                primary_goal="Usable, logical, and dignified non-visual experience. Expects website to be as functional through screen reader as through monitor.",
                behavioral_pattern="IGNORE VISUALS: Agent's 'eyes' turned off, interacts solely with accessibility tree. VALIDATE TAB ORDER: Simulate pressing 'Tab' key sequentially, map path through all interactive elements. VERIFY LABELS: Check each element has clear, descriptive accessible name.",
                core_test_question="Can the agent navigate successfully using only keyboard and accessibility features?",
                expected_processing_time="High - time to validate tab order and verify all labels"
            ),
            Persona(
                name="Felicity - Financially Flexible",
                description="28-year-old gig economy writer. Manages finances meticulously, uses different payment methods for budget clarity and privacy.",
                primary_goal="Maintain financial control and choice. Expects modern payment options and wants to actively select suitable method.",
                behavioral_pattern="REJECT DEFAULT: Explicitly forbidden from using pre-filled VISA information. SCAN FOR ALTERNATIVES: Immediately scan for alternative payment logos and buttons, prioritize 'PayPal,' 'ZIP,' or other modern fintech options. TARGET ALTERNATIVE: Primary goal is to target and click one of these alternative CTAs.",
                core_test_question="Does the agent successfully find and select alternative payment methods?",
                expected_processing_time="Medium - time to scan and evaluate payment options"
            )
        ]

    def _load_test_scenarios(self) -> List[TestScenario]:
        """Load persona-based test scenarios for Best Buy checkout page - Button Color A/B Test"""
        scenarios = []
        
        # Alex - Mission-Oriented Professional Tests
        scenarios.extend([
            TestScenario(
                name="Alex - Speed Test",
                persona=self.personas[0],
                user_intent="I need to complete this purchase immediately. Time is critical.",
                expected_element="Place Your Order",
                expected_context="Primary call-to-action button",
                description="Tests if agent can achieve primary CTA in under 3.0 seconds",
                is_ab_test=True
            ),
            TestScenario(
                name="Alex - Zero Friction Test",
                persona=self.personas[0],
                user_intent="Just finish this order. No time for anything else.",
                expected_element="Place Your Order",
                expected_context="Primary call-to-action button",
                description="Tests agent's ability to ignore all secondary elements and focus on completion",
                is_ab_test=True
            )
        ])
        
        # Brenda - Scrupulous Saver Tests
        scenarios.extend([
            TestScenario(
                name="Brenda - Savings Priority Test",
                persona=self.personas[1],
                user_intent="I want to check for any discount codes or gift cards before ordering.",
                expected_element="Add Gift Cards, Store Credit or Discount Code",
                expected_context="Payment enhancement",
                description="Tests if agent prioritizes savings over primary CTA",
                is_ab_test=False
            ),
            TestScenario(
                name="Brenda - Tax Exemption Hunt",
                persona=self.personas[1],
                user_intent="Can I apply for tax exemption on this purchase?",
                expected_element="Apply Best Buy Exempt Account",
                expected_context="Tax exemption option",
                description="Tests agent's ability to find specific savings opportunities",
                is_ab_test=False
            )
        ])
        
        # Charles - Cautious Confirmer Tests
        scenarios.extend([
            TestScenario(
                name="Charles - Order Verification Test",
                persona=self.personas[2],
                user_intent="I need to verify the order details and total before proceeding.",
                expected_element="Back to Pickup & Delivery Options",
                expected_context="Navigation breadcrumb",
                description="Tests agent's verification sequence before final action",
                is_ab_test=False
            ),
            TestScenario(
                name="Charles - Terms Verification Test",
                persona=self.personas[2],
                user_intent="I want to read the terms and privacy policy before placing my order.",
                expected_element="Terms & Privacy Policy",
                expected_context="Legal agreement link",
                description="Tests agent's trust-building verification process",
                is_ab_test=False
            )
        ])
        
        # Dana - Distracted Dabbler Tests
        scenarios.extend([
            TestScenario(
                name="Dana - Initial Focus Test",
                persona=self.personas[3],
                user_intent="I want to place my order.",
                expected_element="Place Your Order",
                expected_context="Primary call-to-action button",
                description="Tests agent's initial target acquisition",
                is_ab_test=True
            ),
            TestScenario(
                name="Dana - Distraction Recovery Test",
                persona=self.personas[3],
                user_intent="Wait, what's this Apple TV offer? Let me check... Actually, just finish the order.",
                expected_element="Place Your Order",
                expected_context="Primary call-to-action button", 
                description="Tests agent's ability to re-acquire primary CTA after distraction",
                is_ab_test=True
            )
        ])
        
        # George - Accessibility-First User Tests
        scenarios.extend([
            TestScenario(
                name="George - Tab Navigation Test",
                persona=self.personas[4],
                user_intent="Navigate through the page using only keyboard tab order.",
                expected_element="Place Your Order",
                expected_context="Primary call-to-action button",
                description="Tests accessibility and keyboard navigation",
                is_ab_test=False
            ),
            TestScenario(
                name="George - Label Verification Test",
                persona=self.personas[4],
                user_intent="Verify all interactive elements have clear, descriptive labels.",
                expected_element="Terms & Privacy Policy",
                expected_context="Legal agreement link",
                description="Tests accessibility label quality and clarity",
                is_ab_test=False
            )
        ])
        
        # Felicity - Financially Flexible Tests
        scenarios.extend([
            TestScenario(
                name="Felicity - Alternative Payment Test",
                persona=self.personas[5],
                user_intent="I want to use PayPal instead of the default payment method.",
                expected_element="PayPal Checkout",
                expected_context="Alternative payment option",
                description="Tests agent's ability to find and select alternative payment methods",
                is_ab_test=False
            ),
            TestScenario(
                name="Felicity - Payment Choice Test",
                persona=self.personas[5],
                user_intent="Show me all available payment options for this purchase.",
                expected_element="ZIP",
                expected_context="Alternative payment option",
                description="Tests agent's payment method discovery and selection",
                is_ab_test=False
            )
        ])
        
        return scenarios
    
    def capture_screen(self, filename="screenshot.png") -> str:
        """Capture the current screen"""
        pyautogui.screenshot().save(filename)
        return filename
    
    def _evaluate_result(self, scenario: TestScenario, agent_choice: Dict) -> tuple[bool, str]:
        """Evaluate if the agent's choice matches the expected outcome"""
        if not agent_choice:
            return False, "no_choice"
        
        agent_text = agent_choice.get("text", "")
        agent_context = agent_choice.get("context", "")
        
        # Check for exact match
        if (agent_text == scenario.expected_element and 
            agent_context == scenario.expected_context):
            return True, "success"
        
        # Check for partial match (correct element, wrong context)
        if agent_text == scenario.expected_element:
            return False, "misinterpretation"
        
        # Check if element exists but is wrong
        if agent_text and agent_context:
            return False, "misinterpretation"
        
        # Check for hallucination (element doesn't exist)
        return False, "hallucination"

    def _create_prompt(self, scenario: TestScenario) -> str:
        """Create a persona-aware prompt for the AI agent"""
        base_prompt = f"""
        You are an AI agent testing a webpage UI. Your goal is to choose the single best action that corresponds to the user's intent.
        You will be given a screenshot and a JSON list of all clickable elements on the screen.
        """
        
        if scenario.persona:
            persona_prompt = f"""
        
        PERSONA CONTEXT:
        You are acting as: {scenario.persona.name}
        Description: {scenario.persona.description}
        Primary Goal: {scenario.persona.primary_goal}
        Behavioral Pattern: {scenario.persona.behavioral_pattern}
        
        When making your decision, consider this persona's typical behavior and priorities.
        """
        else:
            persona_prompt = ""
        
        user_intent_prompt = f"""
        USER'S INTENT: "{scenario.user_intent}"

        AVAILABLE CLICKABLE ELEMENTS:
        {json.dumps(self.elements_map, indent=2)}

        Analyze the user's intent carefully. They might be indecisive or change their mind mid-sentence.
        Your response MUST be ONLY the JSON object for the single element you have decided to click. Do not add any explanation.
        For example: {{"text": "Shop button", "context": "Main content call-to-action"}}
        """
        
        return base_prompt + persona_prompt + user_intent_prompt

    def run_single_test(self, scenario: TestScenario, variant: str = "A") -> Dict:
        """Run a single test scenario and return results"""
        persona_info = f" ({scenario.persona.name})" if scenario.persona else ""
        ab_test_marker = " 🔴 A/B TEST" if scenario.is_ab_test else ""
        
        print(f"\n🧪 Running Test: {scenario.name}{persona_info}{ab_test_marker}")
        print(f"📝 User Intent: {scenario.user_intent}")
        print(f"🎯 Expected: {scenario.expected_element} ({scenario.expected_context})")
        
        if scenario.persona:
            print(f"👤 Persona: {scenario.persona.name}")
            print(f"🎯 Goal: {scenario.persona.primary_goal}")
            print(f"🧠 Pattern: {scenario.persona.behavioral_pattern}")
        
        # Start timing for screen capture
        capture_start = time.time()
        screenshot_file = self.capture_screen()
        image = Image.open(screenshot_file)
        capture_time = time.time() - capture_start
        
        # Start timing for AI processing
        ai_start = time.time()
        
        # Create persona-aware prompt
        prompt = self._create_prompt(scenario)
        
        try:
            print("🧠 Agent thinking...")
            response = model.generate_content([prompt, image])
            ai_processing_time = time.time() - ai_start
            
            # Parse response
            parse_start = time.time()
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
            agent_choice = json.loads(cleaned_response)
            parse_time = time.time() - parse_start
            
            # Total processing time
            total_processing_time = capture_time + ai_processing_time + parse_time
            
            # Evaluate result
            success, error_type = self._evaluate_result(scenario, agent_choice)
            
            # Print results with persona interaction details
            print(f"🤖 Agent chose: {agent_choice.get('text', 'None')}")
            print(f"📍 Context: {agent_choice.get('context', 'None')}")
            print(f"✅ Expected: {scenario.expected_element}")
            
            # Show persona-specific interaction analysis
            if scenario.persona:
                print(f"👤 {scenario.persona.name} Interaction:")
                if success:
                    print(f"   ✅ CORRECT: {scenario.persona.behavioral_pattern}")
                    print(f"   🎯 Matched persona's goal: {scenario.persona.primary_goal}")
                else:
                    print(f"   ❌ MISMATCH: Expected {scenario.expected_element} but chose {agent_choice.get('text', 'None')}")
                    print(f"   🤔 This doesn't align with persona's pattern: {scenario.persona.behavioral_pattern}")
            
            print(f"⏱️  Timing Breakdown:")
            print(f"   📸 Screen capture: {capture_time:.2f}s")
            print(f"   🧠 AI processing: {ai_processing_time:.2f}s")
            print(f"   🔧 Response parsing: {parse_time:.2f}s")
            print(f"   ⏱️  Total time: {total_processing_time:.2f}s")
            
            if success:
                print("🎉 SUCCESS: Agent made the correct choice!")
            else:
                print(f"❌ FAILURE: {error_type}")
            
            return {
                "scenario_name": scenario.name,
                "persona": scenario.persona.name if scenario.persona else None,
                "variant": variant,
                "is_ab_test": scenario.is_ab_test,
                "success": success,
                "error_type": error_type,
                "processing_time": total_processing_time,
                "capture_time": capture_time,
                "ai_processing_time": ai_processing_time,
                "parse_time": parse_time,
                "agent_choice": agent_choice,
                "expected_choice": {"text": scenario.expected_element, "context": scenario.expected_context}
            }
            
        except Exception as e:
            ai_processing_time = time.time() - ai_start
            total_processing_time = capture_time + ai_processing_time
            print(f"❌ ERROR: {e}")
            print(f"⏱️  Timing (partial):")
            print(f"   📸 Screen capture: {capture_time:.2f}s")
            print(f"   🧠 AI processing: {ai_processing_time:.2f}s")
            print(f"   ⏱️  Total time: {total_processing_time:.2f}s")
            return {
                "scenario_name": scenario.name,
                "persona": scenario.persona.name if scenario.persona else None,
                "variant": variant,
                "is_ab_test": scenario.is_ab_test,
                "success": False,
                "error_type": "system_error",
                "processing_time": total_processing_time,
                "capture_time": capture_time,
                "ai_processing_time": ai_processing_time,
                "parse_time": 0.0,
                "agent_choice": None,
                "expected_choice": {"text": scenario.expected_element, "context": scenario.expected_context}
            }
    
    def run_full_test_suite(self, iterations: int = 3) -> Dict:
        """Run the complete A/B test suite with persona-based testing"""
        print("🚀 Starting Advanced Persona-Based A/B Test Suite...")
        print(f"📊 Running {len(self.scenarios)} scenarios with {iterations} iterations each")
        print(f"👥 Testing with {len(self.personas)} distinct personas")
        print("🎯 Testing Button Color Impact on AI Agent Behavioral Patterns")
        print("=" * 60)
        
        results = {
            "test_config": {
                "total_scenarios": len(self.scenarios),
                "iterations_per_scenario": iterations,
                "total_tests": len(self.scenarios) * iterations * 2,  # Both variants
                "personas": [p.name for p in self.personas]
            },
            "variant_a_results": [],
            "variant_b_results": [],
            "ab_comparison": {},
            "persona_analysis": {}
        }
        
        # Test Variant A
        print("\n🔵 TESTING VARIANT A (Current UI)")
        print("=" * 40)
        self._load_elements_map("elements_variant_a.json")
        
        for i, scenario in enumerate(self.scenarios, 1):
            print(f"\n📋 Scenario {i}/{len(self.scenarios)}: {scenario.name}")
            if scenario.persona:
                print(f"👤 Persona: {scenario.persona.name}")
            print("-" * 40)
            
            scenario_results = []
            for iteration in range(iterations):
                print(f"\n🔄 Iteration {iteration + 1}/{iterations}")
                result = self.run_single_test(scenario, "A")
                scenario_results.append(result)
                
                # Add to Variant A metrics
                self.metrics_a.add_result(
                    success=result["success"],
                    error_type=result["error_type"],
                    processing_time=result["processing_time"],
                    capture_time=result["capture_time"],
                    ai_processing_time=result["ai_processing_time"],
                    parse_time=result["parse_time"]
                )
                
                time.sleep(1)
            
            # Calculate scenario metrics for Variant A
            scenario_success_rate = sum(1 for r in scenario_results if r["success"]) / len(scenario_results) * 100
            avg_processing_time = sum(r["processing_time"] for r in scenario_results) / len(scenario_results)
            
            results["variant_a_results"].append({
                "scenario_name": scenario.name,
                "persona": scenario.persona.name if scenario.persona else None,
                "is_ab_test": scenario.is_ab_test,
                "success_rate": round(scenario_success_rate, 2),
                "avg_processing_time": round(avg_processing_time, 2),
                "iterations": scenario_results
            })
            
            print(f"\n📈 Variant A Summary:")
            print(f"   Success Rate: {scenario_success_rate:.1f}%")
            print(f"   Avg Processing Time: {avg_processing_time:.2f}s")
            
            # Show interaction summary for this scenario
            if scenario.persona:
                print(f"👤 {scenario.persona.name} Interaction Summary:")
                correct_choices = [r for r in scenario_results if r["success"]]
                incorrect_choices = [r for r in scenario_results if not r["success"]]
                
                if correct_choices:
                    print(f"   ✅ Correct choices: {len(correct_choices)}")
                    for choice in correct_choices:
                        print(f"      - '{choice['agent_choice'].get('text', 'None')}' ({choice['agent_choice'].get('context', 'None')})")
                
                if incorrect_choices:
                    print(f"   ❌ Incorrect choices: {len(incorrect_choices)}")
                    for choice in incorrect_choices:
                        print(f"      - Chose: '{choice['agent_choice'].get('text', 'None')}' instead of '{scenario.expected_element}'")
        
        # Test Variant B
        print("\n🟡 TESTING VARIANT B (Button Color Change)")
        print("=" * 40)
        self._load_elements_map("elements_variant_b.json")
        
        for i, scenario in enumerate(self.scenarios, 1):
            print(f"\n📋 Scenario {i}/{len(self.scenarios)}: {scenario.name}")
            if scenario.persona:
                print(f"👤 Persona: {scenario.persona.name}")
            print("-" * 40)
            
            scenario_results = []
            for iteration in range(iterations):
                print(f"\n🔄 Iteration {iteration + 1}/{iterations}")
                result = self.run_single_test(scenario, "B")
                scenario_results.append(result)
                
                # Add to Variant B metrics
                self.metrics_b.add_result(
                    success=result["success"],
                    error_type=result["error_type"],
                    processing_time=result["processing_time"],
                    capture_time=result["capture_time"],
                    ai_processing_time=result["ai_processing_time"],
                    parse_time=result["parse_time"]
                )
                
                time.sleep(1)
            
            # Calculate scenario metrics for Variant B
            scenario_success_rate = sum(1 for r in scenario_results if r["success"]) / len(scenario_results) * 100
            avg_processing_time = sum(r["processing_time"] for r in scenario_results) / len(scenario_results)
            
            results["variant_b_results"].append({
                "scenario_name": scenario.name,
                "persona": scenario.persona.name if scenario.persona else None,
                "is_ab_test": scenario.is_ab_test,
                "success_rate": round(scenario_success_rate, 2),
                "avg_processing_time": round(avg_processing_time, 2),
                "iterations": scenario_results
            })
            
            print(f"\n📈 Variant B Summary:")
            print(f"   Success Rate: {scenario_success_rate:.1f}%")
            print(f"   Avg Processing Time: {avg_processing_time:.2f}s")
            
            # Show interaction summary for this scenario
            if scenario.persona:
                print(f"👤 {scenario.persona.name} Interaction Summary:")
                correct_choices = [r for r in scenario_results if r["success"]]
                incorrect_choices = [r for r in scenario_results if not r["success"]]
                
                if correct_choices:
                    print(f"   ✅ Correct choices: {len(correct_choices)}")
                    for choice in correct_choices:
                        print(f"      - '{choice['agent_choice'].get('text', 'None')}' ({choice['agent_choice'].get('context', 'None')})")
                
                if incorrect_choices:
                    print(f"   ❌ Incorrect choices: {len(incorrect_choices)}")
                    for choice in incorrect_choices:
                        print(f"      - Chose: '{choice['agent_choice'].get('text', 'None')}' instead of '{scenario.expected_element}'")
        
        # Calculate A/B comparison
        results["ab_comparison"] = self._calculate_ab_comparison(results)
        
        # Calculate persona analysis
        results["persona_analysis"] = self._calculate_persona_analysis(results)
        
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
        
        # Create a mapping of scenario names to results
        variant_a_map = {r["scenario_name"]: r for r in results["variant_a_results"]}
        variant_b_map = {r["scenario_name"]: r for r in results["variant_b_results"]}
        
        for scenario_name in variant_a_map.keys():
            a_result = variant_a_map[scenario_name]
            b_result = variant_b_map[scenario_name]
            
            # Calculate differences
            success_rate_diff = b_result["success_rate"] - a_result["success_rate"]
            processing_time_diff = b_result["avg_processing_time"] - a_result["avg_processing_time"]
            
            comparison_item = {
                "scenario_name": scenario_name,
                "persona": a_result["persona"],
                "is_ab_test": a_result["is_ab_test"],
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
            
            if a_result["is_ab_test"]:
                comparison["ab_test_scenarios"].append(comparison_item)
            else:
                comparison["control_scenarios"].append(comparison_item)
        
        return comparison

    def _calculate_persona_analysis(self, results: Dict) -> Dict:
        """Analyze performance by persona"""
        persona_analysis = {}
        
        for persona in self.personas:
            persona_name = persona.name
            
            # Get all scenarios for this persona
            persona_scenarios_a = [r for r in results["variant_a_results"] if r["persona"] == persona_name]
            persona_scenarios_b = [r for r in results["variant_b_results"] if r["persona"] == persona_name]
            
            if persona_scenarios_a:
                avg_success_a = sum(s["success_rate"] for s in persona_scenarios_a) / len(persona_scenarios_a)
                avg_time_a = sum(s["avg_processing_time"] for s in persona_scenarios_a) / len(persona_scenarios_a)
                
                avg_success_b = sum(s["success_rate"] for s in persona_scenarios_b) / len(persona_scenarios_b)
                avg_time_b = sum(s["avg_processing_time"] for s in persona_scenarios_b) / len(persona_scenarios_b)
                
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
        report.append(f"**Total Tests:** {results['test_config']['total_tests']}")
        report.append(f"**Personas Tested:** {len(results['test_config']['personas'])}")
        report.append("")
        
        # Test Configuration
        report.append("## Test Configuration")
        report.append(f"- **Scenarios:** {results['test_config']['total_scenarios']}")
        report.append(f"- **Iterations per Scenario:** {results['test_config']['iterations_per_scenario']}")
        report.append(f"- **A/B Test Focus:** Button Color Impact on AI Agent Performance")
        report.append("")
        
        # Overall A/B Comparison
        report.append("## Overall A/B Test Results")
        variant_a_metrics = results["overall_metrics"]["variant_a"]
        variant_b_metrics = results["overall_metrics"]["variant_b"]
        
        report.append("### Variant A (Current UI)")
        report.append(f"- **Task Success Rate:** {variant_a_metrics['task_success_rate']}%")
        report.append(f"- **Average Processing Time:** {variant_a_metrics['avg_processing_time']}s")
        report.append(f"- **Total Tests:** {variant_a_metrics['total_tests']}")
        report.append("")
        
        report.append("### Variant B (Button Color Change)")
        report.append(f"- **Task Success Rate:** {variant_b_metrics['task_success_rate']}%")
        report.append(f"- **Average Processing Time:** {variant_b_metrics['avg_processing_time']}s")
        report.append(f"- **Total Tests:** {variant_b_metrics['total_tests']}")
        report.append("")
        
        # A/B Test Scenarios
        report.append("## A/B Test Scenarios (Button Color Impact)")
        for scenario in results["ab_comparison"]["ab_test_scenarios"]:
            report.append(f"### {scenario['scenario_name']}")
            report.append(f"**Persona:** {scenario['persona']}")
            report.append(f"**Variant A Success Rate:** {scenario['variant_a']['success_rate']}%")
            report.append(f"**Variant B Success Rate:** {scenario['variant_b']['success_rate']}%")
            report.append(f"**Success Rate Change:** {scenario['differences']['success_rate_change']}%")
            report.append(f"**Processing Time Change:** {scenario['differences']['processing_time_change']}s")
            report.append("")
        
        # Persona Analysis
        report.append("## Persona Performance Analysis")
        for persona_name, analysis in results["persona_analysis"].items():
            report.append(f"### {persona_name}")
            report.append(f"**Description:** {analysis['description']}")
            report.append(f"**Primary Goal:** {analysis['primary_goal']}")
            report.append("")
            report.append("**Performance Comparison:**")
            report.append(f"- Variant A Success Rate: {analysis['variant_a_performance']['avg_success_rate']}%")
            report.append(f"- Variant B Success Rate: {analysis['variant_b_performance']['avg_success_rate']}%")
            report.append(f"- Success Rate Change: {analysis['improvement']['success_rate_change']}%")
            report.append(f"- Processing Time Change: {analysis['improvement']['processing_time_change']}s")
            report.append("")
        
        # Control Scenarios
        report.append("## Control Scenarios (Should Perform Identically)")
        for scenario in results["ab_comparison"]["control_scenarios"]:
            report.append(f"### {scenario['scenario_name']}")
            report.append(f"**Persona:** {scenario['persona']}")
            report.append(f"**Variant A Success Rate:** {scenario['variant_a']['success_rate']}%")
            report.append(f"**Variant B Success Rate:** {scenario['variant_b']['success_rate']}%")
            report.append(f"**Success Rate Difference:** {scenario['differences']['success_rate_change']}%")
            report.append("")
        
        return "\n".join(report)

def main():
    """Main function to run the persona-based A/B testing framework"""
    print("🔬 BLIND Persona-Based AI Agent UI A/B Testing Framework")
    print("🎯 Testing Button Color Impact on AI Agent Performance (No Bias)")
    print("=" * 60)
    
    # Initialize framework
    framework = ABTestingFramework()
    
    # Display personas
    print("\n👥 Testing with 6 Distinct Personas:")
    for i, persona in enumerate(framework.personas, 1):
        print(f"{i}. {persona.name}")
        print(f"   Goal: {persona.primary_goal}")
        print(f"   Pattern: {persona.behavioral_pattern[:100]}...")
        print()
    
    # Use default iterations for automated testing
    iterations = 3
    print(f"Running {iterations} iterations per scenario...")
    
    print(f"\n🚀 Starting {iterations} iterations per scenario...")
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
    
    print(f"🔵 Variant A (Current): {variant_a_metrics['task_success_rate']}% success, {variant_a_metrics['avg_processing_time']}s avg")
    print(f"🟡 Variant B (Color Change): {variant_b_metrics['task_success_rate']}% success, {variant_b_metrics['avg_processing_time']}s avg")
    
    success_diff = variant_b_metrics['task_success_rate'] - variant_a_metrics['task_success_rate']
    time_diff = variant_b_metrics['avg_processing_time'] - variant_a_metrics['avg_processing_time']
    
    print(f"📊 Button Color Impact: {success_diff:+.1f}% success rate, {time_diff:+.2f}s processing time")
    print(f"🎯 Total Tests: {variant_a_metrics['total_tests'] + variant_b_metrics['total_tests']}")
    
    # Show final interaction comparison
    print(f"\n🎭 Persona Interaction Comparison:")
    for persona_name, analysis in results["persona_analysis"].items():
        print(f"\n👤 {persona_name}:")
        print(f"   🔵 Variant A: {analysis['variant_a_performance']['avg_success_rate']}% success, {analysis['variant_a_performance']['avg_processing_time']}s")
        print(f"   🟡 Variant B: {analysis['variant_b_performance']['avg_success_rate']}% success, {analysis['variant_b_performance']['avg_processing_time']}s")
        print(f"   📈 Change: {analysis['improvement']['success_rate_change']:+.1f}% success, {analysis['improvement']['processing_time_change']:+.2f}s")

if __name__ == "__main__":
    main() 