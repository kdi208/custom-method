# Test configuration for A/B testing framework
# Generated from test_config.json

TEST_CONFIG = {
    "num_personas": 20,
    "iterations_per_persona": 1,
    "max_steps_per_session": 5,
    "primary_goal_enabled": True,
    "primary_goal_text": "Complete the transaction",
    "variant_a_elements_file": "elements_variant_a.json",
    "variant_b_elements_file": "elements_variant_b.json",
    "personas_directory": "../personas/example_data/super/",
    "logs_directory": "../results/",
    "variant_a_image": "a.png",
    "variant_b_image": "b.png"
}

DISTRACTED_CONFIG = {
    "enabled": True,
    "step": 2
} 