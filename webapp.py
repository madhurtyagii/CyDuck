from flask import Flask, render_template, request, jsonify
from agent import agent

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Get response from agent
    response = agent.chat(user_message)  # <-- FIXED THIS LINE
    
    return jsonify({'response': response})

@app.route('/clear', methods=['POST'])
def clear():
    agent.clear_memory()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
