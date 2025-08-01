# Persona Field Guide

This document provides a comprehensive explanation of each field in the persona template and how to use them effectively for A/B testing and user experience design.

## Core Identity Fields

### `persona`
**Purpose**: A memorable, descriptive title that captures the essence of the persona
**Format**: "[Name], [The Archetype Description]"
**Example**: "Sarah, The Skeptical Innovator"
**Usage**: Used for quick identification and communication about the persona

### `name`
**Purpose**: The full name of the persona
**Format**: "[First Name] [Last Name]"
**Example**: "Sarah Jenkins"
**Usage**: Provides human connection and makes the persona more relatable

### `age`
**Purpose**: Age in years to provide demographic context
**Format**: Integer value
**Example**: 42
**Usage**: Helps understand generational technology preferences and life stage

### `profession`
**Purpose**: Job title and industry context
**Format**: "[Job Title] ([Industry/Company Type])"
**Example**: "Director of Product (B2B SaaS)"
**Usage**: Provides professional context and influences technical comfort level

### `income`
**Purpose**: Annual income to understand purchasing power and decision-making context
**Format**: Integer value in USD
**Example**: 185000
**Usage**: Influences expectations for premium features and willingness to pay

### `education`
**Purpose**: Highest level of education achieved
**Format**: "[Degree Level] in [Field]"
**Example**: "Master's in Human-Computer Interaction"
**Usage**: Indicates analytical thinking ability and comfort with complex concepts

### `location`
**Purpose**: Geographic location for cultural and regional context
**Format**: "[City], [State]"
**Example**: "Denver, Colorado"
**Usage**: May influence technology adoption patterns and cultural preferences

## Psychological Profile Fields

### `background`
**Purpose**: Detailed story explaining the persona's relationship with technology and current situation
**Format**: Multi-paragraph narrative
**Key Elements**:
- Career history and progression
- Personal interests and hobbies
- How personal interests translate to software interaction
- Current relationship with technology
- Specific situation or context for using the product

**Usage**: Provides the foundation for understanding all other behavioral aspects

### `core_motivation`
**Purpose**: Primary driving force that explains what they want to achieve and why
**Format**: Specific, actionable statement
**Example**: "Mastery & Efficacy. Sarah's ultimate goal is to feel smart, in control, and efficient."
**Usage**: Guides design decisions toward supporting their primary goals

### `primary_anxiety`
**Purpose**: Main fear or concern that could cause abandonment
**Format**: Specific fear with explanation
**Example**: "The Fear of Losing Control to 'Magic'. She is deeply skeptical of 'black box' features."
**Usage**: Helps identify potential failure points and design solutions to address concerns

### `decision_making_style`
**Purpose**: How they approach choices and problem-solving
**Format**: Description of cognitive approach
**Example**: "A Frustrated Optimizer. Sarah wants to be an optimizer—to find the best, most efficient path."
**Usage**: Informs UI design to match their decision-making patterns

## Technical and Behavioral Fields

### `technical_proficiency`
**Purpose**: Level of technical skill and comfort with technology
**Format**: Specific description of capabilities and limitations
**Example**: "Expert Power User. She lives in keyboard shortcuts. She never reads instructions."
**Usage**: Determines complexity level and amount of guidance needed

### `interaction_pattern`
**Purpose**: How they typically interact with interfaces
**Format**: Description of scanning behavior, click patterns, and information processing
**Example**: "She is a 'critical explorer' who scans interfaces with a skeptical eye."
**Usage**: Guides UI layout and information hierarchy decisions

### `work_habits`
**Purpose**: How they typically work, including multitasking and focus patterns
**Format**: Description of work style and preferences
**Example**: "She is a chronic multi-tasker, often juggling a product roadmap, a Slack conversation, and a new feature evaluation simultaneously."
**Usage**: Informs design for interruptions, notifications, and workflow integration

### `device_context`
**Purpose**: Primary devices, screen setup, and technical environment
**Format**: Description of hardware and software environment
**Example**: "She is almost exclusively a desktop user on a large, high-resolution monitor."
**Usage**: Determines responsive design requirements and feature prioritization

### `accessibility_needs`
**Purpose**: Any accessibility requirements or preferences
**Format**: Specific needs or "None"
**Example**: "Requires high-contrast modes and adjustable font sizes to reduce eye strain during long sessions."
**Usage**: Ensures inclusive design and compliance with accessibility standards

## Classification Fields

### `dominant_trait`
**Purpose**: The most defining characteristic that influences all interactions
**Format**: Concise summary of primary behavioral pattern
**Example**: "Impatience & Skepticism. Sarah approaches any new interface with a critical eye and a ticking clock in her head."
**Usage**: Quick reference for understanding the persona's primary behavioral driver

### `archetype`
**Purpose**: Categorization label for grouping similar personas
**Format**: Descriptive label
**Examples**: "skeptical_innovator", "daily_power_user", "cautious_gift_giver"
**Usage**: Enables persona clustering and pattern recognition across different user types

### `user_type`
**Purpose**: User experience level classification
**Format**: Experience level descriptor
**Examples**: "power_user", "novice_user", "expert_user", "reluctant_user"
**Usage**: Determines appropriate complexity level and onboarding approach

## Failure Analysis Fields

### `failure_conditions`
**Purpose**: Specific scenarios that would cause the persona to abandon the product
**Format**: Object with named conditions and detailed reasoning
**Structure**:
```json
{
  "abandonment_by_[reason]": "[Specific scenario with reasoning]"
}
```
**Usage**: Identifies critical failure points to address in design and testing

### `core_value`
**Purpose**: Fundamental belief about what software should provide
**Format**: Non-negotiable principle statement
**Example**: "Transparency and Control. Sarah believes that any tool worth using must be completely transparent about its operations."
**Usage**: Guides ethical design decisions and feature prioritization

### `emotional_trigger`
**Purpose**: Primary emotional state that would cause abandonment
**Format**: Emotion with explanation of interpretation
**Example**: "Her primary emotional trigger for abandoning a product is a feeling of Disempowerment, which she interprets as the software taking away her ability to understand and control her own processes."
**Usage**: Helps design emotional responses and identify potential user experience issues

## Usage Guidelines

### Creating Effective Personas

1. **Start with Background**: The background story should be rich and detailed, as it informs all other fields
2. **Ensure Consistency**: All fields should align with the background story and support each other
3. **Be Specific**: Avoid generic descriptions; use specific examples and behaviors
4. **Focus on Behavior**: Emphasize how the persona interacts with technology, not just who they are
5. **Include Failure Scenarios**: Understanding what causes abandonment is crucial for design decisions

### Testing Personas

1. **Use in A/B Testing**: Create test scenarios that specifically target each persona's needs and concerns
2. **Validate Assumptions**: Use real user data to validate persona assumptions
3. **Iterate**: Update personas based on testing results and new insights
4. **Cross-Reference**: Compare persona predictions with actual user behavior

### Design Applications

1. **Feature Prioritization**: Use personas to determine which features matter most
2. **UI Design**: Design interfaces that match persona interaction patterns
3. **Content Strategy**: Create messaging that addresses persona motivations and anxieties
4. **User Journey Mapping**: Map experiences that align with persona work habits and decision-making styles 