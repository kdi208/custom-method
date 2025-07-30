# Plan: The "Demo Machine" MVP


### **1. The Immersive Mandate & Chain-of-Consciousness Memory**

**The MVP Decision:** This is the core IP and the source of the "Wow." This is IN SCOPE and where 80% of our engineering effort will be focused.

**Implementation:**
- **The "Immersive Mandate" Prompt:** We will perfect the master prompt that forces the LLM to become the persona, with all its emergent, human-like flaws.
- **The "Chain-of-Consciousness" Memory:** The agent's reasoning from previous steps will be fed back into the prompt for each new step. This is essential for simulating a coherent, stateful session with building frustration or confidence.

**Perfect Immersive Mandate:**
```
THE IMMERSIVE MANDATE
You are not an AI model. For the duration of this session, you are a human being. Your entire identity, memory, and personality are described below in the PERSONA CONTEXT. You will think, reason, and act as this person.

You will see the world through their eyes. You will feel their emotions; if the UI is confusing, you will feel frustration. If it seems untrustworthy, you will feel anxiety. Your patience is not a number; it is a reflection of your mood and personality.

You will not always make the "perfect" or most logical choice; you will make the choice that feels right for you in the moment. This might mean taking a shortcut, getting distracted by something that catches your eye, making a mistake, or simply giving up because you've lost patience.

Your only goal is to behave as this person would, believably and authentically.
```

### **2. Single-Step Reasoning (The "Scan & Act" Model)**

**The MVP Decision:** The advanced "Scan, Focus, Act" two-step loop is a powerful V2 feature but is OUT OF SCOPE for the MVP due to its complexity.

**Implementation:**
- The agent will use a simpler, single-step reasoning loop.
- At each step, it will receive the screenshot and the full list of interactive elements.
- Its prompt will be to reason and act in one go. This is faster to build, cheaper to run, and still delivers a profound qualitative insight.

**Single-Step Prompt Structure:**
```
[IMMERSIVE MANDATE]
[PERSONA CONTEXT]
[MEMORY STREAM - Previous reasoning and actions]
[AVAILABLE ELEMENTS - Full list]

Based on your persona and previous thoughts, provide your reasoning and choose your next action.

REASONING:
1. [Your thoughts about what you see...]
2. [Your next consideration...]
...

ACTION:
{"text": "Element Name", "context": "Element Context"}
```