from flask import Flask, render_template, request, jsonify
from agent import CyDuckAgent

app = Flask(__name__)
agent = CyDuckAgent()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = agent.generate_response(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    print("🦆 CyDuck Web App running at http://localhost:5000")
    app.run(debug=True, port=5000)
