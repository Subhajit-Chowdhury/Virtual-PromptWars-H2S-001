const chatContainer = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const attachBtn = document.getElementById('attach-btn');
const fileInput = document.getElementById('file-upload');
const resetBtn = document.getElementById('reset-btn');
const statusPill = document.getElementById('data-status');

const ASSISTANT_ICON = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"></path><rect x="4" y="8" width="16" height="12" rx="2"></rect><path d="M2 14h2"></path><path d="M20 14h2"></path><path d="M15 13v2"></path><path d="M9 13v2"></path></svg>`;

function formatResponse(text) {
    const lines = text.split('\n');
    let inTable = false;
    let html = '';
    let tableHtml = '';

    for (let line of lines) {
        if (line.trim().startsWith('|') && line.trim().endsWith('|')) {
            if (!inTable) {
                inTable = true;
                tableHtml = '<div class="table-container"><table>';
            }
            if (line.includes('---')) continue;
            const cells = line.split('|').filter(c => c.trim() !== '').map(c => `<td>${c.trim()}</td>`).join('');
            tableHtml += `<tr>${cells}</tr>`;
        } else {
            if (inTable) {
                inTable = false;
                tableHtml += '</table></div>';
                html += tableHtml;
                tableHtml = '';
            }
            let formattedLine = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                                    .replace(/\*(.*?)\*/g, '<em>$1</em>');
            html += `<p>${formattedLine}</p>`;
        }
    }
    if (inTable) {
        tableHtml += '</table></div>';
        html += tableHtml;
    }
    return html;
}

function appendMessage(role, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message-group ${role}`;
    const formattedContent = formatResponse(text);
    msgDiv.innerHTML = `
        <div class="msg-avatar">${role === 'assistant' ? ASSISTANT_ICON : '🧑'}</div>
        <div class="msg-content">${formattedContent}</div>
    `;
    chatContainer.appendChild(msgDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendMessage(customText = null) {
    const text = customText || userInput.value.trim();
    if (!text) return;

    if (!customText) userInput.value = '';
    appendMessage('user', text);

    const typingDiv = document.createElement('div');
    typingDiv.className = 'message-group assistant typing';
    typingDiv.innerHTML = `<div class="msg-avatar">${ASSISTANT_ICON}</div>
        <div class="msg-content"><div class="skeleton sk-1"></div><div class="skeleton sk-2"></div><div class="skeleton sk-3"></div></div>`;
    chatContainer.appendChild(typingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });
        const data = await response.json();
        chatContainer.removeChild(typingDiv);
        if (data.assistant) {
            appendMessage('assistant', data.assistant);
        } else {
            appendMessage('assistant', "I'm having a little trouble thinking! Could you try that again?");
        }
    } catch (error) {
        if (chatContainer.contains(typingDiv)) chatContainer.removeChild(typingDiv);
        appendMessage('assistant', "I'm having trouble connecting to my brain! Please check your connection.");
        console.error('Error:', error);
    }
}

// Universal Analyzer Logic
attachBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const ext = file.name.split('.').pop().toLowerCase();
    if (!['csv', 'xlsx', 'json'].includes(ext)) {
        appendMessage('assistant', "❌ Sorry, I can only analyze **.csv**, **.xlsx**, and **.json** files. Please try again.");
        fileInput.value = '';
        return;
    }

    const MAX_SIZE_MB = 2;
    if (file.size > MAX_SIZE_MB * 1024 * 1024) {
        appendMessage('assistant', `❌ File too large. Maximum allowed size is **${MAX_SIZE_MB}MB**. Your file is **${(file.size / 1024 / 1024).toFixed(1)}MB**. Please use a smaller dataset.`);
        fileInput.value = '';
        return;
    }

    appendMessage('user', `📎 Uploading ${file.name}...`);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload-file', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (data.success) {
            statusPill.classList.add('custom');
            statusPill.innerHTML = `<span class="dot"></span> Custom Data`;
            appendMessage('assistant', `✅ **File Ready!** I've scanned **${file.name}** and everything looks great. ${data.report_summary || ''}\n\nWhat would you like to know about this dataset?`);
        } else {
            appendMessage('assistant', `❌ **Upload Failed:** ${data.error || 'Unknown error'}`);
        }
    } catch (error) {
        appendMessage('assistant', "❌ **Error:** I couldn't process the file. Make sure it's not password protected.");
    }
    fileInput.value = '';
});

resetBtn.addEventListener('click', async () => {
    try {
        const response = await fetch('/reset-data', { method: 'POST' });
        const data = await response.json();
        if (data.success) {
            statusPill.classList.remove('custom');
            statusPill.innerHTML = `<span class="dot"></span> Live Data`;
            appendMessage('assistant', "🔄 **Reset Complete!** I'm back to reading your original Google Sheets data. How can I help?");
        }
    } catch (error) {
        console.error('Reset error:', error);
    }
});

function handleSuggestion(text) { sendMessage(text); }
sendBtn.addEventListener('click', () => sendMessage());
userInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });
