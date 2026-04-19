const chatContainer = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

const ASSISTANT_ICON = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"></path><rect x="4" y="8" width="16" height="12" rx="2"></rect><path d="M2 14h2"></path><path d="M20 14h2"></path><path d="M15 13v2"></path><path d="M9 13v2"></path></svg>`;

function formatResponse(text) {
    // 1. Handle Markdown Tables
    const tableRegex = /\|(.+)\|/g;
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
            
            // Skip the separator row | --- | --- |
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
            // Standard formatting for non-table lines
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
        <div class="msg-avatar">${role === 'assistant' ? ASSISTANT_ICON : '👤'}</div>
        <div class="msg-content">
            ${formattedContent}
        </div>
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
    typingDiv.innerHTML = `
        <div class="msg-avatar">${ASSISTANT_ICON}</div>
        <div class="msg-content">
            <div class="skeleton sk-1"></div>
            <div class="skeleton sk-2"></div>
            <div class="skeleton sk-3"></div>
        </div>`;
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
        appendMessage('assistant', "I'm having trouble connecting to my brain! Please check your Vercel Environment Variables.");
        console.error('Error:', error);
    }
}

function handleSuggestion(text) {
    sendMessage(text);
}

sendBtn.addEventListener('click', () => sendMessage());
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
