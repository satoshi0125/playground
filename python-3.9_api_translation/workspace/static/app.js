document.addEventListener('DOMContentLoaded', function() {
    const translateBtn = document.getElementById('translate-btn');
    const userInput = document.getElementById('user-input');
    const translatedOutput = document.getElementById('translated-output');
    const fromProfile = document.getElementById('from-profile');
    const toProfile = document.getElementById('to-profile');

    translateBtn.addEventListener('click', function() {
        const message = userInput.value.trim();
        if (message) {
            fetch('/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    from_profile: fromProfile.value,
                    to_profile: toProfile.value
                }),
            })
            .then(response => response.json())
            .then(data => {
                translatedOutput.textContent = data.translated_message;
            })
            .catch((error) => {
                console.error('Error:', error);
                translatedOutput.textContent = 'エラーが発生しました。もう一度お試しください。';
            });
        }
    });
});