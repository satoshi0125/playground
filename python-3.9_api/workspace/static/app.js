let messages = [];

function addMessage(content, isUser = false) {
    const chatContainer = document.getElementById('chat-container');
    const messageDiv = document.createElement('div');
    messageDiv.className = `mb-2 ${isUser ? 'text-right' : 'text-left'}`;
    const messageContent = document.createElement('span');
    messageContent.className = `inline-block p-2 rounded-lg ${isUser ? 'bg-blue-500 text-white' : 'bg-gray-200 text-black'}`;
    messageContent.innerHTML = marked.parse(content);
    messageDiv.appendChild(messageContent);
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    const role = document.getElementById('role').value;

    if (message) {
        addMessage(message, true);
        userInput.value = '';

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ role: role, message: message, messages: messages }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                addMessage(`エラー: ${data.error}`);
            } else {
                addMessage(data.reply);
                messages = data.messages;
            }
        })
        .catch((error) => {
            addMessage(`エラー: ${error}`);
        });
    }
}