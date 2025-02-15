import React, { useState } from "react";
import axios from "axios";

function App() {
  const [token, setToken] = useState("");
  const [file, setFile] = useState(null);
  const [filename, setFilename] = useState("");

  const API_BASE_URL = "http://localhost:5000";  // Changed from 127.0.0.1

  console.log("App component is rendering...");

  const login = async () => {
    try {
      const res = await axios.post(`${API_BASE_URL}/login`, {
        username: "admin",
        password: "password123",
      });
      setToken(res.data.access_token);
      console.log("Token received:", res.data.access_token);
    } catch (error) {
      console.error("Login error:", error.response ? error.response.data : error.message);
      alert("Login failed! Check console for details.");
    }
  };

  const uploadFile = async () => {
    if (!file) {
      alert("Please select a file before uploading.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    console.log("Uploading file:", file.name);
    console.log("Token being sent:", token);

    try {
      const res = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${token}`,
        },
      });
      console.log("Upload response:", res.data);
      alert("File uploaded successfully!");
    } catch (error) {
      console.error("Upload Error:", error.response ? error.response.data : error.message);
      alert("File upload failed! Check console for details.");
    }
  };

  const downloadFile = async () => {
    if (!filename) {
      alert("Please enter a filename to download.");
      return;
    }
    if (!token) {
      alert("You must log in first!");
      return;
    }
  
    try {
      const res = await axios.get(`http://127.0.0.1:5000/download/${encodeURIComponent(filename)}`, {
        headers: { Authorization: `Bearer ${token}` },
        responseType: "blob", // Ensure we get a file response
      });
  
      if (res.data.size === 0) {
        alert("File not found on server!");
        return;
      }
  
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
  
      console.log("Download successful:", filename);
    } catch (error) {
      console.error("Download error:", error);
      alert("Download failed! Check if the file exists on the server.");
    }
  };
  

  return (
    <div>
      <h2>Cloud SaaS System</h2>
      <button onClick={login}>Login</button>

      <h3>Upload File</h3>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={uploadFile}>Upload</button>

      <h3>Download File</h3>
      <input type="text" placeholder="Filename" onChange={(e) => setFilename(e.target.value)} />
      <button onClick={downloadFile}>Download</button>
    </div>
  );
}

export default App;
