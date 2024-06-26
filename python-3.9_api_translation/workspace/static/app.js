document.addEventListener('DOMContentLoaded', function() {
    const translateBtn = document.getElementById('translate-btn');
    const userInput = document.getElementById('user-input');
    const translatedOutput = document.getElementById('translated-output');
    const fromProfile = document.getElementById('from-profile');
    const toProfile = document.getElementById('to-profile');
    const voiceInputBtn = document.getElementById('voice-input-btn');
    const voiceOutputBtn = document.getElementById('voice-output-btn');

    let recognition;
    const synth = window.speechSynthesis;
    let voices = [];

    function populateVoiceList() {
        voices = synth.getVoices().sort(function (a, b) {
            const aname = a.name.toUpperCase();
            const bname = b.name.toUpperCase();
            if (aname < bname) return -1;
            else if (aname == bname) return 0;
            else return +1;
        });
    }

    populateVoiceList();
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = populateVoiceList;
    }

    function speak(text) {
        if (synth.speaking) {
            console.error('speechSynthesis.speaking');
            return;
        }
        if (text !== '') {
            const utterThis = new SpeechSynthesisUtterance(text);
            utterThis.onend = function (event) {
                console.log('SpeechSynthesisUtterance.onend');
            }
            utterThis.onerror = function (event) {
                console.error('SpeechSynthesisUtterance.onerror');
            }
            // 日本語の音声を選択（利用可能な場合）
            const japaneseVoice = voices.find(voice => voice.lang === 'ja-JP');
            if (japaneseVoice) {
                utterThis.voice = japaneseVoice;
            }
            utterThis.pitch = 1;
            utterThis.rate = 1;
            synth.speak(utterThis);
        }
    }

    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'ja-JP';

        recognition.onresult = function(event) {
            const result = event.results[0][0].transcript;
            userInput.value += result;
        };

        recognition.onerror = function(event) {
            console.error('音声認識エラー:', event.error);
            voiceInputBtn.textContent = '音声入力';
            voiceInputBtn.classList.remove('bg-red-500', 'hover:bg-red-700');
            voiceInputBtn.classList.add('bg-green-500', 'hover:bg-green-700');
        };

        recognition.onend = function() {
            voiceInputBtn.textContent = '音声入力';
            voiceInputBtn.classList.remove('bg-red-500', 'hover:bg-red-700');
            voiceInputBtn.classList.add('bg-green-500', 'hover:bg-green-700');
        };

        voiceInputBtn.addEventListener('click', function() {
            if (recognition.isStarted) {
                recognition.stop();
            } else {
                recognition.start();
                this.textContent = '停止';
                this.classList.remove('bg-green-500', 'hover:bg-green-700');
                this.classList.add('bg-red-500', 'hover:bg-red-700');
            }
        });
    } else {
        console.log('Web Speech API is not supported in this browser.');
        voiceInputBtn.style.display = 'none';
    }

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

    voiceOutputBtn.addEventListener('click', function() {
        const translatedText = translatedOutput.textContent;
        if (translatedText) {
            speak(translatedText);
        }
    });
});