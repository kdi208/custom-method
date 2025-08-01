The "Emotional Fingerprint" Engine
We will create a new, post-processing module that runs after a test session is complete. For each step in the session log, it will take the agent's raw REASONING string and send it to a specialized LLM prompt to get a structured emotional analysis.
1. The New Architectural Step: Post-Session Analysis
The run_session method completes as normal, generating a detailed JSON log file with the raw REASONING text for each step.
After the session is saved, a new method, _analyze_session_emotions(session_log), is called.
This method iterates through each step in the log, takes the REASONING text, and sends it to our new "Sentiment Analysis" prompt.
It then saves these structured emotional scores back into the session log file as a new key, emotional_analysis.
2. The "Sentiment & Emotion Analysis" Prompt
This is a specialized prompt designed to force a structured, multi-dimensional JSON output.
The Prompt Template:
You are an expert Behavioral Psychologist. Your task is to analyze the following internal monologue from a user who is testing a software interface. Read the text carefully and provide a quantitative analysis of their emotional and cognitive state.
INTERNAL MONOLOGUE:
"{reasoning_text_goes_here}"
Based on this text, provide your analysis in the following JSON format. Rate each dimension on a scale of 1 (very low) to 10 (very high). Provide a brief justification.
Generated json
{
  "sentiment_score": "[A single float from -1.0 (very negative) to 1.0 (very positive)]",
  "sentiment_label": "['Positive', 'Negative', 'Neutral', or 'Mixed']",
  "dominant_emotion": "[The single most prominent emotion, e.g., 'Frustration', 'Confidence', 'Confusion', 'Curiosity']",
  "emotional_dimensions": {
    "confidence": "[1-10, How certain and secure does the user feel?]",
    "frustration": "[1-10, How annoyed or blocked does the user feel?]",
    "curiosity": "[1-10, How intrigued or interested is the user? Does the UI attract them?]",
    "confusion": "[1-10, How lost or uncertain is the user? This measures cognitive load.]"
  },
  "justification": "[A brief, one-sentence explanation for your scores.]"
}
Use code with caution.
Json
3. The Quantifiable Output
This prompt gives us exactly what you asked for: a structured, quantifiable rating of the user's internal state.
Example Input (Reasoning Text):
"As a new user, I don't know what this abstract icon means. I am looking for the word 'Create' or 'New'. I can't find a clear path forward and I am feeling frustrated."
Example Output (The Structured Analysis):
Generated json
{
  "sentiment_score": -0.8,
  "sentiment_label": "Negative",
  "dominant_emotion": "Confusion",
  "emotional_dimensions": {
    "confidence": 1,
    "frustration": 8,
    "curiosity": 2,
    "confusion": 9
  },
  "justification": "The user explicitly states they are frustrated and cannot find their path, indicating extremely high confusion and low confidence."
}```

#### **4. How We Integrate This into the MVP Report**

This is the crucial step. We don't want to add a dozen new charts and clutter our clean "Single-Page Strategic Memo." Instead, we will use this data to **enhance the existing "Voice of the User" section**, making it even more powerful.

**The New "Insight Card" in the Results Dashboard:**

The right panel of our report will now contain cards with three layers of insight, creating an irrefutable "pyramid of proof."

> **Theme: Workflow Interruption & Frustration**
>
> **Emotional Fingerprint:**
> `Confidence:  [▇□□□□□□□□□] 1/10`
> `Frustration: [▇▇▇▇▇▇▇▇□□] 8/10`
> `Confusion:   [▇▇▇▇▇▇▇▇▇□] 9/10`
>
> **"Voice of the User" Quote (Power User):**
> *"My entire workflow relies on that button being in the top-left. This change is unnecessary and slows me down. It is frustrating, and it breaks my muscle memory."*

This is a game-changer for the demo. The founder can now say:

> "And we don't just have to take the agent's word for it. Our engine analyzes the emotional content of the agent's thoughts at every step. As you can see from the **Emotional Fingerprint** for this interaction, the user's confidence plummeted to a 1 out of 10, while their frustration and confusion shot up to an 8 and 9. This isn't just a bad design; it's a design that is actively causing a negative emotional reaction in your expert users."

This is how we do it. We integrate this advanced analysis as a **layer of evidence** that makes our existing qualitative insights even more credible and impactful, without sacrificing the elegant simplicity of our MVP report.
Use code with caution.
Json