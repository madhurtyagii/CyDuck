from flask import Flask, render_template, request, jsonify
from agent import CyDuckAgent
import time

app = Flask(__name__)
agent = CyDuckAgent()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    user_id = request.json.get('user_id', 'web_user')
    
    # Simulate typing delay
    time.sleep(0.5)
    
    response = agent.generate_response(user_message, user_id)
    return jsonify({'response': response})

@app.route('/history', methods=['GET'])
def get_history():
    """Get chat history"""
    limit = request.args.get('limit', 10, type=int)
    history = agent.get_chat_history(limit)
    return jsonify({'history': history})

@app.route('/clear', methods=['POST'])
def clear_history():
    """Clear chat history"""
    message = agent.clear_history()
    return jsonify({'message': message})

if __name__ == '__main__':
    print("🦆 CyDuck Web App with MEMORY running at http://localhost:5000")
    app.run(debug=True, port=5000, host='0.0.0.0')
