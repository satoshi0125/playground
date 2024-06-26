let messages = [];
let recognition;

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

// 音声認識の設定
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.lang = 'ja-JP';

    recognition.onresult = function(event) {
        const result = event.results[0][0].transcript;
        document.getElementById('user-input').value = result;
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error', event.error);
    };

    document.getElementById('voice-input-btn').addEventListener('click', function() {
        recognition.start();
        this.textContent = '聞いています...';
        this.classList.remove('bg-green-500', 'hover:bg-green-700');
        this.classList.add('bg-red-500', 'hover:bg-red-700');
    });

    recognition.onend = function() {
        const button = document.getElementById('voice-input-btn');
        button.textContent = '音声入力';
        button.classList.remove('bg-red-500', 'hover:bg-red-700');
        button.classList.add('bg-green-500', 'hover:bg-green-700');
    };
} else {
    console.log('Web Speech API is not supported in this browser.');
    document.getElementById('voice-input-btn').style.display = 'none';
}

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