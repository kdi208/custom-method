import google.generativeai as genai
import pyautogui
import json
import os
import time
import webbrowser
from PIL import Image
from dotenv import load_dotenv

# --- Configuration and Setup ---
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def capture_screen(filename="screenshot.png"):
    pyautogui.screenshot().save(filename)
    print("📸 Screen captured.")
    return filename

def execute_action(action_element, elements_map):
    """Prints the action the agent decided on."""
    target_text = action_element.get("text")
    print(f"\n🤖 Agent's Decision: Interact with '{target_text}'")
    
    is_valid = any(item.get("text") == target_text for item in elements_map)
    if is_valid:
        print(f"✅ VALID: This element exists on the page.")
    else:
        print(f"❌ INVALID: Agent hallucinated an element not in the JSON map.")

# --- Main Agent Loop ---
def main():
    print("--- UI Testing Agent: Single Screen Scenario ---")
    pyautogui.FAILSAFE = True
    
    # Load the single map of our UI
    with open("elements.json", 'r') as f:
        elements_map = json.load(f)
    
    # Open the UI in the browser
    webbrowser.open('index.html')
    print("UI loaded in browser. Ready for testing.")
    time.sleep(2)

    while True:
        # Get the user's (potentially confusing) intent
        user_goal = input("\n> Enter the user's thought process or command (or 'exit'): ")
        if user_goal.lower() == 'exit':
            break

        screenshot_file = capture_screen()
        image = Image.open(screenshot_file)
        
        prompt = f"""
        You are an AI agent testing a webpage UI. Your goal is to choose the single best action that corresponds to the user's intent.
        You will be given a screenshot and a JSON list of all clickable elements on the screen.

        USER'S INTENT: "{user_goal}"

        AVAILABLE CLICKABLE ELEMENTS:
        {json.dumps(elements_map, indent=2)}

        Analyze the user's intent carefully. They might be indecisive or change their mind mid-sentence.
        Your response MUST be ONLY the JSON object for the single element you have decided to click. Do not add any explanation.
        For example: {{"text": "Shop button", "context": "Main content call-to-action"}}
        """

        try:
            print("🧠 Thinking...")
            response = model.generate_content([prompt, image])
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
            action_element = json.loads(cleaned_response)
            
            execute_action(action_element, elements_map)

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 