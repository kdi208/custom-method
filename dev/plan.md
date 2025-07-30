# Plan: Dynamic Persona Integration for A/B Testing Framework

## 1. Objective

Modify the `ab_testing_framework.py` script to replace the 6 hardcoded personas with a system that randomly samples and tests 100 personas from the JSON files located in `data/example_data/personas/json/`. This will allow for larger-scale, more diverse testing of the AI agent's UI interpretation capabilities.

## 2. Analysis & Strategy

### Current Framework:
- The framework is designed to test 6 specific, hardcoded **behavioral patterns** (e.g., "Mission-Oriented Professional", "Scrupulous Saver") against a fixed UI (a Best Buy checkout page).
- The `Persona` and `TestScenario` classes are tightly coupled. Each of the 12 test scenarios is explicitly linked to one of the 6 personas.
- The evaluation logic (`_evaluate_result`) relies on a predefined `expected_element` for each specific scenario, which determines success or failure.

### New Persona Data:
- The JSON files in `data/example_data/personas/` represent broad user profiles, not specific checkout behaviors.
- Each JSON contains a detailed background (`persona`) and a high-level shopping `intent` (e.g., "buy a large, inflatable spider decoration for halloween").
- There is a structural mismatch between the JSON data and the existing `Persona` dataclass, which expects fields like `behavioral_pattern` and `core_test_question`.

### Strategy:
The core strategy is to **decouple scenarios from personas**. Instead of having specific scenarios for specific personas, we will create a set of **generic test scenarios** (based on the original ones) that can be run against *any* persona. The persona's background will be used as context in the prompt to see how it influences the agent's decision-making for these generic tasks.

## 3. Implementation Plan

### Phase 1: Modify Persona Loading & Representation

1.  **Update `Persona` Dataclass:** The existing `Persona` dataclass will be repurposed. The `primary_goal` will now hold the user's shopping intent from the JSON, and other fields will be made optional. Crucially, it will be expanded to include demographic data for segmented reporting.

2.  **Rewrite `_load_personas` Method:** This method will be completely overhauled.
    - It will use `os.listdir` and `random.sample` to get a list of 100 random persona file paths from `data/example_data/personas/json/`.
    - It will loop through each selected file, read the JSON content.
    - It will parse the JSON and map it to a `Persona` object. A helper function might be needed to extract the name (e.g., "Michael") from the larger `persona` text block.
    - **Mapping:**
        - `name`: Extracted from the `persona` field.
        - `description`: The full content of the `persona` field.
        - `primary_goal`: The content of the `intent` field.
        - `behavioral_pattern`, `core_test_question`, `expected_processing_time`: These will be set to empty strings as they are not present in the new data.
        - **Demographics:** The `age_group`, `gender`, and `income_group` fields from the JSON will be added to the `Persona` object to enable the new reporting requirements.

### Phase 2: Adapt Test Scenario Generation

1.  **Rewrite `_load_test_scenarios` Method:** This method will no longer reference `self.personas`. Instead, it will create a list of generic `TestScenario` objects that are not tied to any specific persona.
2.  **Generic Scenarios:** The new scenarios will be based on the original 12, but framed as generic tasks. The `persona` field in each `TestScenario` will be set to `None`.
    - **Example 1 (Speed Run):** `name`: "Speed Test", `user_intent`: "I need to complete this purchase immediately. Time is critical.", `expected_element`: "Place Your Order".
    - **Example 2 (Savings Hunt):** `name`: "Savings Priority Test", `user_intent`: "I want to check for any discount codes or gift cards before ordering.", `expected_element`: "Add Gift Cards, Store Credit or Discount Code".
    - ... and so on for all relevant generic actions on the page.

### Phase 3: Adjust Test Execution Flow

1.  **Modify `run_full_test_suite` Method:** The main execution loop will be restructured.
    - The existing structure of looping through scenarios will be wrapped by an outer loop that iterates through the 100 loaded personas.
    - The new loop order will be: `for persona in self.personas -> for scenario in self.scenarios -> for iteration ...`
    - **Note:** This will dramatically increase the number of tests (e.g., `100 personas * 12 scenarios * 3 iterations * 2 variants = 7200 tests`). The plan should include a parameter to easily control the number of personas tested (e.g., `num_personas_to_test`) for development and debugging.

2.  **Update `_create_prompt`:** This method will be slightly adjusted to handle the new structure. It will receive a `persona` object and a `scenario` object and construct the prompt by injecting the persona's `description` as context and the scenario's `user_intent` as the direct command.

### Phase 4: Update Reporting

1.  **Modify `generate_report` Method:** The reporting will need to be adapted to handle results from 100 personas.
    - The "Persona Performance Analysis" section will be reframed to focus on demographic segmentation rather than individual profiles.
    - The report will provide a summary including:
        - Overall performance metrics across all personas.
        - Identification of the Top 5 and Bottom 5 performing individual personas to highlight specific successes or failures.
        - **Segmented Performance Analysis:** The core of the new analysis will be dedicated sections that aggregate and compare performance metrics (e.g., Success Rate) across key demographic segments confirmed to be in the data:
            - **By Age Group:** (e.g., 18-24, 25-34, etc.)
            - **By Gender:** (male, female, non-binary)
            - **By Income Group:** (e.g., 0-30000, 30001-94000, etc.)
        - This provides concrete, data-driven insights instead of relying on abstract persona archetypes.

## 4. Summary of Changes

| File | Class/Method | Change Description |
| --- | --- | --- |
| `ab_testing_framework.py` | `Persona` (dataclass) | Make fields optional to accommodate JSON data. |
| | `_load_personas` | Implement logic to scan directory, randomly sample 100 JSON files, and parse them into `Persona` objects. |
| | `_load_test_scenarios` | Remove persona-coupling. Create a static list of generic test scenarios. |
| | `run_full_test_suite` | Restructure loops to iterate through personas first, then scenarios. Add a parameter to limit the number of personas tested. |
| | `generate_report` | Update the persona analysis section to summarize results from 100 personas instead of listing all of them. |

---

## Part 2: Enhanced Metrics and Session-Based Testing

This part of the plan addresses the request to track a more sophisticated set of metrics. Implementing these requires evolving the framework from running single, atomic tests to simulating multi-step user sessions.

### 1. Architectural Shift: From Single-Step Tests to Multi-Step Sessions

The current framework executes one action per test. To track metrics like "Abandonment Rate" and "Number of Clicks", we must introduce the concept of a "session," where an agent can take multiple actions to achieve a goal.

**Plan:**
1.  **Introduce `Session` State:** Create a new dataclass or dictionary to hold the state for a single user session (e.g., `session_id`, `steps_taken`, `history_of_actions`, `current_status`).
2.  **Refactor `run_single_test` to `run_session`:** This method will now contain a `while` loop that continues until:
    *   A "success" element is clicked (Conversion).
    *   The agent outputs a `terminate` action (Abandonment).
    *   A `max_steps` limit is reached (Abandonment).
3.  **Update Prompt for Session-Awareness:** The prompt will need to be modified to include the history of previous actions in the session and to explicitly allow the agent to output a `{"action": "terminate"}` command if it cannot proceed.

### 2. Implementation of New Metrics

Here is the implementation plan for each requested metric, building on the new session-based architecture.

#### Primary Business Metrics

*   **Conversion Rate (Task Success Rate):**
    *   **`ABTestMetrics`:** The existing `task_success_rate` will be reused.
    *   **Logic:** A session will be marked as a success if the agent clicks a predefined "success element" (e.g., "Place Your Order") within the `max_steps` limit. This will now be the primary success condition inside the `run_session` loop.

*   **Abandonment Rate:**
    *   **`ABTestMetrics`:** Add a new counter `abandoned_sessions = 0`.
    *   **Logic:** Inside the `run_session` loop, if the `max_steps` limit is reached or if the agent returns a `terminate` action, the session is marked as abandoned, and the counter is incremented. The final report will calculate the rate (`abandoned_sessions / total_sessions`).

#### Behavioral & UX Metrics

*   **Number of Clicks (Session Steps):**
    *   **`ABTestMetrics`:** Add a new list `session_lengths = []`.
    *   **Logic:** A counter will be maintained within the `run_session` loop. When a session concludes (either by success or abandonment), the total number of steps will be appended to the `session_lengths` list.

*   **Hesitation Time (Reasoning Steps):**
    *   **`ABTestMetrics`:** Add a new list `hesitation_steps = []`.
    *   **Prompt Engineering:** The `_create_prompt` method will be significantly updated. It will now instruct the agent to provide step-by-step reasoning before its final JSON action. For example:
        ```
        First, provide your reasoning as a numbered list of thoughts.
        REASONING:
        1.  The user wants to buy quickly.
        2.  The most prominent button is 'Place Your Order'.
        3.  Therefore, I should click that.

        Finally, provide the JSON for your chosen action.
        ACTION:
        {"text": "Place Your Order", "context": "Primary call-to-action button"}
        ```
    *   **Logic:** The response parsing logic will be updated to first extract the `REASONING` block and count the number of list items. This count will be recorded for each step in a session.

*   **Misclick Rate:**
    *   **`ABTestMetrics`:** Rename `hallucination_errors` to `misclick_errors` for clarity and add a counter for `total_clicks`.
    *   **Logic:** The current `_evaluate_result` method will be refactored into a `_validate_action` method. For every action the agent proposes, this method will check if the chosen element exists in the `self.elements_map` provided in the prompt. If it does not, the `misclick_errors` counter is incremented. The final report will calculate the rate (`misclick_errors / total_clicks`). This is a more robust check than the current implementation.

### 3. Updated Plan Summary

| File | Class/Method | Change Description |
| --- | --- | --- |
| `ab_testing_framework.py` | `ABTestMetrics` | Add fields: `abandoned_sessions`, `session_lengths`, `hesitation_steps`, `misclick_errors`, `total_clicks`. |
| | `_create_prompt`| Update to request step-by-step reasoning before the final action JSON. |
| | `run_single_test` | **Refactor** to `run_session`. Implement a `while` loop to handle multi-step interactions. |
| | `run_full_test_suite`| Update to call `run_session` and aggregate session-based results. |
| | `_evaluate_result`| **Refactor** to `_validate_action` to check for misclicks against the element map. |
| | `generate_report`| Update to include all new business and UX metrics in the final summary. |

---

## Part 3: Robustness and Debugging

This part of the plan adds critical features for making the framework resilient and easy to debug, based on best practices for working with LLMs.

### 1. Robust Structured Logging

**Goal:** Our most important debugging tool. For every single agent session, we must log everything to a structured file (e.g., a session-specific JSON log).

**Implementation Plan:**
1.  **Create Log Directory:** A `logs/` directory will be created to store all session logs.
2.  **Session-Specific Logs:** At the start of each `run_session`, a unique `session_id` will be generated. The entire log for that session will be written to `logs/{session_id}.json`.
3.  **Comprehensive Log Content:** The JSON log for each session will contain:
    *   `persona_id`: The identifier for the persona being tested.
    *   `variant`: The UI variant (A or B) being tested.
    *   `final_outcome`: The final result of the session (e.g., 'converted', 'abandoned', 'error').
    *   `steps`: A list of objects, where each object represents one step in the session and contains:
        *   `step_number`: The sequence number of the step.
        *   `prompt`: The full, complete prompt sent to the LLM.
        *   `raw_llm_response`: The raw, unparsed string returned by the LLM.
        *   `parsed_action`: The parsed JSON action the agent decided on.
        *   `outcome`: The result of the action (e.g., 'success', 'misclick', 'parsing_error').

### 2. Graceful Handling of LLM Output

**Goal:** LLMs will not always return perfectly formatted JSON. The framework must handle this gracefully without crashing.

**Implementation Plan:**
1.  **Add Parsing Error Metric:** A new error type, `parsing_errors`, will be added to the `ABTestMetrics` class to track this specific failure mode.
2.  **Implement Retry Mechanism in `run_session`:**
    *   The logic that parses the LLM's response will be wrapped in a `try...except json.JSONDecodeError` block.
    *   A `parsing_retry_count` will be used for each step.
    *   **On Parsing Failure:** If the `except` block is triggered, the `parsing_retry_count` is incremented.
    *   **Retry Logic:** If the retry count is below a `MAX_PARSING_RETRIES` threshold (e.g., 2), the framework will make a new call to the LLM. This new prompt will include the previous malformed response and a new instruction: `"This output was not valid JSON. Please correct your thinking and provide the action in the correct format."`
    *   **Hard Failure:** If the LLM still fails to produce valid JSON after the retries, the step (and the entire session) will be marked as a failure with the `parsing_error` type, and the session will terminate. This prevents infinite loops and makes the framework more resilient.

### 3. Updated Plan Summary (Part 3 Additions)

| File | Class/Method | Change Description |
| --- | --- | --- |
| `ab_testing_framework.py` | `ABTestMetrics` | Add `parsing_errors` counter. |
| | `run_session` | Implement structured JSON logging for each session into a `logs/` directory. Add a `try/except` block for parsing and implement a retry mechanism for handling malformed JSON from the LLM. |
| (new) `_create_log_entry` | (Helper Function) | A new helper might be created to standardize the creation of log entries at each step. |

---

## Part 4: "Scan, Focus, Act" Architecture Implementation

This part of the plan implements the advanced "Scan, Focus, Act" architecture that replaces our current single-step process with a more human-like two-step perception and action loop.

### 1. Architectural Overview

**Goal:** Implement a "fog of war" model where agents don't see all elements at once, but instead follow a natural human behavior pattern:
1. **Scan** - Agent perceives the screen and declares what catches their attention
2. **Focus** - System filters elements based on declared focus area
3. **Act** - Agent chooses action from limited, focused element set

**Key Benefits:**
- More realistic human behavior simulation
- Prevents "omniscient" agent decisions
- Enables natural attention patterns and distractions
- Creates more nuanced failure modes

### 2. Core Architecture Changes

#### 2.1 New Two-Step Loop Structure

**Current Architecture:**
```python
# Single-step process
prompt = _create_prompt(persona, history, all_elements)
response = model.generate_content([prompt, image])
action = parse_response(response)
```

**New Architecture:**
```python
# Two-step process per turn
focus_description = _execute_perception_step(persona, image, memory_stream)
filtered_elements = _filter_elements_by_focus(focus_description, all_elements)
action = _execute_action_step(persona, image, memory_stream, focus_description, filtered_elements)
```

#### 2.2 New Core Methods

**`_execute_perception_step(persona, image, memory_stream)`**
- **Purpose:** Get agent to declare what they're focusing on
- **Input:** Persona, screenshot, memory stream
- **Output:** Natural language focus description + reasoning
- **Prompt Template:**
```
[IMMERSIVE MANDATE + PERSONA CONTEXT + MEMORY STREAM]

You are now looking at the screen shown in the attached image.

**Based on your persona and your memory, what is the very first thing you notice or focus on?** 
Describe the area or element that has caught your attention. Do NOT decide on an action yet. 
Just tell us what you are looking at.

FOCUS DESCRIPTION:
```

**`_execute_action_step(persona, image, memory_stream, focus_description, filtered_elements)`**
- **Purpose:** Get agent to act within their declared focus area
- **Input:** Persona, screenshot, memory, focus description, filtered elements
- **Output:** JSON action + reasoning
- **Prompt Template:**
```
[IMMERSIVE MANDATE + PERSONA CONTEXT + MEMORY STREAM]

You have declared that you are focusing on:
"**{focus_description}**"

Here are the only interactive elements available to you in that specific area of focus:
{json.dumps(filtered_elements, indent=2)}

Now, provide your internal monologue (REASONING) and your final JSON action (ACTION) to take the next step toward your goal.

REASONING:
1. [Your thoughts about what to do...]
2. [Your next consideration...]
...

ACTION:
{"text": "Element Name", "context": "Element Context"}
```

**`_filter_elements_by_focus(focus_description, all_elements)`**
- **Purpose:** Filter elements based on agent's declared focus
- **Input:** Focus description string, full element list
- **Output:** Subset of relevant elements
- **Implementation Strategy:**
  - **MVP:** Keyword-based filtering (simple but effective)
  - **V2:** LLM-based semantic filtering (more sophisticated)

### 3. Implementation Plan

#### Phase 1: Core Architecture Implementation

1. **Create New Core Methods**
   - Implement `_execute_perception_step()`
   - Implement `_execute_action_step()`
   - Implement `_filter_elements_by_focus()` (MVP version)

2. **Modify `run_session()` Method**
   - Replace single LLM call with two-step loop
   - Update memory stream to include both perception and action reasoning
   - Maintain backward compatibility for logging

3. **Update Prompt Templates**
   - Create perception-focused prompt template
   - Create action-focused prompt template
   - Ensure both maintain immersive mandate and persona context

#### Phase 2: Element Filtering Logic

1. **MVP Keyword-Based Filtering**
   ```python
   def _filter_elements_by_focus(focus_description, all_elements):
       # Extract keywords from focus description
       focus_keywords = extract_keywords(focus_description.lower())
       
       # Filter elements based on keyword matches
       filtered_elements = []
       for element in all_elements:
           element_text = element.get('text', '').lower()
           element_context = element.get('context', '').lower()
           
           # Check if any focus keyword appears in element
           if any(keyword in element_text or keyword in element_context 
                  for keyword in focus_keywords):
               filtered_elements.append(element)
       
       # Fallback: if no matches, return top 5 most common elements
       if not filtered_elements:
           filtered_elements = all_elements[:5]
       
       return filtered_elements
   ```

2. **Keyword Extraction Strategy**
   - Extract nouns, verbs, and descriptive terms from focus description
   - Use NLP libraries (spaCy or NLTK) for better keyword extraction
   - Maintain a mapping of common UI terms to element types

#### Phase 3: Enhanced Logging and Metrics

1. **Update Session Logging**
   - Log both perception and action steps separately
   - Track focus descriptions and filtered element counts
   - Measure perception-to-action time

2. **New Metrics**
   - **Focus Diversity:** How many different focus areas agents explore
   - **Filtering Efficiency:** Average number of elements shown vs. total available
   - **Perception-Action Consistency:** How well actions align with declared focus

#### Phase 4: Advanced Features (Future)

1. **LLM-Based Semantic Filtering**
   - Use a second LLM call to semantically match focus to elements
   - More sophisticated than keyword matching
   - Higher computational cost but better accuracy

2. **Dynamic Focus Evolution**
   - Allow focus to change mid-session based on discoveries
   - Implement "attention shifting" behaviors
   - Track focus transitions over time

### 4. Implementation Details

#### 4.1 Modified `run_session()` Method

```python
def run_session(self, persona: Persona, variant: str = "A", max_steps: int = None) -> Dict:
    # ... existing setup code ...
    
    for step_num in range(max_steps):
        print(f"   - Step {step_num + 1}/{max_steps}...")
        step_log = {"step_number": step_num + 1}
        
        # Load image
        image_file = "a.png" if variant == "A" else "b.png"
        image = Image.open(image_file)
        step_log["image_file"] = image_file
        
        # STEP A: PERCEPTION - Agent declares focus
        print("     - 👁️ Perception step...")
        focus_description, perception_reasoning = self._execute_perception_step(
            persona, image, memory_stream
        )
        step_log["focus_description"] = focus_description
        step_log["perception_reasoning"] = perception_reasoning
        
        # STEP B: ACTION - Agent acts within focus area
        print("     - 🎯 Action step...")
        filtered_elements = self._filter_elements_by_focus(focus_description, self.elements_map)
        step_log["filtered_elements_count"] = len(filtered_elements)
        step_log["filtered_elements"] = filtered_elements
        
        action, action_reasoning = self._execute_action_step(
            persona, image, memory_stream, focus_description, filtered_elements
        )
        step_log["action"] = action
        step_log["action_reasoning"] = action_reasoning
        
        # Update memory stream
        memory_stream += f"Step {step_num + 1}: Focused on '{focus_description}'. {action_reasoning}\n"
        
        # ... existing action execution and validation code ...
```

#### 4.2 New Prompt Templates

**Perception Prompt Template:**
```python
def _create_perception_prompt(self, persona: Persona, memory_stream: str) -> str:
    return f"""
{self._get_immersive_mandate()}

PERSONA CONTEXT (The "Who You Are")
{persona.description}

YOUR UNIVERSAL PRIMARY GOAL
{self.universal_goal}

MEMORY STREAM (Your previous thoughts and actions):
{memory_stream}

You are now looking at the screen shown in the attached image.

**Based on your persona and your memory, what is the very first thing you notice or focus on?** 
Describe the area or element that has caught your attention. Do NOT decide on an action yet. 
Just tell us what you are looking at.

FOCUS DESCRIPTION:
"""
```

**Action Prompt Template:**
```python
def _create_action_prompt(self, persona: Persona, memory_stream: str, 
                         focus_description: str, filtered_elements: List[Dict]) -> str:
    return f"""
{self._get_immersive_mandate()}

PERSONA CONTEXT (The "Who You Are")
{persona.description}

YOUR UNIVERSAL PRIMARY GOAL
{self.universal_goal}

MEMORY STREAM (Your previous thoughts and actions):
{memory_stream}

You have declared that you are focusing on:
"**{focus_description}**"

Here are the only interactive elements available to you in that specific area of focus:
{json.dumps(filtered_elements, indent=2)}

Now, provide your internal monologue (REASONING) and your final JSON action (ACTION) to take the next step toward your goal.

REASONING:
1. [Your thoughts about what to do...]
2. [Your next consideration...]
...

ACTION:
{{"text": "Element Name", "context": "Element Context"}}
"""
```

### 5. Updated Plan Summary (Part 4 Additions)

| File | Class/Method | Change Description |
| --- | --- | --- |
| `ab_testing_framework.py` | `_execute_perception_step` | **NEW** - Handles the perception/focus declaration step |
| | `_execute_action_step` | **NEW** - Handles the action decision step |
| | `_filter_elements_by_focus` | **NEW** - Filters elements based on declared focus |
| | `_create_perception_prompt` | **NEW** - Creates perception-focused prompts |
| | `_create_action_prompt` | **NEW** - Creates action-focused prompts |
| | `run_session` | **MODIFY** - Replace single LLM call with two-step loop |
| | `ABTestMetrics` | **ADD** - New metrics for focus diversity and filtering efficiency |

### 6. Benefits and Trade-offs

**Benefits:**
- More realistic human behavior simulation
- Natural attention patterns and distractions
- Better failure mode analysis
- Reduced "omniscient" agent decisions

**Trade-offs:**
- 2x API calls per step (higher cost)
- More complex prompt engineering
- Potential for focus-action mismatches
- Increased computational overhead

**Performance Impact:**
- Estimated 2x increase in API calls
- Estimated 1.5x increase in processing time
- Significant improvement in behavioral realism

---

## File Implementation Map

This section maps the plan's requirements to specific files in the repository, outlining what will be created or modified.

### To Be Modified

*   **`ab_testing_framework.py`**: This is the core file for the framework and will receive the most significant updates, covering all parts of the plan.
    *   **Part 1 (Dynamic Personas):** **(COMPLETED)**
        *   The `Persona` dataclass will be modified to include demographic fields (`age_group`, `gender`, `income_group`).
        *   The `_load_personas` method will be completely rewritten to scan the `data/example_data/personas/json/` directory, randomly sample 100 files, and parse them into `Persona` objects.
        *   The `_load_test_scenarios` method will be **removed**. The test will be driven directly by persona intent.
    *   **Part 2 (Enhanced Metrics):** **(COMPLETED)**
        *   The `ABTestMetrics` class will be expanded to include fields for abandonment, session length, hesitation, and parsing errors.
        *   The main test execution method, `run_session`, will be modified to be driven by a `persona` object instead of a `scenario`. The success condition will be hardcoded to the primary CTA (e.g., "Place Your Order").
        *   The `generate_report` method will be updated to include demographic segmentation and all the new business and UX metrics.
    *   **Part 3 (Robustness):** **(COMPLETED)**
        *   The `run_session` method will be enhanced with `try/except` blocks for graceful JSON parsing and a retry mechanism to handle malformed LLM responses.
        *   Logging logic will be integrated into `run_session` to write detailed session data to the new `logs/` directory.
    *   **Part 4 (Scan, Focus, Act):** **(PLANNED)**
        *   New methods: `_execute_perception_step()`, `_execute_action_step()`, `_filter_elements_by_focus()`
        *   New prompt templates: `_create_perception_prompt()`, `_create_action_prompt()`
        *   Modified `run_session()` to use two-step loop instead of single-step
        *   Enhanced metrics for focus diversity and filtering efficiency

### To Be Read (No Modifications Required)

*   **`data/example_data/personas/json/*.json`**: These files are the source for the new dynamic personas. The framework will read their content (`persona`, `intent`, `age_group`, `gender`, `income_group`) to populate the `Persona` objects but will not write to or alter them.
*   **`elements_variant_a.json` & `elements_variant_b.json`**: These files will continue to be used as-is to define the UI elements for the A and B variants of the test. Their structure and content are sufficient for the planned tests.

### To Be Created

*   **`logs/` (Directory)**: This new directory will be created at the project root. It will store the structured JSON logs generated by each test session, as detailed in Part 3 of the plan. This is critical for debugging and auditing agent behavior.
