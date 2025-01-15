import openai
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Load Azure OpenAI API Key and Endpoint from environment variables
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = "https://folky-ai-service.openai.azure.com/"
openai.api_type = "azure"
openai.api_version = "2023-05-15"  # Use the correct version for Azure OpenAI

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
            # Use Azure OpenAI ChatCompletion for conversation
            response = openai.ChatCompletion.create(
                engine="gpt-35-turbo",  # Replace with the correct deployment name of your model in Azure
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input},
                ],
                max_tokens=150,
                temperature=0.7
            )
            reply = response['choices'][0]['message']['content'].strip()
            return jsonify({'reply': reply})
        except Exception as e:
            return jsonify({'reply': f"Error: {str(e)}"})
    return jsonify({'reply': "Sorry, I didn't understand that."})
