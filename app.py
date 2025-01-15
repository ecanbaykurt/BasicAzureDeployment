import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Add your Azure OpenAI API Key and Endpoint
import os
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai_endpoint = "https://folky-ai-service.openai.azure.com/"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if user_input:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=150
        )
        reply = response.choices[0].text.strip()
        return jsonify({'reply': reply})
    return jsonify({'reply': "Sorry, I didn't understand that."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
