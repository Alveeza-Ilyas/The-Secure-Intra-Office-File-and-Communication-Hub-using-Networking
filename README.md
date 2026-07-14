# The Secure Intra-Office File & Communication Hub

A lightweight, secure, and self-hosted intranet web application designed for fast file sharing and instant communication within a local office network. Built with **Python (Flask)**, it features a secure admin login, a centralized file upload/download dashboard, and a local real-time chat interface.

---

## 🚀 Features

*   **🔒 Secure Access Control:** Simple server login gateway preventing unauthorized access outside the administrative channel[cite: 1, 4].
*   **📂 Centralized File Hub:** Upload, store, and download shared office resources easily[cite: 2, 4]. 
*   **💬 Integrated Chat System:** A client-side message terminal allowing quick communication between connected office staff[cite: 3, 4].
*   **💻 Intranet Ready:** Configured to host on a local server (`0.0.0.0:5000`) so any device on the same local network (Wi-Fi/LAN) can securely connect[cite: 4].

---

## 🛠️ Tech Stack

*   **Backend:** Python 3, Flask[cite: 4]
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla)[cite: 1, 2, 3]
*   **Storage:** Local directory-based file tracking (`/uploads`)[cite: 4]

---

## 📂 Project Directory Structure

To run the application smoothly, make sure your project files are organized as follows:

```text
intra-office-hub/
│
├── app.py                 # Core Flask Backend Server
├── uploads/               # Auto-created folder for uploaded files
└── templates/             # Frontend HTML Views
    ├── login.html         # Portal Authentication Page
    ├── dashboard.html     # Secure File Hub & Control Center
    └── chat.html          # Communication Client Page

```

(Note: Place the `login.html`, `dashboard.html`, and `chat.html` files inside a folder named `templates` so Flask can find them.)

---

## ⚙️ Installation & Local Setup

Follow these steps to spin up the hub on your local machine:

### 1. Install Dependencies

Open your terminal inside the project directory and install **Flask**:

```bash
pip install Flask

```

### 2. Run the Application

Start the Flask server by running:

```bash
python app.py

```

Upon launching, the server will automatically generate an `uploads/` folder in your root directory if it does not already exist.

---

## 🖥️ How to Access the App

### 1. On the Host Machine

Once the server is running, open your browser and navigate to:

```text
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

```

### 2. On Other Office Devices (Same Network)

To access the hub from another device connected to the **same local Wi-Fi or LAN**:

1. Find the local IP address of your host machine (e.g., `192.168.1.50`).
2. Open the browser on the client device and enter:
```text
http://<YOUR_HOST_IP>:5000/

```



---

## 🔑 Default Credentials

Use the default administrative credentials below to bypass the login portal:

* **Username:** `admin`

* **Password:** `12345`
