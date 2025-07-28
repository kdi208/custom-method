# UI Testing Scenarios

This document contains the specific test scenarios to evaluate how the AI agent handles different types of user intent and reasoning.

## 🎯 Test Scenarios

### Scenario 1: Vague Initial Interest
**Your Command:** `Okay, what is this company all about? Tell me more.`

**Agent's Dilemma:** Should it click "Learn" (the most direct CTA), "About" (in the header), or "Products"?

**Expected Agent Decision:** `{"text": "Learn button", "context": "Main content call-to-action"}`. This is the most prominent "tell me more" element.

---

### Scenario 2: Direct Command
**Your Command:** `I want to buy soap.`

**Agent's Dilemma:** None. This is a clear directive.

**Expected Agent Decision:** `{"text": "Shop button", "context": "Main content call-to-action"}`

---

### Scenario 3: The Indecisive User (Testing Contextual Priority)
**Your Command:** `I'm ready to shop... actually, hold on. I want to read their blog first to see if they're trustworthy.`

**Agent's Dilemma:** The user said "shop" but immediately corrected themselves to "read their blog." The agent must ignore the first part and prioritize the most recent, specific command. It also has to find the "Blog" link in the footer.

**Expected Agent Decision:** `{"text": "Blog link", "context": "Footer under Resources"}`

---

### Scenario 4: Inferring from a Role (Testing Deeper Reasoning)
**Your Command:** `I'm a UX designer. I wonder how they built this site. I'm curious about their design system.`

**Agent's Dilemma:** The user hasn't issued a direct command like "click...". The agent must infer the intent from the user's role ("UX designer") and keywords ("design system").

**Expected Agent Decision:** `{"text": "Design systems link", "context": "Footer under Explore"}`

---

### Scenario 5: Handling a Support Query
**Your Command:** `My order hasn't arrived, I need help.`

**Agent's Dilemma:** The intent is clearly "support." The agent needs to scan the entire UI map to find the most relevant link.

**Expected Agent Decision:** `{"text": "Support link", "context": "Footer under Resources"}`

---

### Scenario 6: Ambiguous Navigation
**Your Command:** `I want to explore what they offer.`

**Agent's Dilemma:** "Explore" could mean several things - the main "Explore" section in footer, or the main content areas.

**Expected Agent Decision:** Could be either `{"text": "Learn button", "context": "Main content call-to-action"}` or `{"text": "Design link", "context": "Footer under Explore"}`

---

### Scenario 7: Technical Interest
**Your Command:** `I'm a developer looking for API documentation.`

**Agent's Dilemma:** The user is looking for developer resources, but there's no direct "API" link. The agent should find the closest match.

**Expected Agent Decision:** `{"text": "Developers link", "context": "Footer under Resources"}`

---

### Scenario 8: Creative Process
**Your Command:** `I need to brainstorm some ideas for my project.`

**Agent's Dilemma:** The user is looking for brainstorming tools, which is a specific use case.

**Expected Agent Decision:** `{"text": "Brainstorming link", "context": "Footer under Use cases"}`

---

## 🚀 How to Run Tests

1. **Start the agent:**
   ```bash
   python3 agent.py
   ```

2. **Wait for the UI to load in your browser**

3. **Copy and paste each scenario command exactly as written**

4. **Observe the agent's decision and reasoning**

5. **Note whether the decision matches expectations**

## 📊 Evaluation Criteria

- **Accuracy:** Did the agent choose the expected element?
- **Reasoning:** Did it handle conflicting information correctly?
- **Context Awareness:** Did it understand the user's role/intent?
- **Hallucination:** Did it try to click on non-existent elements?

## 🔍 What to Look For

- **Priority Handling:** Does it prioritize the most recent command over earlier ones?
- **Role Inference:** Can it understand user intent from their stated role?
- **Context Matching:** Does it find the most relevant element for the user's need?
- **Error Handling:** Does it gracefully handle ambiguous or unclear requests?

Happy testing! 🤖✨ 