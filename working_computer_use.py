#!/usr/bin/env python3
"""
Working Computer Use Script for Mac
This script actually opens a browser and performs actions based on Claude's instructions.
"""

import google.generativeai as genai
import base64
import json
import time
import subprocess
import os
import webbrowser
from PIL import Image, ImageGrab, ImageTk
import pyautogui
import io
import tkinter

class MacComputerUse:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Configure pyautogui for Mac
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 1.0  # Slower pace for Mac
        
    def take_screenshot(self):
        """Take a screenshot and return as base64"""
        try:
            screenshot = ImageGrab.grab()
            img_buffer = io.BytesIO()
            screenshot.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
            return img_base64
        except Exception as e:
            print(f"Screenshot error: {e}")
            return None
    
    def open_browser_to_url(self, url):
        """Open browser to specific URL"""
        try:
            webbrowser.open(url)
            time.sleep(3)  # Wait for browser to open
            return f"Opened browser to {url}"
        except Exception as e:
            return f"Error opening browser: {e}"
    
    def execute_computer_action(self, action_data):
        """Execute computer actions based on Claude's instructions"""
        action = action_data.get("action")
        
        try:
            if action == "screenshot":
                # This action is handled separately in the main loop to send the image to Gemini
                return "Taking a screenshot."
            
            elif action == "left_click":
                coordinate = action_data.get("coordinate", [0, 0])
                x, y = coordinate
                pyautogui.click(x, y)
                return f"Clicked at ({x}, {y})"
            
            elif action == "type":
                text = action_data.get("text", "")
                pyautogui.typewrite(text, interval=0.1)
                return f"Typed: {text}"
            
            elif action == "key":
                key = action_data.get("key", "")
                if key:
                    pyautogui.press(key)
                    return f"Pressed key: {key}"
                
            elif action == "scroll":
                coordinate = action_data.get("coordinate", [640, 400])
                clicks = action_data.get("clicks", 3)
                x, y = coordinate
                pyautogui.scroll(clicks, x=x, y=y)
                return f"Scrolled {clicks} at ({x}, {y})"
            
            else:
                return f"Unknown action: {action}"
                
        except Exception as e:
            return f"Error executing {action}: {e}"
    
    def run_checkout_task(self):
        """Run the specific checkout task"""
        print("🚀 Starting checkout automation from a local image...")
        print("-" * 50)
        
        # Step 1: Load the initial image from a local file
        image_path = "amazon_cart.png"
        print(f"Loading initial image from: {image_path}")
        try:
            initial_image = Image.open(image_path)
        except FileNotFoundError:
            print(f"❌ Error: The image file was not found at '{image_path}'")
            print("Please ensure the screenshot is in the same directory as the script and named correctly.")
            return

        # Create a Tkinter window to display the image
        root = tkinter.Tk()
        root.title("Checkout Simulation")
        image_width, image_height = initial_image.size
        root.geometry(f"{image_width}x{image_height}+0+0")
        root.resizable(False, False)
        
        tk_image = ImageTk.PhotoImage(initial_image)
        image_label = tkinter.Label(root, image=tk_image, bd=0)
        image_label.pack()
        root.update()

        # Define tools for Gemini based on available computer actions
        tools = [
            {"name": "screenshot", "description": "Take a screenshot of the current screen.", "parameters": {"type": "OBJECT", "properties": {}}},
            {"name": "left_click", "description": "Perform a left mouse click at a specified coordinate.", "parameters": {"type": "OBJECT", "properties": {"coordinate": {"type": "ARRAY", "description": "The [x, y] coordinate to click.", "items": {"type": "INTEGER"}}}, "required": ["coordinate"]}},
            {"name": "type", "description": "Type text using the keyboard.", "parameters": {"type": "OBJECT", "properties": {"text": {"type": "STRING", "description": "The text to type."}}, "required": ["text"]}},
            {"name": "key", "description": "Press a special key.", "parameters": {"type": "OBJECT", "properties": {"key": {"type": "STRING", "description": "The key to press (e.g., 'enter', 'tab')."}}, "required": ["key"]}},
            {"name": "scroll", "description": "Scroll the window.", "parameters": {"type": "OBJECT", "properties": {"coordinate": {"type": "ARRAY", "description": "The [x, y] coordinate to scroll at.", "items": {"type": "INTEGER"}}, "clicks": {"type": "INTEGER", "description": "Number of scroll clicks."}}, "required": ["coordinate", "clicks"]}},
        ]
        
        # Initial prompt for Gemini
        initial_prompt = "This is a screenshot of my Amazon shopping cart. Your goal is to complete the checkout. First, click on the 'Proceed to checkout' button."

        messages = [{'role': 'user', 'parts': [initial_prompt, initial_image]}]
        
        max_steps = 15
        step = 0
        
        while step < max_steps:
            step += 1
            print(f"\n--- Step {step} ---")
            
            try:
                # Send current conversation to Gemini
                response = self.model.generate_content(messages, tools=tools)
                response_part = response.candidates[0].content.parts[0]
                
                if response_part.text:
                    print(f"Gemini says: {response_part.text}")

                # Check if Gemini wants to use a tool
                if hasattr(response_part, 'function_call') and response_part.function_call:
                    tool_call = response_part.function_call
                    action = tool_call.name
                    args = {key: value for key, value in tool_call.args.items()}
                    action_data = {'action': action, **args}
                    
                    print(f"Executing: {action} with args {args}")

                    messages.append({'role': 'model', 'parts': response.candidates[0].content.parts})
                    
                    if action == 'screenshot':
                        screenshot_b64 = self.take_screenshot()
                        if screenshot_b64:
                            print("Result: Took a screenshot.")
                            image_part = {"inline_data": {"mime_type": "image/png", "data": screenshot_b64}}
                            messages.append({'role': 'user', 'parts': [image_part, "Here is the screenshot you requested. What's the next step?"]})
                        else:
                            print("Error: Failed to take screenshot.")
                            messages.append({'role': 'user', 'parts': [{"text": "I failed to take the screenshot. Please try again."}]})
                    else:
                        result = self.execute_computer_action(action_data)
                        print(f"Result: {result}")
                        messages.append({
                            'role': 'tool',
                            'parts': [{
                                "function_response": {
                                    "name": action,
                                    "response": {
                                        "result": str(result)
                                    },
                                }
                            }]
                        })
                else:
                    # Gemini finished
                    print("✅ Gemini finished the task!")
                    break
                    
            except Exception as e:
                import traceback
                print(f"❌ Error in step {step}:")
                print(f"    Type: {type(e).__name__}")
                print(f"    Message: {e}")
                traceback.print_exc()
                break
                
            time.sleep(2)  # Brief pause between actions
            root.update_idletasks()
            root.update()
        
        print("\n🎉 Checkout automation completed!")
        root.destroy()

def main():
    print("🖥️  Mac Computer Use - Checkout Form Automation")
    print("=" * 60)
    
    # Check if we're on Mac
    if os.uname().sysname != "Darwin":
        print("❌ This script is designed for Mac only!")
        return
    
    agent = MacComputerUse()
    agent.run_checkout_task()

if __name__ == "__main__":
    main() 