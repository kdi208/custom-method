#!/usr/bin/env python3
"""
Configuration file for A/B Testing Framework
Modify these values to change test parameters without touching the main code.
"""

# =============================================================================
# TEST CONFIGURATION
# =============================================================================
# 
# To modify test parameters, simply change the values below:
# - num_personas: How many different personas to test (1-1000+ available)
# - iterations_per_persona: How many times to test each persona
# - max_steps_per_session: Maximum steps before session timeout
# - File paths: Locations for elements, personas, logs, and screenshots
#
# =============================================================================

TEST_CONFIG = {
    # Test Scale Configuration
    "num_personas": 5,            # Number of personas for this exploratory test (using super personas)
    "iterations_per_persona": 1,  # Number of iterations per persona
    "max_steps_per_session": 5,   # Maximum steps per session
    "universal_intent": "Your goal is to complete the purchase of the items in your cart.", # Universal intent for this test run

    # File Paths - Updated to use demo variants and super personas
    "variant_a_elements_file": "demo/elements_variant_a.json",
    "variant_b_elements_file": "demo/elements_variant_b.json",
    "personas_directory": "data/example_data/super/",
    "logs_directory": "logs/",
    "screenshots_directory": "screenshots/"
}

# =============================================================================
# PRESET CONFIGURATIONS
# =============================================================================
# Uncomment one of these to use a preset configuration:

# Quick Test (10 personas, 1 iteration each)
# TEST_CONFIG = {
#     "num_personas": 10,
#     "iterations_per_persona": 1,
#     "max_steps_per_session": 5,
#     "variant_a_elements_file": "elements_variant_a.json",
#     "variant_b_elements_file": "elements_variant_b.json",
#     "personas_directory": "data/example_data/personas/json/",
#     "logs_directory": "logs/",
#     "screenshots_directory": "screenshots/"
# }

# Medium Scale Test (50 personas, 2 iterations each)
# TEST_CONFIG = {
#     "num_personas": 50,
#     "iterations_per_persona": 2,
#     "max_steps_per_session": 5,
#     "variant_a_elements_file": "elements_variant_a.json",
#     "variant_b_elements_file": "elements_variant_b.json",
#     "personas_directory": "data/example_data/personas/json/",
#     "logs_directory": "logs/",
#     "screenshots_directory": "screenshots/"
# }

# Large Scale Test (100 personas, 3 iterations each)
# TEST_CONFIG = {
#     "num_personas": 100,
#     "iterations_per_persona": 3,
#     "max_steps_per_session": 5,
#     "variant_a_elements_file": "elements_variant_a.json",
#     "variant_b_elements_file": "elements_variant_b.json",
#     "personas_directory": "data/example_data/personas/json/",
#     "logs_directory": "logs/",
#     "screenshots_directory": "screenshots/"
# }

# =============================================================================
# CALCULATED VALUES
# =============================================================================

def get_total_sessions():
    """Calculate total number of sessions that will be run"""
    return TEST_CONFIG["num_personas"] * TEST_CONFIG["iterations_per_persona"] * 2

def print_configuration():
    """Print current configuration"""
    print("=" * 60)
    print("🔧 CURRENT TEST CONFIGURATION")
    print("=" * 60)
    print(f"👥 Personas to test: {TEST_CONFIG['num_personas']}")
    print(f"🔄 Iterations per persona: {TEST_CONFIG['iterations_per_persona']}")
    print(f"📏 Max steps per session: {TEST_CONFIG['max_steps_per_session']}")
    print(f"📊 Total sessions: {get_total_sessions()}")
    print(f"⏱️  Estimated time: {get_total_sessions() * 30} seconds (~{get_total_sessions() * 30 / 60:.1f} minutes)")
    print("=" * 60)

if __name__ == "__main__":
    print_configuration() 