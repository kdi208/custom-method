# A/B Testing Framework Configuration Guide

## Quick Configuration

To modify test parameters, edit `test_config.py`:

```python
TEST_CONFIG = {
    "num_personas": 20,           # Number of personas to test
    "iterations_per_persona": 2,  # Number of iterations per persona
    "max_steps_per_session": 5,   # Maximum steps per session
    # ... other settings
}
```

## Available Preset Configurations

The `test_config.py` file includes several preset configurations you can uncomment:

### Quick Test (10 personas, 1 iteration each)
- **Total Sessions:** 20
- **Estimated Time:** ~10 minutes
- **Use Case:** Development and debugging

### Medium Scale Test (50 personas, 2 iterations each)
- **Total Sessions:** 200
- **Estimated Time:** ~1.7 hours
- **Use Case:** Standard A/B testing

### Large Scale Test (100 personas, 3 iterations each)
- **Total Sessions:** 600
- **Estimated Time:** ~5 hours
- **Use Case:** Production testing with high confidence

## Current Configuration

Run this command to see your current settings:

```bash
python3 test_config.py
```

## Configuration Parameters

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `num_personas` | Number of different personas to test | 20 | 1-1000+ |
| `iterations_per_persona` | Times to test each persona | 2 | 1-10 |
| `max_steps_per_session` | Max steps before timeout | 5 | 1-20 |
| `variant_a_elements_file` | UI elements for Variant A | `elements_variant_a.json` | - |
| `variant_b_elements_file` | UI elements for Variant B | `elements_variant_b.json` | - |
| `personas_directory` | Directory with persona JSON files | `data/example_data/personas/json/` | - |
| `logs_directory` | Directory for session logs | `results/` | - |
| `screenshots_directory` | Directory for screenshots | `screenshots/` | - |

## Running Tests

1. **Configure:** Edit `test_config.py` with your desired settings
2. **Run:** Execute `python3 ab_testing_framework.py`
3. **Analyze:** Use `python3 analyze_results.py` for detailed metrics

## Example: Quick Test Setup

To run a quick test with 10 personas and 1 iteration each:

1. Edit `test_config.py`:
   ```python
   TEST_CONFIG = {
       "num_personas": 10,
       "iterations_per_persona": 1,
       # ... other settings remain the same
   }
   ```

2. Run the test:
   ```bash
   python3 ab_testing_framework.py
   ```

3. View results:
   ```bash
   python3 analyze_results.py
   ```

## Scaling Considerations

- **Small tests (10-20 personas):** Good for development and debugging
- **Medium tests (50-100 personas):** Good for standard A/B testing
- **Large tests (200+ personas):** Good for production confidence
- **Very large tests (500+ personas):** May take several hours, consider running overnight 