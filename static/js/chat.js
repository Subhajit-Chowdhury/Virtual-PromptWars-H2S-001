const chatContainer = document.getElementById('chat-window');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

function appendMessage(role, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message-group ${role}`;
    
    // Convert newlines to breaks and simple markdown-like formatting
    const formattedText = text.replace(/\n/g, '<br>')
                              .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                              .replace(/\*(.*?)\*/g, '<em>$1</em>');

    msgDiv.innerHTML = `
        <div class="msg-avatar">${role === 'assistant' ? '🤖' : '👤'}</div>
        <div class="msg-content">
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

    // Skeleton Loader for Classic Style
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message-group assistant typing';
    typingDiv.innerHTML = `
        <div class="msg-avatar">🤖</div>
        <div class="msg-content">
            <div class="skeleton sk-1"></div>
            <div class="skeleton sk-2"></div>
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
