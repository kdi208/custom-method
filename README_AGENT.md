# Local AI Agent Test Environment

This project demonstrates how to create a local AI agent that can understand visual interfaces and interact with them using multimodal AI capabilities.

## 🎯 What This Does

The AI agent can:
- Take screenshots of your screen
- Analyze the visual content using Google's Gemini AI
- Understand user commands in natural language
- Decide which UI elements to interact with
- Simulate mouse clicks (safety mode enabled)

## 📋 Prerequisites

1. **Python 3.7+** installed on your system
2. **Google AI API Key** (free from [Google AI Studio](https://aistudio.google.com/))

## 🚀 Quick Setup

### Option 1: Automated Setup
```bash
python setup.py
```

### Option 2: Manual Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get Your API Key:**
   - Go to [Google AI Studio](https://aistudio.google.com/)
   - Click "Get API key" and create one (it's free)
   - Copy your API key

3. **Configure Environment:**
   - Edit the `.env` file
   - Replace `PASTE_YOUR_API_KEY_HERE` with your actual API key

## 🎮 How to Use

1. **Run the Agent:**
   ```bash
   python agent.py
   ```

2. **Watch the Magic:**
   - The script will open `index.html` in your browser
   - It will display the Amazon cart screenshot
   - The agent will ask for your command

3. **Try These Commands:**
   - `"I want to buy some soap"`
   - `"Tell me more about the company"`
   - `"Show me the products"`
   - `"I want to sign in"`

4. **Safety Features:**
   - Mouse clicking is disabled by default (safety mode)
   - Move your mouse to the top-left corner to stop the script
   - The agent will tell you what it would have clicked

## 📁 Project Structure

```
test/
├── agent.py              # Main AI agent script
├── index.html            # Webpage that displays the screenshot
├── elements.json         # Map of interactive elements
├── amazon_cart.png       # Screenshot for testing
├── .env                  # Your API key (create this)
├── requirements.txt      # Python dependencies
├── setup.py             # Automated setup script
└── README_AGENT.md      # This file
```

## 🔧 Customization

### Adding Real Clicking
To enable actual mouse clicking, uncomment these lines in `agent.py`:

```python
# box = item['box_2d']
# center_x, center_y = get_element_center(box)
# pyautogui.moveTo(center_x, center_y, duration=0.5)
# pyautogui.click()
```

### Using Your Own Screenshot
1. Replace `amazon_cart.png` with your own screenshot
2. Update `elements.json` with the correct element coordinates
3. Update `index.html` to reference your new image

### Updating Element Map
The `elements.json` file contains:
- `box_2d`: [x1, y1, x2, y2] coordinates of the element
- `text`: Human-readable description
- `element_type`: Type of element (button, link, etc.)

## 🛠️ Troubleshooting

### "API key not found"
- Make sure your `.env` file exists
- Ensure your API key is correctly set in the `.env` file
- Check that there are no extra spaces or quotes

### "Module not found" errors
- Run `pip install -r requirements.txt`
- Make sure you're using Python 3.7+

### Browser doesn't open
- Check that your default browser is properly configured
- Try opening `index.html` manually in your browser

### Agent can't find elements
- The current `elements.json` is a demo with placeholder coordinates
- For real use, you need to map actual screen coordinates
- Use tools like browser dev tools to find real element positions

## 🔒 Safety Notes

- **Mouse Control**: By default, the agent won't actually click (safety mode)
- **Failsafe**: Move mouse to top-left corner to stop the script
- **API Usage**: Google AI API has usage limits, but generous free tier
- **Screenshots**: The agent captures your entire screen - be mindful of sensitive content

## 🎓 Learning More

This is a simplified version of how real AI agents work. In production systems:
- Element detection is more sophisticated
- Coordinates are dynamically calculated
- Multiple actions can be chained together
- Error handling is more robust
- Security measures are more comprehensive

## 📞 Support

If you run into issues:
1. Check the troubleshooting section above
2. Verify your API key is working
3. Make sure all dependencies are installed
4. Try the setup script: `python setup.py`

Happy testing! 🤖✨ 