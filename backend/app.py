from flask import Flask, request, jsonify, send_file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import sqlite3
import os

from config import SECRET_KEY, UPLOAD_FOLDER, DATABASE_PATH

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
jwt = JWTManager(app)

# Allow credentials and all origins
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize database and create tables
def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT NOT NULL,
                        role TEXT CHECK(role IN ('admin', 'user')) NOT NULL)''')

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO users VALUES (?, ?, ?)", [
            ("admin", "password123", "admin"),
            ("user1", "userpass", "user")
        ])
    
    conn.commit()
    conn.close()

init_db()

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and user[0] == password:
            access_token = create_access_token(identity={"username": username, "role": user[1]})
            return jsonify(access_token=access_token)

        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    try:
        current_user = get_jwt_identity()

        if 'file' not in request.files:
            return jsonify({"error": "No file part in request"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        filename = f"{current_user['username']}_{file.filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        return jsonify({"message": f"File uploaded successfully by {current_user['username']}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
@jwt_required()
def download_file(filename):
    current_user = get_jwt_identity()
    role = current_user["role"]
    username = current_user["username"]

    if role == "admin" or filename.startswith(username):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        return jsonify({"error": "File not found"}), 404

    return jsonify({"error": "Access denied"}), 403

if __name__ == '__main__':
    app.run(debug=True, port=5000)
