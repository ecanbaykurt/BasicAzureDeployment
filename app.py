import openai
from flask import Flask, render_template, request, jsonify
import os

# Load environment variables (optional for local testing with .env)
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Azure OpenAI API Configuration
openai.api_type = "azure"
openai.api_base = "https://folky-ai-service.openai.azure.com/"  # Replace with your Azure OpenAI endpoint
openai.api_version = "2023-05-15"  # Use the correct API version for Azure
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")  # Fetch the key from environment variables

# Ensure the API key is set
if not openai.api_key:
    raise ValueError("API key for Azure OpenAI is not set. Please set the 'AZURE_OPENAI_API_KEY' environment variable.")

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chatbot interactions."""
    user_input = request.json.get('message')
    if user_input:
        try:
            # Call Azure OpenAI ChatCompletion API
            response = openai.ChatCompletion.create(
                engine="gpt-35-turbo",  # Replace with your Azure deployment name
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input},
                ],
                max_tokens=150,
                temperature=0.7
            )
            # Extract the assistant's reply
            reply = response['choices'][0]['message']['content'].strip()
            return jsonify({'reply': reply})
        except Exception as e:
            # Log detailed error for debugging and show a user-friendly message
            print(f"Error calling Azure OpenAI API: {e}")
            return jsonify({'reply': "Sorry, there was an issue connecting to the AI service. Please try again later."})
    return jsonify({'reply': "Sorry, I didn't understand that."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
