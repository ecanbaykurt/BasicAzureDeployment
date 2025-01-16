import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Azure OpenAI API Configuration
openai.api_type = "azure"
openai.api_base = "https://folky-ai-service.openai.azure.com/"  # Replace with your Azure OpenAI endpoint
openai.api_version = "2023-05-15"  # Use the correct API version for Azure
openai.api_key = "Eu9JVXSDcxL4F1R9rRNEeQMmHGBmRK0wwQjaOQUDvBlILow3jhb0JQQJ99BAACYeBjFXJ3w3AAABACOGVjMm"  # Replace with your API key

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
                engine="gpt-35-turbo-2",  # Replace with your Azure deployment name
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
            return jsonify({'reply': f"Error: {str(e)}"})
    return jsonify({'reply': "Sorry, I didn't understand that."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
