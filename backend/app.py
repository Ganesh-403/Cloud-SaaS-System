from flask import Flask, request, jsonify, send_file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'supersecretkey'
jwt = JWTManager(app)
CORS(app, supports_credentials=True)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
DB_PATH = "database/cloud_saas.db"

# Initialize database and create tables
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password TEXT NOT NULL,
                        role TEXT CHECK(role IN ('admin', 'user')) NOT NULL)''')
    
    # Check if users exist, otherwise insert default users
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

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and user[0] == password:
            # Remove 'subject' argument here
            access_token = create_access_token(
    identity={"username": username},
    additional_claims={"subject": username})

            return jsonify(access_token=access_token)

        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    print("UPLOAD route hit!")  # 👈 Add this line
    try:
        current_user = get_jwt_identity()

        # 🔍 Debug print
        print("request.files:", request.files)

        # Check if a file is included in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file part in request"}), 400

        file = request.files['file']
        
        # Ensure a valid file is selected
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Save the file with a unique name
        filename = f"{current_user['username']}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)
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

    # 🔍 Debugging logs
    print(f"Requested filename: {filename}")

    # Ensure admin can download all files, but users can only download their own
    if role == "admin" or filename.startswith(username):
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)

        print("File not found:", file_path)
        return jsonify({"error": "File not found"}), 404  # Return proper HTTP 404 status

    return jsonify({"error": "Access denied"}), 403


if __name__ == '__main__':
    app.run(debug=True, port=5000)
