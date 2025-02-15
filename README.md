# Cloud-Based SaaS System

## Overview
This project is a cloud-based SaaS (Software as a Service) system that allows users to upload, download, and manage files securely. It includes authentication, role-based access control, and a user-friendly frontend built with React.

## Features
- User authentication with JWT (JSON Web Token)
- Role-based access control (Admin & User)
- Secure file upload and download functionality
- Frontend built using React.js
- Backend developed with Flask and SQLite
- API endpoints protected with authentication
- CORS enabled for frontend-backend communication

## Technologies Used
### Frontend:
- React.js
- Axios (for API requests)
- Bootstrap (optional for UI styling)

### Backend:
- Flask (Python)
- Flask-JWT-Extended (Authentication)
- Flask-CORS (Cross-Origin Resource Sharing)
- SQLite (Database for user management)

## Setup Instructions

### Prerequisites:
- Install **Node.js** and **npm** for the frontend
- Install **Python 3** and **pip** for the backend

### Backend Setup:
1. Navigate to the backend directory:
   ```
   cd backend
   ```

### Backend Setup:

1. Navigate to the backend directory:
   ```
   cd backend
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```
   python app.py
   ```

### Frontend Setup:

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```
2. Install dependencies:
   ```
   npm install
   ```
3. Start the React application:
   ```
   npm start
   ```

## API Endpoints

### Authentication
- `POST /login` - User login to get a JWT token

### File Management
- `POST /upload` - Upload a file (requires authentication)
- `GET /download/<filename>` - Download a file (requires authentication)

## Usage Instructions

1. Start the backend and frontend servers.
2. Log in using an existing user (e.g., `admin` with `password123`).
3. Use the UI to upload and download files.
4. Ensure the authentication token is included in API requests.

## Future Enhancements

- Implement user registration and password hashing
- Support additional file storage solutions (AWS S3, Google Drive)
- Improve UI with better styling and error handling
- Add database migrations for better scalability

## License

This project is open-source and available for personal and educational use.

