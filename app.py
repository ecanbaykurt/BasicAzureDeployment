import openai
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Azure OpenAI API Key and Endpoint
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")  # Set your Azure OpenAI API key as an environment variable
openai.api_base = "https://folky-ai-service.openai.azure.com/"  # Replace with your Azure OpenAI Endpoint
openai.api_type = "azure"
openai.api_version = "2023-05-15"  # Use the correct API version for Azure OpenAI

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
            reply = response['choices'][0]['message']['content'].strip()
            return jsonify({'reply': reply})
        except Exception as e:
            return jsonify({'reply': f"Error: {str(e)}"})
    return jsonify({'reply': "Sorry, I didn't understand that."})

if __name__ == "__main__":
    # Run the Flask app
    app.run(host='0.0.0.0', port=8080)
