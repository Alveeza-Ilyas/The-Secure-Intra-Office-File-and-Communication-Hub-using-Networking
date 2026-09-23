// Real-Time LAN Team Chat Engine

document.addEventListener('DOMContentLoaded', () => {
    const messagesArea = document.getElementById('chatMessagesArea');
    const messageInput = document.getElementById('chatMessageInput');
    const sendBtn = document.getElementById('chatSendBtn');

    let lastKnownCount = 0;
    let isInitialLoad = true;

    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    function getInitials(name) {
        if (!name) return '??';
        const parts = name.trim().split(/\s+/);
        if (parts.length >= 2) {
            return (parts[0][0] + parts[1][0]).toUpperCase();
        }
        return name.slice(0, 2).toUpperCase();
    }

    function formatTime(timestamp) {
        if (!timestamp) return '';
        try {
            const date = new Date(timestamp.replace(' ', 'T'));
            if (!isNaN(date.getTime())) {
                return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            }
        } catch (e) {}
        return timestamp;
    }

    function renderMessages(messages) {
        if (!messagesArea) return;

        messagesArea.innerHTML = '';

        if (messages.length === 0) {
            messagesArea.innerHTML = `
                <div style="text-align: center; color: var(--text-muted); margin: auto;">
                    <div style="font-size: 15px; font-weight: 700; color: var(--text-heading); margin-bottom: 4px;">#intra-office-general</div>
                    <span style="font-size: 13px;">This is the start of your team's persistent LAN channel. Send a message to say hi!</span>
                </div>
            `;
            return;
        }

        messages.forEach(msg => {
            const isSystem = (msg.username.toLowerCase() === 'system');
            const row = document.createElement('div');
            row.className = `chat-bubble-row ${msg.is_me ? 'mine' : ''}`;

            const initials = isSystem ? 'SYS' : getInitials(msg.username);
            const avatarClass = isSystem ? 'chat-sender-avatar system' : 'chat-sender-avatar';

            row.innerHTML = `
                <div class="${avatarClass}">${initials}</div>
                <div class="bubble-content-block">
                    <div class="chat-meta">
                        <span class="chat-author">${escapeHtml(msg.username)}</span>
                        <span class="chat-time">${formatTime(msg.timestamp)}</span>
                    </div>
                    <div class="chat-speech-bubble">${escapeHtml(msg.message)}</div>
                </div>
            `;

            messagesArea.appendChild(row);
        });

        if (isInitialLoad || messages.length > lastKnownCount) {
            messagesArea.scrollTop = messagesArea.scrollHeight;
            lastKnownCount = messages.length;
            isInitialLoad = false;
        }
    }

    async function loadChatMessages() {
        try {
            const res = await fetch('/api/chat/messages');
            if (!res.ok) return;
            const data = await res.json();
            if (data.status === 'success') {
                renderMessages(data.messages);
            }
        } catch (err) {
            console.error('Network sync error:', err);
        }
    }

    async function sendMessage() {
        if (!messageInput) return;
        const text = messageInput.value.trim();
        if (!text) return;

        messageInput.disabled = true;
        if (sendBtn) sendBtn.disabled = true;

        try {
            const res = await fetch('/api/chat/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            if (res.ok) {
                messageInput.value = '';
                await loadChatMessages();
                messagesArea.scrollTop = messagesArea.scrollHeight;
            }
        } catch (err) {
            alert('Failed to transmit message over LAN.');
        } finally {
            messageInput.disabled = false;
            if (sendBtn) sendBtn.disabled = false;
            messageInput.focus();
        }
    }

    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }

    if (messageInput) {
        messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        messageInput.focus();
    }

    // Initial load and polling every 2.5 seconds
    loadChatMessages();
    setInterval(loadChatMessages, 2500);
});
