#!/usr/bin/env python3
"""
Complete Computer Use Script with Agent Loop
This script implements the full computer use functionality including:
- Taking screenshots
- Mouse clicks and movements
- Keyboard input
- Agent loop to continue conversation with Claude
"""

import anthropic
import base64
import json
import time
import subprocess
import os
from PIL import Image, ImageGrab
import pyautogui
import io

class ComputerUseAgent:
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.messages = []
        
        # Configure pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
    def take_screenshot(self):
        """Take a screenshot and return as base64 encoded string"""
        try:
            # Take screenshot using PIL
            screenshot = ImageGrab.grab()
            
            # Convert to bytes
            img_buffer = io.BytesIO()
            screenshot.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            # Encode as base64
            img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
            
            return img_base64
        except Exception as e:
            return f"Error taking screenshot: {str(e)}"
    
    def execute_action(self, action_type, params):
        """Execute a computer action based on Claude's request"""
        try:
            if action_type == "screenshot":
                screenshot_b64 = self.take_screenshot()
                return {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": screenshot_b64
                    }
                }
            
            elif action_type == "left_click":
                x, y = params["coordinate"]
                pyautogui.click(x, y)
                return f"Clicked at coordinates ({x}, {y})"
            
            elif action_type == "right_click":
                x, y = params["coordinate"]
                pyautogui.rightClick(x, y)
                return f"Right-clicked at coordinates ({x}, {y})"
            
            elif action_type == "double_click":
                x, y = params["coordinate"]
                pyautogui.doubleClick(x, y)
                return f"Double-clicked at coordinates ({x}, {y})"
            
            elif action_type == "type":
                text = params["text"]
                pyautogui.typewrite(text)
                return f"Typed: {text}"
            
            elif action_type == "key":
                key = params["key"]
                pyautogui.press(key)
                return f"Pressed key: {key}"
            
            elif action_type == "scroll":
                x, y = params["coordinate"]
                clicks = params.get("clicks", 3)
                pyautogui.scroll(clicks, x=x, y=y)
                return f"Scrolled {clicks} clicks at ({x}, {y})"
            
            else:
                return f"Unknown action type: {action_type}"
                
        except Exception as e:
            return f"Error executing {action_type}: {str(e)}"
    
    def run_task(self, task_description):
        """Run a computer use task with Claude"""
        print(f"Starting task: {task_description}")
        print("-" * 50)
        
        # Initial message
        self.messages = [
            {
                "role": "user",
                "content": task_description
            }
        ]
        
        max_iterations = 20  # Prevent infinite loops
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            print(f"\n--- Iteration {iteration} ---")
            
            # Send message to Claude
            try:
                response = self.client.beta.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1024,
                    tools=[
                        {
                            "type": "computer_20250124",
                            "name": "computer",
                            "display_width_px": 1920,
                            "display_height_px": 1080,
                            "display_number": 1,
                        }
                    ],
                    messages=self.messages,
                    betas=["computer-use-2025-01-24"]
                )
                
                print(f"Claude's response: {response.content}")
                
                # Check if Claude wants to use a tool
                if response.stop_reason == "tool_use":
                    # Find the tool use block
                    tool_use = None
                    for content in response.content:
                        if content.type == "tool_use":
                            tool_use = content
                            break
                    
                    if tool_use:
                        print(f"Claude wants to use tool: {tool_use.name}")
                        print(f"Tool input: {tool_use.input}")
                        
                        # Execute the action
                        action = tool_use.input.get("action")
                        if action:
                            result = self.execute_action(action, tool_use.input)
                            print(f"Action result: {result}")
                            
                            # Add Claude's response to messages
                            self.messages.append({
                                "role": "assistant",
                                "content": response.content
                            })
                            
                            # Add tool result to messages
                            if isinstance(result, dict) and result.get("type") == "image":
                                # Handle image result (screenshot)
                                self.messages.append({
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
                                # Handle text result
                                self.messages.append({
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
                            print("No action specified in tool use")
                            break
                    else:
                        print("No tool use found in response")
                        break
                        
                else:
                    # Claude finished the task
                    print("Claude finished the task!")
                    print(f"Final response: {response.content}")
                    break
                    
            except Exception as e:
                print(f"Error in iteration {iteration}: {str(e)}")
                break
                
            # Small delay between iterations
            time.sleep(1)
        
        if iteration >= max_iterations:
            print("Reached maximum iterations. Task may not be complete.")
        
        print("\n" + "=" * 50)
        print("Task completed!")

def main():
    # Check if required packages are installed
    try:
        import pyautogui
        from PIL import Image, ImageGrab
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call(["pip", "install", "pyautogui", "pillow"])
        import pyautogui
        from PIL import Image, ImageGrab
    
    # Create agent
    agent = ComputerUseAgent()
    
    # Task description
    task = """
    Open https://speaker-checkout-dinoilievski1.replit.app and fill out the checkout form with test data.
    
    Use the following test data for Chloe Thompson (a 27-year-old freelance content writer from Portland):
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
    
    Please complete the entire checkout process step by step.
    """
    
    # Run the task
    agent.run_task(task)

if __name__ == "__main__":
    main() 