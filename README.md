# The Secure Intra-Office File & Communication Hub

A lightweight, secure, and self-hosted intranet web application designed for fast file sharing and instant communication within a local office network. Built with Python (Flask) and an integrated SQLite Database, it features secure user authentication, a centralized file upload/download repository, and real-time team chat.

---

## Project Directory Structure

For the Flask application to function correctly, organize the files as follows:

```text
The-Secure-Intra-Office-File-and-Communication-Hub/
│
├── app.py                     # Main Flask Server & SQLite Database Backend
├── database.db                # SQLite Database (Auto-created: users, files, chat messages)
├── requirements.txt           # Python dependencies (Flask, Werkzeug)
├── run.bat                    # Windows 1-Click launcher (Double-click to run & open browser)
├── README.md                  # Complete documentation and setup guide
│
├── templates/                 # All HTML frontend templates (Jinja2)
│   ├── login.html             # Secure Office Login portal
│   ├── dashboard.html         # File Hub, Uploads & System Control Center
│   └── chat.html              # Intra-office Team Chat room
│
├── static/                    # CSS stylesheets and client JavaScript
│   ├── css/
│   │   └── style.css          # Modern, responsive UI design & color theme
│   └── js/
│       ├── chat.js            # Real-time chat polling, auto-scroll & sending
│       └── dashboard.js       # Live search filter, drag-and-drop & link copying
│
└── uploads/                   # Auto-created folder for storing uploaded office files

```

---

## How to Run the Application

### Option 1: 1-Click Run on Windows (Recommended)

1. Double-click the `run.bat` file located inside the project folder.
2. It will automatically check for required packages and start the Flask server.
3. Your default web browser will automatically open `(http://127.0.0.1:5000/)`.

### Option 2: Run via Terminal / Command Prompt

1. Open Terminal or Command Prompt and navigate to the project directory.
2. Install the required dependencies:
```bash
pip install -r requirements.txt

```


3. Run the application:
```bash
python app.py

```


4. Open your browser (Chrome/Edge/Firefox) and navigate to:
```
http://127.0.0.1:5000/

```



> **Important Note:** Do not open HTML files directly by double-clicking them (`file:///...`). Flask web applications must always be served by running `python app.py` and accessed through `(http://127.0.0.1:5000/)`.

---

## Default Login Credentials

Use the following credentials to authenticate into the hub:

* **Administrator:**
* **Username:** `admin`
* **Password:** `12345`


* **Staff Member:**
* **Username:** `staff`
* **Password:** `12345`



---

## Accessing from Other Office Devices (LAN / Wi-Fi)

To connect from other computers or mobile devices on the same local network:

1. Check the local IP address of the host machine by running `ipconfig` in Command Prompt (e.g., `192.168.1.50`).
2. Open a browser on any other device on the network and navigate to:
```
http://<HOST_IP_ADDRESS>:5000/

```


*(Example: `(http://192.168.1.50:5000/)`)*

