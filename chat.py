from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For session management

messages = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_name', methods=['POST'])
def set_name():
    name = request.form.get('name')
    if not name:
        return redirect(url_for('index'))
    session['name'] = name
    return redirect(url_for('chatroom'))

@app.route('/chatroom', methods=['GET', 'POST'])
def chatroom():
    if 'name' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        message_text = request.form.get('message')
        if message_text:
            message = {
                'sender': session['name'],
                'text': message_text,
                'time': datetime.now().strftime('[%B-%d, %H:%M:%S %p]')
            }
            messages.append(message)

    return render_template('chatroom.html', messages=messages)

@app.route('/get_messages')
def get_messages():
    return jsonify(messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=404,debug=True, threaded=True)