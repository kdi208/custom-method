import google.generativeai as genai
import pyautogui
import json
import os
import time
import webbrowser
from PIL import Image
from dotenv import load_dotenv

# --- Configuration and Setup ---

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("API key not found. Please set GOOGLE_API_KEY in your .env file.")

# Configure the generative AI model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# --- Helper Functions ---

def load_elements_map(filename="elements.json"):
    """Loads the interactive elements map from a JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def capture_screen(filename="screenshot.png"):
    """Captures the entire screen and saves it to a file."""
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print("📸 Screen captured.")
    return filename

def get_element_center(box_2d):
    """Calculates the center of a bounding box."""
    x1, y1, x2, y2 = box_2d
    return (x1 + x2) // 2, (y1 + y2) // 2

def execute_click(element, elements_map):
    """Finds an element by its text and clicks its center."""
    target_text = element.get("text")
    print(f"🤖 Action selected: Click on '{target_text}'")
    
    # Find the full element details from our map
    for item in elements_map:
        if item.get("text") == target_text:
            # IMPORTANT: The JSON you created has text, not coordinates.
            # In a real scenario, you'd use the box_2d coordinates directly.
            # For this test, we'll just print that we would have clicked.
            # To make it actually click, you would need to populate the JSON
            # with the real coordinates from the screenshot.
            
            # box = item['box_2d']
            # center_x, center_y = get_element_center(box)
            # pyautogui.moveTo(center_x, center_y, duration=0.5)
            # pyautogui.click()
            
            print(f"✅ SUCCESS: Would have clicked on '{target_text}'. (Actual clicking is disabled for safety).")
            return
            
    print(f"❌ ERROR: Element '{target_text}' not found in the JSON map.")


# --- Main Agent Loop ---

def main():
    print("--- Local AI Agent Test ---")
    
    # Set a failsafe: moving mouse to the top-left corner will stop the script.
    pyautogui.FAILSAFE = True
    
    elements_map = load_elements_map()
    
    # Open the local webpage in the default browser
    webbrowser.open('index.html')
    time.sleep(2) # Give the browser time to open

    while True:
        user_goal = input("\n> What should I do next? (or type 'exit' to quit): ")
        if user_goal.lower() == 'exit':
            break

        screenshot_file = capture_screen()
        image = Image.open(screenshot_file)

        # The prompt for the LLM
        prompt = f"""
        You are a helpful AI assistant that operates a web browser.
        You will be given a user's goal and a screenshot of the current page.
        You also have a JSON file listing the interactive elements available.

        USER GOAL: "{user_goal}"

        JSON OF INTERACTIVE ELEMENTS:
        {json.dumps(elements_map, indent=2)}

        Based on the user's goal, the screenshot, and the JSON, decide which single element to click.
        Your response MUST be ONLY the JSON object for that element, and nothing else.
        For example: {{"box_2d": [221, 507, 244, 560], "text": "Shop button", "element_type": "button"}}
        """

        try:
            print("🧠 Thinking...")
            response = model.generate_content([prompt, image])
            
            # Clean up the response to make sure it's valid JSON
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
            action_element = json.loads(cleaned_response)
            
            execute_click(action_element, elements_map)

        except Exception as e:
            print(f"An error occurred: {e}")
            print("Could not determine the action. Please try another command.")

if __name__ == "__main__":
    main() 