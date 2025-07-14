import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-20250514",  # Claude Sonnet 4
    max_tokens=1024,
    tools=[
        {
            "type": "computer_20250124",  # Correct tool type for Claude Sonnet 4
            "name": "computer",
            "display_width_px": 1280,
            "display_height_px": 800,
            "display_number": 1,
        }
    ],
    messages=[
        {
            "role": "user",
            "content": "Open https://speaker-checkout-dinoilievski1.replit.app and fill out the checkout form with test data."
        }
    ],
    betas=["computer-use-2025-01-24"]  # Required for Claude Sonnet 4
)

print(response) 