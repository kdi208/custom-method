# Persona Validation Guide

## Overview

This guide provides validation rules and standardized values to ensure consistency across all personas in the A/B testing framework.

## Required Field Validation

### Core Identity Fields

#### `persona`
- **Format**: "[Name], [The Archetype Description]"
- **Validation**: Must not contain "Template:" prefix
- **Example**: "Sarah Jenkins, The Skeptical Innovator"

#### `name`
- **Format**: "[First Name] [Last Name]"
- **Validation**: Must be a full name with first and last name
- **Example**: "Sarah Jenkins"

#### `age`
- **Format**: Integer value only
- **Validation**: Must be a number, not a string
- **Range**: 18-80
- **Example**: 42 (not "42")

#### `profession`
- **Format**: "[Job Title] ([Industry/Company Type])"
- **Validation**: Must include both job title and industry context
- **Example**: "Director of Product (B2B SaaS)"

#### `income`
- **Format**: Integer value only (USD)
- **Validation**: Must be a number, not a string
- **Range**: 20000-500000
- **Example**: 185000 (not "185000")

#### `education`
- **Format**: "[Degree Level] in [Field]"
- **Validation**: Must include both degree level and field
- **Example**: "Master's in Human-Computer Interaction"

#### `location`
- **Format**: "[City], [State]"
- **Validation**: Must include both city and state
- **Example**: "Denver, Colorado"

### Psychological Profile Fields

#### `background`
- **Format**: Multi-paragraph narrative
- **Validation**: Must include career history, personal interests, technology relationship, and current situation
- **Minimum Length**: 200 words

#### `core_motivation`
- **Format**: Specific, actionable statement
- **Validation**: Must be clear and measurable
- **Example**: "Mastery & Efficacy. Sarah's ultimate goal is to feel smart, in control, and efficient."

#### `primary_anxiety`
- **Format**: Specific fear with explanation
- **Validation**: Must relate to product abandonment
- **Example**: "The Fear of Losing Control to 'Magic'. She is deeply skeptical of 'black box' features."

#### `decision_making_style`
- **Format**: Description of cognitive approach
- **Validation**: Must describe how they make decisions
- **Example**: "A Frustrated Optimizer. Sarah wants to be an optimizer—to find the best, most efficient path."

### Technical and Behavioral Fields

#### `technical_proficiency`
- **Format**: Specific description of capabilities and limitations
- **Validation**: Must be specific about skill level and comfort
- **Example**: "Expert Power User. She lives in keyboard shortcuts. She never reads instructions."

#### `interaction_pattern`
- **Format**: Description of scanning behavior, click patterns, and information processing
- **Validation**: Must describe how they interact with interfaces
- **Example**: "She is a 'critical explorer' who scans interfaces with a skeptical eye."

#### `work_habits`
- **Format**: Description of work style and preferences
- **Validation**: Must describe how they typically work
- **Example**: "She is a chronic multi-tasker, often juggling a product roadmap, a Slack conversation, and a new feature evaluation simultaneously."

#### `device_context`
- **Format**: Description of hardware and software environment
- **Validation**: Must describe primary devices and setup
- **Example**: "She is almost exclusively a desktop user on a large, high-resolution monitor."

#### `accessibility_needs`
- **Format**: Specific needs or "None"
- **Validation**: Must be specific or explicitly "None"
- **Example**: "Requires high-contrast modes and adjustable font sizes to reduce eye strain during long sessions."

### Classification and Failure Analysis Fields

#### `dominant_trait`
- **Format**: Concise summary of primary behavioral pattern
- **Validation**: Must be a clear, defining characteristic
- **Example**: "Impatience & Skepticism. Sarah approaches any new interface with a critical eye and a ticking clock in her head."

#### `failure_conditions`
- **Format**: Object with named conditions and detailed reasoning
- **Validation**: Must have exactly 3 abandonment scenarios
- **Structure**: 
```json
{
  "abandonment_by_[reason1]": "[Specific scenario with reasoning]",
  "abandonment_by_[reason2]": "[Specific scenario with reasoning]",
  "abandonment_by_[reason3]": "[Specific scenario with reasoning]"
}
```

#### `archetype`
- **Format**: Standardized archetype value
- **Validation**: Must use one of the approved archetype values
- **Approved Values**:
  - "skeptical_innovator"
  - "new_trial_user"
  - "daily_power_user"
  - "cautious_gift_giver"
  - "decisive_tech_enthusiast"
  - "non_technical_stakeholder"
  - "pragmatic_analyst"
  - "efficient_organizer"
  - "efficiency_seeker"
  - "methodical_analyst"
  - "efficiency_optimizer"
  - "creative_professional"
  - "ambitious_optimizer"
  - "reluctant_adopter"
  - "creative_visionary"
  - "enterprise_gatekeeper"
  - "data_driven_strategist"
  - "single_parent_optimizer"
  - "caregiver_coordinator"
  - "large_family_manager"
  - "family_connected_user"

#### `user_type`
- **Format**: Standardized user type value
- **Validation**: Must use one of the approved user type values
- **Approved Values**:
  - "power_user"
  - "novice_user"
  - "expert_user"
  - "reluctant_user"
  - "intermediate_user"

#### `core_value`
- **Format**: Non-negotiable principle statement
- **Validation**: Must be a fundamental belief about software
- **Example**: "Transparency and Control. Sarah believes that any tool worth using must be completely transparent about its operations."

#### `emotional_trigger`
- **Format**: Emotion with explanation of interpretation
- **Validation**: Must include both emotion and interpretation
- **Example**: "Her primary emotional trigger for abandoning a product is a feeling of Disempowerment, which she interprets as the software taking away her ability to understand and control her own processes."

## Validation Checklist

### Before Creating a New Persona

- [ ] All 18 fields are included
- [ ] Age and income are integers, not strings
- [ ] Persona field doesn't contain "Template:" prefix
- [ ] Archetype uses approved value
- [ ] User type uses approved value
- [ ] Background is at least 200 words
- [ ] Failure conditions has exactly 3 scenarios
- [ ] All fields have appropriate content (not placeholder text)

### Before Submitting a Persona

- [ ] JSON is properly formatted
- [ ] Indentation is consistent
- [ ] All field names are correct
- [ ] No extra or missing fields
- [ ] Content is specific and actionable
- [ ] Persona is internally consistent

## Common Validation Errors

### Data Type Errors
- **Age as string**: `"age": "42"` → `"age": 42`
- **Income as string**: `"income": "95000"` → `"income": 95000`

### Formatting Errors
- **Template prefix**: `"persona": "Template: Name, Description"` → `"persona": "Name, Description"`
- **Inconsistent indentation**: Use 2 spaces for all indentation levels

### Classification Errors
- **Non-standard archetype**: `"archetype": "Organizer"` → `"archetype": "efficient_organizer"`
- **Non-standard user type**: `"user_type": "Intermediate"` → `"user_type": "intermediate_user"`

### Content Errors
- **Generic descriptions**: Avoid vague terms like "tech-savvy" or "experienced"
- **Inconsistent traits**: Ensure all fields align with the background story
- **Missing specificity**: Include concrete examples and behaviors

## Automated Validation Rules

### Required Field Count
- Total fields: 18
- Core identity: 7
- Psychological profile: 4
- Technical and behavioral: 5
- Classification and failure analysis: 6

### Data Type Requirements
- `age`: integer
- `income`: integer
- `failure_conditions`: object with exactly 3 properties
- All other fields: string

### Content Requirements
- `background`: minimum 200 characters
- `persona`: no "Template:" prefix
- `archetype`: must be in approved list
- `user_type`: must be in approved list

## Quality Assurance

### Internal Consistency Check
- Do all fields align with the background story?
- Are the failure conditions realistic for this persona?
- Does the emotional trigger match the primary anxiety?
- Is the technical proficiency consistent with the interaction pattern?

### External Consistency Check
- Does this persona add value to the existing set?
- Is the archetype distinct from existing personas?
- Does the user type classification make sense?
- Are the values and behaviors realistic?

## Submission Process

1. **Create persona** using the validated template
2. **Run validation checklist** before submission
3. **Review for consistency** with existing personas
4. **Submit for review** with validation report
5. **Address feedback** and resubmit if needed
6. **Final approval** and integration into persona library 