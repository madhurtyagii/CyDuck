from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from agent import agent
import sqlite3
import traceback
import uuid
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/conversations', methods=['GET'])
def get_conversations():
    """List all chat sessions"""
    try:
        with sqlite3.connect(agent.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, created_at FROM sessions ORDER BY created_at DESC')
            rows = cursor.fetchall()
            return jsonify([dict(row) for row in rows])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/conversation/<session_id>', methods=['GET'])
def get_messages(session_id):
    """Get messages for a specific session"""
    try:
        messages = agent.get_messages(session_id)
        return jsonify(messages)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/conversation/new', methods=['POST'])
def new_conversation():
    """Create a new chat session"""
    try:
        session_id = str(uuid.uuid4())
        agent.ensure_session(session_id, "New Chat")
        return jsonify({'session_id': session_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/conversation/<session_id>', methods=['PUT'])
def rename_conversation(session_id):
    """Rename a chat session"""
    try:
        data = request.get_json()
        new_title = data.get('title')
        if not new_title:
            return jsonify({'error': 'Title required'}), 400
            
        with sqlite3.connect(agent.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE sessions SET title = ? WHERE id = ?', (new_title, session_id))
            conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/conversation/<session_id>', methods=['DELETE'])
def delete_conversation(session_id):
    """Delete a chat session"""
    try:
        with sqlite3.connect(agent.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
            # Messages delete automatically due to CASCADE
            conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """Stream chat response using SSE"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        def generate():
            for chunk in agent.chat_stream(user_message, session_id):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
        
        return Response(stream_with_context(generate()), mimetype='text/event-stream')
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/clear', methods=['POST'])
def clear():
    """Wipe all sessions (for developer/maintenance)"""
    try:
        with sqlite3.connect(agent.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM sessions')
            conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
