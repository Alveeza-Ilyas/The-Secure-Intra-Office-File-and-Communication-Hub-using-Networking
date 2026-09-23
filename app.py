import os
import sqlite3
from datetime import datetime
from functools import wraps
from flask import (
    Flask, render_template, request, redirect,
    url_for, send_from_directory, jsonify, session, flash
)
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'intra-office-hub-secure-token-2026')

# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DATABASE_FILE = os.path.join(BASE_DIR, 'database.db')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB max upload limit

# Ensure uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----------------- Database Helpers ----------------- #

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'staff',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Files Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE NOT NULL,
            original_name TEXT NOT NULL,
            file_size TEXT NOT NULL,
            uploaded_by TEXT NOT NULL,
            upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 3. Chat Messages Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Seed default admin user if not exists
    cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
    if not cursor.fetchone():
        cursor.execute(
            'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
            ('admin', '12345', 'Administrator')
        )
    
    # Seed a demo staff user if not exists
    cursor.execute('SELECT * FROM users WHERE username = ?', ('staff',))
    if not cursor.fetchone():
        cursor.execute(
            'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
            ('staff', '12345', 'Office Staff')
        )

    # Seed initial welcome chat message if table empty
    cursor.execute('SELECT COUNT(*) as count FROM messages')
    if cursor.fetchone()['count'] == 0:
        cursor.execute(
            'INSERT INTO messages (username, message) VALUES (?, ?)',
            ('System', 'Welcome to the Secure Intra-Office Hub! You can chat with colleagues in real-time here.')
        )

    conn.commit()
    conn.close()

# Initialize DB on server start
init_db()

def format_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"

# Sync files on disk with DB if any were manually added
def sync_disk_files():
    conn = get_db_connection()
    cursor = conn.cursor()
    if os.path.exists(UPLOAD_FOLDER):
        for f in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, f)
            if os.path.isfile(file_path):
                cursor.execute('SELECT * FROM files WHERE filename = ?', (f,))
                if not cursor.fetchone():
                    size = format_size(os.path.getsize(file_path))
                    cursor.execute(
                        'INSERT INTO files (filename, original_name, file_size, uploaded_by) VALUES (?, ?, ?, ?)',
                        (f, f, size, 'admin')
                    )
    conn.commit()
    conn.close()

sync_disk_files()

# ----------------- Auth Decorator ----------------- #

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in first to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ----------------- Routes ----------------- #

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f"Welcome back, {user['username']}!", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch all uploaded files ordered by most recent
    cursor.execute('SELECT * FROM files ORDER BY upload_time DESC')
    files_list = cursor.fetchall()
    
    # Get total file count and storage space used
    total_files = len(files_list)
    total_bytes = 0
    if os.path.exists(UPLOAD_FOLDER):
        for f in os.listdir(UPLOAD_FOLDER):
            fp = os.path.join(UPLOAD_FOLDER, f)
            if os.path.isfile(fp):
                total_bytes += os.path.getsize(fp)
    total_storage = format_size(total_bytes)

    # Get recent messages count
    cursor.execute('SELECT COUNT(*) as msg_count FROM messages')
    total_messages = cursor.fetchone()['msg_count']

    conn.close()

    return render_template(
        'dashboard.html',
        username=session.get('username'),
        role=session.get('role'),
        files=files_list,
        total_files=total_files,
        total_storage=total_storage,
        total_messages=total_messages
    )

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part selected in request.', 'error')
        return redirect(url_for('dashboard'))

    file = request.files['file']
    if file.filename == '':
        flash('Please choose a file to upload.', 'warning')
        return redirect(url_for('dashboard'))

    if file:
        original_name = file.filename
        safe_name = secure_filename(original_name)
        if not safe_name:
            safe_name = f"upload_{int(datetime.now().timestamp())}_{original_name}"

        # Prevent name collisions by timestamp prefixing if duplicate exists
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
        if os.path.exists(save_path):
            timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_name = f"{timestamp_str}_{safe_name}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)

        file.save(save_path)
        file_size_bytes = os.path.getsize(save_path)
        formatted_size = format_size(file_size_bytes)
        uploader = session.get('username', 'Unknown')

        # Insert metadata into SQLite
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO files (filename, original_name, file_size, uploaded_by) VALUES (?, ?, ?, ?)',
            (safe_name, original_name, formatted_size, uploader)
        )
        conn.commit()
        conn.close()

        flash(f'File "{original_name}" uploaded successfully!', 'success')

    return redirect(url_for('dashboard'))

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    safe_name = secure_filename(filename)
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        safe_name,
        as_attachment=True
    )

@app.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM files WHERE id = ?', (file_id,))
    file_record = cursor.fetchone()

    if file_record:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_record['filename'])
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                app.logger.error(f"Error removing file: {e}")

        cursor.execute('DELETE FROM files WHERE id = ?', (file_id,))
        conn.commit()
        flash(f'File "{file_record["original_name"]}" was deleted.', 'info')
    else:
        flash('File not found.', 'error')

    conn.close()
    return redirect(url_for('dashboard'))

# ----------------- Chat Routes ----------------- #

@app.route('/chat')
@login_required
def chat():
    return render_template(
        'chat.html',
        username=session.get('username'),
        role=session.get('role')
    )

@app.route('/api/chat/messages', methods=['GET'])
@login_required
def get_chat_messages():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Fetch last 100 messages ordered chronologically
    cursor.execute('SELECT id, username, message, timestamp FROM messages ORDER BY id ASC LIMIT 100')
    rows = cursor.fetchall()
    conn.close()

    messages = []
    for r in rows:
        messages.append({
            'id': r['id'],
            'username': r['username'],
            'message': r['message'],
            'timestamp': r['timestamp'],
            'is_me': (r['username'] == session.get('username'))
        })

    return jsonify({'status': 'success', 'messages': messages})

@app.route('/api/chat/send', methods=['POST'])
@login_required
def send_chat_message():
    data = request.get_json(silent=True) or request.form
    message_text = data.get('message', '').strip()

    if not message_text:
        return jsonify({'status': 'error', 'error': 'Empty message'}), 400

    username = session.get('username', 'Anonymous')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO messages (username, message) VALUES (?, ?)',
        (username, message_text)
    )
    conn.commit()
    msg_id = cursor.lastrowid
    conn.close()

    return jsonify({
        'status': 'success',
        'id': msg_id,
        'username': username,
        'message': message_text,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'is_me': True
    })

# ----------------- Main ----------------- #

if __name__ == '__main__':
    print("\n" + "="*60)
    print(" 🚀 The Secure Intra-Office File & Communication Hub is starting!")
    print(" 🌐 Local Address: http://127.0.0.1:5000")
    print(" 👥 Default Logins: admin / 12345   OR   staff / 12345")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=True)
