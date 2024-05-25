import openai
import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY')

# Ensure uploaded documents are not used to train OpenAI models
headers = {
    'Authorization': f'Bearer {openai.api_key}',
    'OpenAI-User': 'openai',
    'OpenAI-User-Purpose': 'none'
}

def ask_openai(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can choose another model if you prefer
        prompt=prompt,
        max_tokens=150,
        headers=headers
    )
    return response.choices[0].text.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "Please provide a message"}), 400

    response = ask_openai(user_input)
    return jsonify({"response": response})

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads', filename)
        file.save(file_path)
        with open(file_path, 'r') as f:
            content = f.read()
        return jsonify({"message": f"File '{filename}' uploaded successfully"}), 200

    return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
