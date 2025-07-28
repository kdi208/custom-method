# Persona-Based AI Agent UI A/B Testing Framework

## 🎯 **What We're Testing**

**Button Color Impact on AI Agent Performance**

This framework tests how different button colors affect AI agent decision-making and performance across four distinct user personas. The test focuses on the "Place Your Order" button in a Best Buy checkout page.

## 👥 **The Four Personas**

### 1. **Alex - Mission-Oriented Professional**
- **Who:** Busy project manager buying replacement TV for client presentation
- **Goal:** Complete purchase with maximum speed and minimum cognitive load
- **Behavior:** Immediately scans for most prominent "finish" action, ignores secondary information
- **Expected A/B Impact:** Green button = immediate targeting, Yellow button = full-page scan required

### 2. **Brenda - Scrupulous Saver**
- **Who:** Budget-conscious parent buying family gift
- **Goal:** Ensure no possible savings are missed before committing to purchase
- **Behavior:** Ignores primary button first, scans for discount codes and gift cards
- **Expected A/B Impact:** Low-contrast button might make secondary links more prominent

### 3. **Charles - Cautious Confirmer**
- **Who:** Retired individual comfortable with technology but very meticulous
- **Goal:** Verify accuracy of every detail before final click
- **Behavior:** Performs full "information verification" pass, reads terms and policies
- **Expected A/B Impact:** Green button = clear final step signal, Yellow button = potential anxiety

### 4. **Dana - Distracted Dabbler**
- **Who:** Multi-tasking parent working from home
- **Goal:** Eventually complete purchase, but focus will shift during process
- **Behavior:** Initial focus on CTA, then distraction, then re-acquisition of primary CTA
- **Expected A/B Impact:** Green button = instant re-acquisition, Yellow button = slow re-acquisition

## 🧪 **Test Scenarios**

### **A/B Test Scenarios (Button Color Impact)**
1. **Alex - Direct Purchase:** "I need to complete this purchase immediately."
2. **Alex - Urgent Completion:** "Finish this order right now."
3. **Dana - Initial Focus:** "I want to place my order."
4. **Dana - Distraction Recovery:** "Wait, what's this Apple TV offer? Let me check... Actually, just finish the order."

### **Control Scenarios (Should Perform Identically)**
1. **Brenda - Find Savings First:** "I want to check for any discount codes or gift cards before ordering."
2. **Brenda - Tax Exemption Check:** "Can I apply for tax exemption on this purchase?"
3. **Charles - Verify Order Details:** "I need to double-check my order details and pickup location."
4. **Charles - Read Terms:** "I want to read the terms and privacy policy before placing my order."

## 📊 **Key Metrics**

### **Primary A/B Test Metrics**
- **Processing Time:** Does button color affect AI decision speed?
- **Success Rate:** Does button color affect accuracy?
- **Confidence:** Does button color affect AI confidence?

### **Control Metrics**
- **Consistency:** Do control tests perform identically across variants?
- **Baseline:** Establish baseline performance for non-button elements

## 🚀 **How to Run the Test**

### **Prerequisites**
1. Python 3 with required packages installed
2. Google Gemini API key configured
3. Screenshots `a.png` and `b.png` (identical except button color)
4. Element JSON files for both variants

### **Running the Test**
```bash
python3 ab_testing_framework.py
```

### **Test Flow**
1. **Variant A Testing:** Tests current UI with all personas
2. **Variant B Testing:** Tests button color change with all personas
3. **Analysis:** Compares performance across variants
4. **Report Generation:** Creates detailed persona-based analysis

## 📈 **Expected Results**

### **Alex (Speed-Focused)**
- **Variant A:** Very fast processing, high success rate
- **Variant B:** Slower processing, potential success rate drop
- **Key Insight:** Button color significantly impacts speed-focused users

### **Brenda (Savings-Focused)**
- **Both Variants:** Similar performance (control scenario)
- **Key Insight:** Button color doesn't affect savings exploration

### **Charles (Cautious)**
- **Variant A:** Clear final step signal, moderate processing time
- **Variant B:** Potential anxiety, longer processing time
- **Key Insight:** Button color affects trust and verification behavior

### **Dana (Distracted)**
- **Variant A:** Fast re-acquisition after distraction
- **Variant B:** Slow re-acquisition, requires full page scan
- **Key Insight:** Button color critical for distracted users

## 🎯 **Scientific Value**

This framework provides:

1. **Persona-Specific Insights:** How different user types respond to UI changes
2. **Behavioral Validation:** Real-world user behavior patterns in AI agents
3. **Design Guidelines:** Evidence-based UI design for AI agent optimization
4. **Performance Metrics:** Quantifiable impact of visual design on AI performance

## 📋 **Report Output**

The framework generates a comprehensive report including:

- **Overall A/B Comparison:** Aggregate performance differences
- **Persona Analysis:** Individual persona performance breakdown
- **A/B Test Results:** Button color impact on specific scenarios
- **Control Validation:** Confirmation that non-button elements perform identically
- **Design Recommendations:** Actionable insights for UI optimization

## 🔬 **Research Applications**

This methodology can be extended to test:

- **Button Size Impact:** How button dimensions affect AI agent performance
- **Text Color Impact:** How text color affects readability and decision-making
- **Layout Changes:** How page layout affects AI agent navigation
- **Icon Usage:** How icons vs. text affect AI agent understanding
- **Animation Effects:** How motion affects AI agent attention and performance

## 💡 **Key Insights**

The persona-based approach reveals that **button color doesn't just affect visual appeal—it fundamentally changes how AI agents process and interact with UI elements**. Different personas respond differently to the same visual change, providing nuanced insights for AI-optimized design.

This framework represents a new paradigm in UI testing: **designing interfaces specifically for AI agent performance while maintaining human usability**. 