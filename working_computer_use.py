#!/usr/bin/env python3
"""
Working Computer Use Script for Mac
This script actually opens a browser and performs actions based on Claude's instructions.
"""

import anthropic
import base64
import json
import time
import subprocess
import os
import webbrowser
from PIL import Image, ImageGrab
import pyautogui
import io

class MacComputerUse:
    def __init__(self):
        self.client = anthropic.Anthropic()
        
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
                screenshot_b64 = self.take_screenshot()
                if screenshot_b64:
                    return {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png", 
                            "data": screenshot_b64
                        }
                    }
                else:
                    return "Failed to take screenshot"
            
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
        print("🚀 Starting checkout automation...")
        print("-" * 50)
        
        # Step 1: Open the browser to the checkout page
        url = "https://speaker-checkout-dinoilievski1.replit.app"
        print(f"Opening browser to: {url}")
        self.open_browser_to_url(url)
        
        # Step 2: Take initial screenshot and start conversation with Claude
        messages = [
            {
                "role": "user",
                "content": """I've opened the browser to https://speaker-checkout-dinoilievski1.replit.app 

Please help me fill out the checkout form with this test data for Chloe Thompson:
- Name: Chloe Thompson  
- Email: chloe.thompson@creativecontent.com
- Address: 1234 Bohemian Lane
- City: Portland
- State: Oregon
- ZIP: 97201
- Country: United States
- Credit Card: 4111111111111111 (test card)
- Cardholder Name: Chloe Thompson
- Expiry: 12/25
- CVV: 123

First, please take a screenshot to see the current state of the page."""
            }
        ]
        
        max_steps = 15
        step = 0
        
        while step < max_steps:
            step += 1
            print(f"\n--- Step {step} ---")
            
            try:
                # Send current conversation to Claude
                response = self.client.beta.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1024,
                    tools=[
                        {
                            "type": "computer_20250124",
                            "name": "computer", 
                            "display_width_px": 1440,
                            "display_height_px": 900,
                            "display_number": 1,
                        }
                    ],
                    messages=messages,
                    betas=["computer-use-2025-01-24"]
                )
                
                print(f"Claude says: {[c.text for c in response.content if hasattr(c, 'text')]}")
                
                # Check if Claude wants to use a tool
                tool_use = None
                for content in response.content:
                    if hasattr(content, 'type') and content.type == "tool_use":
                        tool_use = content
                        break
                
                if tool_use:
                    print(f"Executing: {tool_use.input}")
                    
                    # Execute the computer action
                    result = self.execute_computer_action(tool_use.input)
                    print(f"Result: {type(result)}")
                    
                    # Add Claude's response to conversation
                    messages.append({
                        "role": "assistant", 
                        "content": response.content
                    })
                    
                    # Add tool result back to conversation
                    if isinstance(result, dict) and result.get("type") == "image":
                        # Screenshot result
                        messages.append({
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_use.id,
                                    "content": [result]
                                }
                            ]
                        })
                    else:
                        # Text result
                        messages.append({
                            "role": "user", 
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_use.id,
                                    "content": str(result)
                                }
                            ]
                        })
                else:
                    # Claude finished
                    print("✅ Claude finished the task!")
                    break
                    
            except Exception as e:
                print(f"❌ Error in step {step}: {e}")
                break
                
            time.sleep(2)  # Brief pause between actions
        
        print("\n🎉 Checkout automation completed!")

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