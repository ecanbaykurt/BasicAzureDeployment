import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Add your OpenAI API Key
openai.api_key = "OPENAI_API_KEY"  # Replace with your OpenAI API key

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
            # Call OpenAI GPT model
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use 'gpt-4' if available
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
