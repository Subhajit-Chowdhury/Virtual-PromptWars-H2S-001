const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

function appendMessage(role, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;
    
    // Convert newlines to breaks and simple markdown-like formatting
    const formattedText = text.replace(/\n/g, '<br>')
                              .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                              .replace(/\*(.*?)\*/g, '<em>$1</em>');

    msgDiv.innerHTML = `
        <div class="avatar">${role === 'assistant' ? '🤖' : '👤'}</div>
        <div class="content">
            <p>${formattedText}</p>
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

    // Skeleton Loader instead of just dots
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant typing';
    typingDiv.innerHTML = `
        <div class="avatar">🤖</div>
        <div class="content">
            <div class="skeleton sk-1"></div><br>
            <div class="skeleton sk-2"></div><br>
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
            appendMessage('assistant', 'Oops, I had a little hiccup. Could you try that again?');
        }
    } catch (error) {
        if (chatContainer.contains(typingDiv)) chatContainer.removeChild(typingDiv);
        appendMessage('assistant', 'I'm having trouble connecting to my brain! Please check your Vercel Environment Variables (GEMINI_API_KEY, SPREADSHEET_ID, etc).');
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
