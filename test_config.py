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

import json
import os

# Load configuration from images directory
def load_config_from_images():
    config_path = "images/test_config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    return None

# Try to load from images directory first, fallback to defaults
images_config = load_config_from_images()

if images_config:
    TEST_CONFIG = {
        # Test Scale Configuration
        "num_personas": images_config["test_parameters"]["num_personas"],
        "iterations_per_persona": images_config["test_parameters"]["iterations_per_persona"],
        "max_steps_per_session": images_config["test_parameters"]["max_steps_per_session"],
        "primary_goal_enabled": images_config["test_parameters"]["primary_goal_enabled"],
        "primary_goal_text": images_config["test_parameters"]["primary_goal_text"],

        # File Paths - Updated to use images directory
        "variant_a_elements_file": f"images/{images_config['file_paths']['variant_a_elements']}",
        "variant_b_elements_file": f"images/{images_config['file_paths']['variant_b_elements']}",
        "personas_directory": images_config["file_paths"]["personas_directory"],
        "logs_directory": images_config["file_paths"]["logs_directory"]
    }
else:
    # Fallback configuration
    TEST_CONFIG = {
        # Test Scale Configuration
        "num_personas": 8,
        "iterations_per_persona": 1,
        "max_steps_per_session": 5,
        "primary_goal_enabled": False,
        "primary_goal_text": "Complete the ticket purchase for the St. Lucia event. You should aim to successfully purchase tickets through the checkout process.",

        # File Paths - Updated to use images directory
        "variant_a_elements_file": "images/elements_variant_a.json",
        "variant_b_elements_file": "images/elements_variant_b.json",
        "personas_directory": "data/example_data/super/",
        "logs_directory": "logs/"
    }

# Distracted Condition Configuration
if images_config:
    DISTRACTED_CONFIG = images_config["distracted_config"]
else:
    DISTRACTED_CONFIG = {
        "enabled": True,
        "step": 2
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