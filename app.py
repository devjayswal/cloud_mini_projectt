from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

# File path to store chat history
CHAT_HISTORY_FILE = 'chat_history.txt'

# Load existing chat history from file
try:
    with open(CHAT_HISTORY_FILE, 'r') as file:
        chat_history = eval(file.read())
except FileNotFoundError:
    chat_history = {}

@app.route('/')
def welcome():
    return "Welcome to the Chat Microservice"

@app.route("/send", methods=["POST"])
def send_message():
    """
    Send a message from one person to another.
    ---
    parameters:
       - name: sender
         in: formData
         type: string
         required: true
         description: The name of the sender
       - name: receiver
         in: formData
         type: string
         required: true
         description: The name of the receiver
       - name: message
         in: formData
         type: string
         required: true
         description: The message content
    responses:
        201:
            description: Message sent successfully
    """
    sender = request.form.get('sender')
    receiver = request.form.get('receiver')
    message = request.form.get('message')

    if sender not in chat_history:
        chat_history[sender] = {}
    if receiver not in chat_history[sender]:
        chat_history[sender][receiver] = []

    chat_history[sender][receiver].append({'sender': sender, 'receiver': receiver, 'message': message})

    # Save updated chat history to file
    with open(CHAT_HISTORY_FILE, 'w') as file:
        file.write(repr(chat_history))

    return "Message sent successfully", 201

@app.route('/chat/<sender>/<receiver>', methods=['GET'])
def get_chat_history(sender, receiver):
    """
    Fetch the chat history between two specified persons.
    ---
    parameters:
        - name: sender
          in: path
          type: string
          required: true
          description: The name of the sender
        - name: receiver
          in: path
          type: string
          required: true
          description: The name of the receiver
    responses:
        200:
            description: Chat history between two persons
    """
    if sender in chat_history and receiver in chat_history[sender]:
        return jsonify(chat_history[sender][receiver])
    else:
        return "No chat history found", 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
