# The Secure Intra-Office File & Communication Hub

A lightweight, secure, and self-hosted intranet web application designed for fast file sharing and instant communication within a local office network. Built with **Python (Flask)** and an integrated **SQLite Database**, it features secure user authentication, a centralized file upload/download repository, and real-time team chat.

---

## Project Directory Structure (Konsi file kis folder mein honi chahiye)

Flask application ke theek se chalne ke liye files is tarah organize honi chahiye:

```text
The-Secure-Intra-Office-File-and-Communication-Hub/
│
├── app.py                     # Main Flask Server & SQLite Database Backend
├── database.db                # SQLite Database (Auto-created: users, files, chat messages)
├── requirements.txt           # Python dependencies (Flask, Werkzeug)
├── run.bat                    # Windows 1-Click launcher (Double-click to run & open browser)
├── README.md                  # Complete documentation and setup guide
│
├── templates/                 # Tamaam HTML frontend templates (Jinja2)
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

## How to Run the Application (Chalanay Ka Tareeqa)

### Option 1: 1-Click Run on Windows (Sab se asaan)
Project folder mein mojood **`run.bat`** file par double-click karein:
- Yeh automatic required packages check karega.
- Flask server start karega.
- Browser mein khud-b-khud `http://127.0.0.1:5000` open ho jayega!

---

### Option 2: Terminal / Command Prompt se Chalana
1. Terminal ya Command Prompt open karein aur project folder mein navigate karein.
2. Dependencies install karein:
   ```bash
   pip install -r requirements.txt
   ```
3. Application run karein:
   ```bash
   python app.py
   ```
4. Apnay browser (Chrome/Edge/Firefox) mein yeh link open karein:
   ```text
   http://127.0.0.1:5000/
   ```

> **Important Note:** HTML files ko direct double-click karke (`file:///...`) browser mein open **mat** karein. Flask website hamesha `python app.py` chala kar `http://127.0.0.1:5000` ke zariye browser mein open hoti hai.

---

## Default Login Credentials (Login Details)

Hub mein login karne ke liye ye credentials istemal karein:

* **Administrator:**
  * **Username:** `admin`
  * **Password:** `12345`

* **Staff Member:**
  * **Username:** `staff`
  * **Password:** `12345`

---

## Other Office Devices se Connect Karna (LAN / Wi-Fi)

Agar doosray office computer ya mobile se connect karna ho:
1. Server walay computer ka Local IP address check karein (CMD mein `ipconfig` likhein, maslan: `192.168.1.50`).
2. Kisi bhi doosray computer ke browser mein enter karein:
   ```text
   http://<HOST_IP_ADDRESS>:5000/
   ```
   *(Misaal ke tor par: `http://192.168.1.50:5000/`)*

---

## Features Included

1. **Integrated SQLite Database (`database.db`):**
   - `users`: Logins and role management.
   - `files`: File size, original names, uploader name, upload date/time.
   - `messages`: Real-time persistent office chat history.
2. **Modern Responsive UI:**
   - Dark/Light slate modern styling with Inter font typography.
   - Drag & Drop file uploader with size indicator.
   - Live Instant Search box for searching uploaded files.
   - Copy Direct Link button for sharing files across office network.
   - Real-time LAN Chatroom with auto-scroll and polling.
